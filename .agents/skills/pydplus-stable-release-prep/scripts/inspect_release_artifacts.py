#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Module:            pydplus_stable_release_artifacts
:Synopsis:          Validates local PyDPlus release archives before publication
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-6)
:Modified Date:     12 Sep 2026
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Iterable

import constants as const


def canonicalize_name(value: str) -> str:
    """Return the normalized distribution name used for comparisons."""
    return const.NORMALIZE_NAME.sub('-', value).lower()


def sha256(path: Path) -> str:
    """Return the SHA-256 digest for a file."""
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def metadata_values(data: bytes) -> tuple[str | None, str | None]:
    """Return Name and Version values from package metadata."""
    metadata = BytesParser().parsebytes(data)
    return metadata.get('Name'), metadata.get('Version')


def unsafe_archive_paths(names: Iterable[str]) -> list[str]:
    """Return archive members that are unsafe or suspicious for a release."""
    hits: list[str] = []
    for name in names:
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts:
            hits.append(name)
            continue
        lowered = {part.lower() for part in path.parts}
        basename = path.name.lower()
        if lowered & const.FORBIDDEN_COMPONENTS or basename in const.FORBIDDEN_BASENAMES or basename.startswith('._'):
            hits.append(name)
    return hits


def wheel_test_members(names: Iterable[str]) -> list[str]:
    """Return wheel members that contain repository or package test content."""
    hits: list[str] = []
    for name in names:
        path = PurePosixPath(name)
        lowered_parts = tuple(part.lower() for part in path.parts)
        if any(part.endswith(('.dist-info', '.data')) for part in lowered_parts):
            continue
        if {'test', 'tests'} & set(lowered_parts):
            hits.append(name)
    return hits


def project_file_requirements(project_root: Path, project: dict[str, object]) -> tuple[list[str], list[str]]:
    """Return exact files and unmatched license patterns from project metadata."""
    exact = ['pyproject.toml']
    unmatched_patterns: list[str] = []

    readme = project.get('readme')
    if isinstance(readme, str):
        exact.append(PurePosixPath(readme).as_posix())
    elif isinstance(readme, dict) and isinstance(readme.get('file'), str):
        exact.append(PurePosixPath(readme['file']).as_posix())

    license_value = project.get('license')
    if isinstance(license_value, dict) and isinstance(license_value.get('file'), str):
        exact.append(PurePosixPath(license_value['file']).as_posix())
    elif isinstance(license_value, str) and (project_root / license_value).is_file():
        exact.append(PurePosixPath(license_value).as_posix())

    license_files = project.get('license-files')
    if isinstance(license_files, list):
        for pattern in license_files:
            if not isinstance(pattern, str):
                continue
            try:
                matches = [
                    path for path in project_root.glob(pattern) if path.is_file() and path.resolve().is_relative_to(project_root)
                ]
            except (OSError, ValueError):
                matches = []
            if matches:
                exact.extend(path.relative_to(project_root).as_posix() for path in matches)
            else:
                unmatched_patterns.append(pattern)

    return list(dict.fromkeys(exact)), unmatched_patterns


def relative_sdist_names(names: Iterable[str], archive_root: str) -> list[PurePosixPath]:
    """Return source-distribution member paths without their archive root."""
    paths = [PurePosixPath(name) for name in names]
    return [PurePosixPath(*path.parts[1:]) for path in paths if len(path.parts) > 1 and path.parts[0] == archive_root]


def inspect_sdist(
    path: Path,
    expected_name: str,
    expected_version: str,
    required_files: list[str],
) -> tuple[list[str], list[str]]:
    """Inspect a source distribution and return errors and warnings."""
    errors: list[str] = []
    warnings: list[str] = []

    expected_suffix = f'-{expected_version}.tar.gz'
    if not path.name.endswith(expected_suffix):
        errors.append(f'{path.name}: filename does not end with {expected_suffix}')
    else:
        filename_name = path.name[: -len(expected_suffix)]
        if canonicalize_name(filename_name) != canonicalize_name(expected_name):
            errors.append(f'{path.name}: filename distribution does not match {expected_name}')

    with tarfile.open(path, mode='r:gz') as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        metadata_members = [member for member in members if PurePosixPath(member.name).name == 'PKG-INFO']
        archive_root: str | None = None
        if len(metadata_members) != 1:
            errors.append(f'{path.name}: expected one PKG-INFO file, found {len(metadata_members)}')
        else:
            metadata_path = PurePosixPath(metadata_members[0].name)
            if len(metadata_path.parts) < 2:
                errors.append(f'{path.name}: PKG-INFO is not inside a source-distribution root directory')
            else:
                archive_root = metadata_path.parts[0]
            stream = archive.extractfile(metadata_members[0])
            if stream is None:
                errors.append(f'{path.name}: could not read PKG-INFO')
            else:
                name, version = metadata_values(stream.read())
                if name is None or canonicalize_name(name) != canonicalize_name(expected_name):
                    errors.append(f'{path.name}: metadata Name {name!r} does not match {expected_name!r}')
                if version != expected_version:
                    errors.append(f'{path.name}: metadata Version {version!r} does not match {expected_version!r}')

        if archive_root is not None:
            relative_names = {name.as_posix() for name in relative_sdist_names(names, archive_root)}
            for required in required_files:
                if required not in relative_names:
                    errors.append(f'{path.name}: missing required source file {required}')

        suspicious = unsafe_archive_paths(names)
        if suspicious:
            warnings.append(f'{path.name}: suspicious members: {", ".join(suspicious[:10])}')

        if not any(name.endswith('.py') for name in names):
            warnings.append(f'{path.name}: no Python source file found')

    return errors, warnings


def inspect_wheel(path: Path, expected_name: str, expected_version: str) -> tuple[list[str], list[str]]:
    """Inspect a wheel and return errors and warnings."""
    errors: list[str] = []
    warnings: list[str] = []

    filename_parts = path.name.removesuffix('.whl').split('-')
    if len(filename_parts) < 5:
        errors.append(f'{path.name}: malformed wheel filename')
    else:
        if canonicalize_name(filename_parts[0]) != canonicalize_name(expected_name):
            errors.append(f'{path.name}: filename distribution does not match {expected_name}')
        if filename_parts[1] != expected_version:
            errors.append(f'{path.name}: filename version {filename_parts[1]!r} does not match {expected_version!r}')

    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        metadata_names = [name for name in names if name.endswith('.dist-info/METADATA')]
        if len(metadata_names) != 1:
            errors.append(f'{path.name}: expected one METADATA file, found {len(metadata_names)}')
        else:
            name, version = metadata_values(archive.read(metadata_names[0]))
            if name is None or canonicalize_name(name) != canonicalize_name(expected_name):
                errors.append(f'{path.name}: metadata Name {name!r} does not match {expected_name!r}')
            if version != expected_version:
                errors.append(f'{path.name}: metadata Version {version!r} does not match {expected_version!r}')

        suspicious = unsafe_archive_paths(names)
        if suspicious:
            warnings.append(f'{path.name}: suspicious members: {", ".join(suspicious[:10])}')

        test_members = wheel_test_members(names)
        if test_members:
            warnings.append(f'{path.name}: test content included: {", ".join(test_members[:10])}')

        code_members = [
            name for name in names if '.dist-info/' not in name and '.data/' not in name and name.endswith(('.py', '.so', '.pyd'))
        ]
        if not code_members:
            warnings.append(f'{path.name}: no importable package code found')

    return errors, warnings


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, default=const.DEFAULT_PROJECT_ROOT)
    parser.add_argument('--dist-dir', type=Path)
    parser.add_argument('--expected-version', required=True)
    parser.add_argument('--expected-wheel-count', type=int, default=1)
    parser.add_argument('--strict', action='store_true', help='Treat suspicious archive warnings as failures.')
    return parser.parse_args()


def main() -> int:
    """Inspect release artifacts and print a readiness summary."""
    args = parse_args()
    project_root = args.project_root.resolve()
    dist_dir = (args.dist_dir or project_root / 'dist').resolve()
    pyproject_path = project_root / 'pyproject.toml'

    if not pyproject_path.is_file():
        print(f'ERROR: missing {pyproject_path}', file=sys.stderr)
        return 1
    if not dist_dir.is_dir():
        print(f'ERROR: missing distribution directory {dist_dir}', file=sys.stderr)
        return 1

    with pyproject_path.open('rb') as stream:
        pyproject = tomllib.load(stream)
    project = pyproject.get('project')
    if not isinstance(project, dict) or not isinstance(project.get('name'), str):
        print('ERROR: pyproject.toml must define [project].name', file=sys.stderr)
        return 1

    expected_name = project['name']
    project_version = project.get('version')
    errors: list[str] = []
    warnings: list[str] = []
    if canonicalize_name(expected_name) != const.EXPECTED_PROJECT_NAME:
        errors.append(f'pyproject.toml project name {expected_name!r} is not {const.EXPECTED_PROJECT_NAME!r}')
    if project_version != args.expected_version:
        errors.append(f'pyproject.toml version {project_version!r} does not match expected version {args.expected_version!r}')

    sdists = sorted(dist_dir.glob('*.tar.gz'))
    wheels = sorted(dist_dir.glob('*.whl'))
    expected_entries = {*sdists, *wheels}
    unexpected = sorted(
        path.name for path in dist_dir.iterdir() if path not in expected_entries and path.name not in const.ALLOWED_DIST_METADATA
    )

    if len(sdists) != 1:
        errors.append(f'expected one source distribution, found {len(sdists)}')
    if len(wheels) != args.expected_wheel_count:
        errors.append(f'expected {args.expected_wheel_count} wheel(s), found {len(wheels)}')
    if unexpected:
        warnings.append(f'unexpected files in dist directory: {", ".join(unexpected)}')

    required_files, unmatched_patterns = project_file_requirements(project_root, project)
    for pattern in unmatched_patterns:
        errors.append(f'pyproject.toml license-files pattern {pattern!r} matches no project file')
    for path in sdists:
        try:
            found_errors, found_warnings = inspect_sdist(
                path,
                expected_name,
                args.expected_version,
                required_files,
            )
        except (OSError, tarfile.TarError) as error:
            found_errors = [f'{path.name}: unreadable source distribution: {error}']
            found_warnings = []
        errors.extend(found_errors)
        warnings.extend(found_warnings)
    for path in wheels:
        try:
            found_errors, found_warnings = inspect_wheel(path, expected_name, args.expected_version)
        except (OSError, zipfile.BadZipFile) as error:
            found_errors = [f'{path.name}: unreadable wheel: {error}']
            found_warnings = []
        errors.extend(found_errors)
        warnings.extend(found_warnings)

    print(f'Project: {expected_name}')
    print(f'Version: {args.expected_version}')
    print(f'Artifacts: {len(sdists)} sdist, {len(wheels)} wheel(s)')
    for path in [*sdists, *wheels]:
        print(f'SHA256 {path.name} {sha256(path)}')

    for warning in warnings:
        print(f'WARNING: {warning}', file=sys.stderr)
    for error in errors:
        print(f'ERROR: {error}', file=sys.stderr)

    if errors or (args.strict and warnings):
        return 1
    print('Artifact inspection passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
