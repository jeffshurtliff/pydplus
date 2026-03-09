# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_core_utils
:Synopsis:          Unit tests for utility functions in pydplus.utils.core_utils
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     09 Mar 2026
"""

from __future__ import annotations

import os

import pytest

from pydplus import errors
from pydplus.utils import core_utils


pytestmark = pytest.mark.unit


def test_url_encode_decode_round_trip() -> None:
    """Ensure URL encoding and decoding preserve the original string."""
    raw_string = 'john.doe@example.com + id'
    encoded_string = core_utils.url_encode(raw_string)

    assert encoded_string != raw_string
    assert core_utils.url_decode(encoded_string) == raw_string


def test_ensure_ending_slash_for_url_and_file_path(tmp_path) -> None:
    """Ensure URL and file paths receive trailing separators when missing."""
    assert core_utils.ensure_ending_slash('https://example.com') == 'https://example.com/'

    file_path = str(tmp_path / 'subdir')
    assert core_utils.ensure_ending_slash(file_path, path_type='file').endswith(os.sep)


def test_ensure_ending_slash_invalid_path_type_raises_invalid_parameter_error() -> None:
    """Ensure invalid path types raise InvalidParameterError."""
    with pytest.raises(errors.exceptions.InvalidParameterError):
        core_utils.ensure_ending_slash('https://example.com', path_type='invalid')


def test_get_file_type_detects_json_and_yaml_extensions(tmp_path) -> None:
    """Ensure file types are identified by extension when possible."""
    json_file = tmp_path / 'config.json'
    json_file.write_text('{"ok": true}', encoding='utf-8')

    yaml_file = tmp_path / 'config.yaml'
    yaml_file.write_text('ok: true\n', encoding='utf-8')

    assert core_utils.get_file_type(str(json_file)) == 'json'
    assert core_utils.get_file_type(str(yaml_file)) == 'yaml'


def test_get_file_type_detects_json_by_content_when_extension_unknown(tmp_path) -> None:
    """Ensure unknown file extensions can still be detected by file contents."""
    unknown_file = tmp_path / 'config.cfg'
    unknown_file.write_text('{"ok": true}\n', encoding='utf-8')

    assert core_utils.get_file_type(str(unknown_file)) == 'json'


def test_get_file_type_raises_file_not_found_for_missing_path(tmp_path) -> None:
    """Ensure missing files raise FileNotFoundError."""
    missing_file = tmp_path / 'missing.json'
    with pytest.raises(FileNotFoundError):
        core_utils.get_file_type(str(missing_file))


def test_split_file_path_returns_path_and_file_name() -> None:
    """Ensure split_file_path returns a directory path and basename."""
    file_path, file_name = core_utils.split_file_path('/tmp/example/config.json')
    assert file_path == f'/tmp/example{os.sep}'
    assert file_name == 'config.json'


def test_get_base_url_returns_expected_values() -> None:
    """Ensure URL parsing can include or exclude the scheme."""
    full_url = 'https://example.com/path/to/resource?id=1'
    assert core_utils.get_base_url(full_url, include_scheme=True) == 'https://example.com'
    assert core_utils.get_base_url(full_url, include_scheme=False) == 'example.com'
