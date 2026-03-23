# -*- coding: utf-8 -*-
"""
:Module:            pydplus.utils.version
:Synopsis:          This module contains the package version information
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     21 Mar 2026
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional
from importlib.metadata import version, PackageNotFoundError
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[import-not-found]

logger = logging.getLogger(__name__)


def get_full_version() -> str:
    """Return the current full version of the ``pydplus`` package.

    The package version is retrieved from the installed package metadata, which is
    populated from the ``version`` field in ``pyproject.toml``.

    :returns: The current package version as a string
    """
    try:
        return version('pydplus')
    except PackageNotFoundError:
        # This can happen if the package is not installed in the environment
        # (e.g. running from a source checkout without an editable install)
        logger.debug('Package is not installed and version will be retrieved from the pyproject.toml file')
        return get_version_from_pyproject()


def get_major_minor_version(full_version: Optional[str] = None) -> str:
    """Return the current major.minor (i.e., X.Y) version of the package.

    :param full_version: The full package version (e.g. X.Y.Z)
    :type full_version: str, None
    :returns: The current package version (X.Y) as a string
    """
    if not full_version:
        full_version = get_full_version()
    parts = full_version.split('.')
    if len(parts) >= 2:
        return '.'.join(parts[:2])
    return full_version


def get_version_from_pyproject(pyproject_path: Optional[str] = None) -> str:
    """Retrieve the current version from the pyproject.toml file.

    :param pyproject_path: The path to the pyproject.toml file (optional)
    :type pyproject_path: str, None
    :returns: The current package version as a string
    """
    path = Path(pyproject_path) if pyproject_path else Path(__file__).resolve().parents[3] / 'pyproject.toml'

    # tomllib.loads() expects a string, while Path.read_bytes() returns bytes
    # Prefer tomllib.load() with a binary file handle to avoid encoding pitfalls
    with path.open('rb') as fp:
        data = tomllib.load(fp)

    # PEP 621
    project_version = data.get('project', {}).get('version')
    if project_version:
        return str(project_version)

    # Poetry legacy layout
    project_version = data.get('tool', {}).get('poetry', {}).get('version')
    if project_version:
        return str(project_version)

    logger.warning("pydplus version could not be retrieved; falling back to '0.0.0' as version")
    return '0.0.0'


# Define __version__ for backward compatibility and to utilize as needed
__version__ = get_full_version()
