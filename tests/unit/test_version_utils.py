# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_version_utils
:Synopsis:          Unit tests for pydplus.utils.version helpers
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     30 Mar 2026
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError

import pytest

from pydplus.utils import version as version_utils

pytestmark = pytest.mark.unit


def test_get_major_minor_version_returns_first_two_segments() -> None:
    """Ensure major.minor values are extracted from semantic versions."""
    assert version_utils.get_major_minor_version('2.7.9') == '2.7'


def test_get_major_minor_version_returns_original_for_short_version() -> None:
    """Ensure non-semver strings are returned unchanged when no minor segment exists."""
    assert version_utils.get_major_minor_version('2') == '2'


def test_get_full_version_falls_back_to_pyproject(monkeypatch) -> None:
    """Ensure fallback logic is used when package metadata is unavailable."""

    def _raise_package_not_found(_package_name: str):
        raise PackageNotFoundError

    monkeypatch.setattr(version_utils, 'version', _raise_package_not_found)
    monkeypatch.setattr(version_utils, 'get_version_from_pyproject', lambda: '9.9.9')

    assert version_utils.get_full_version() == '9.9.9'


def test_get_version_from_pyproject_reads_pep621_layout(tmp_path) -> None:
    """Ensure version is read from the [project] table when present."""
    pyproject_file = tmp_path / 'pyproject.toml'
    pyproject_file.write_text('[project]\nversion = "1.2.3"\n', encoding='utf-8')

    assert version_utils.get_version_from_pyproject(str(pyproject_file)) == '1.2.3'


def test_get_version_from_pyproject_reads_poetry_layout(tmp_path) -> None:
    """Ensure version is read from the legacy [tool.poetry] table when needed."""
    pyproject_file = tmp_path / 'pyproject.toml'
    pyproject_file.write_text('[tool.poetry]\nversion = "4.5.6"\n', encoding='utf-8')

    assert version_utils.get_version_from_pyproject(str(pyproject_file)) == '4.5.6'


def test_get_version_from_pyproject_defaults_when_version_missing(tmp_path) -> None:
    """Ensure a stable fallback is returned when no version keys exist."""
    pyproject_file = tmp_path / 'pyproject.toml'
    pyproject_file.write_text('[tool.poetry]\nname = "pydplus"\n', encoding='utf-8')

    assert version_utils.get_version_from_pyproject(str(pyproject_file)) == '0.0.0'
