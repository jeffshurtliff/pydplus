# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_core_utils
:Synopsis:          Unit tests for utility functions in pydplus.utils.core_utils
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     16 Mar 2026
"""

from __future__ import annotations

import os

import pytest

from pydplus import constants as const
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


def test_remove_ending_slash_handles_paths_with_and_without_trailing_slash() -> None:
    """Ensure remove_ending_slash only removes a trailing slash when present."""
    assert core_utils.remove_ending_slash('https://example.com/') == 'https://example.com'
    assert core_utils.remove_ending_slash('https://example.com') == 'https://example.com'


def test_file_exists_returns_expected_values(tmp_path) -> None:
    """Ensure file_exists returns True for files and False for missing paths."""
    existing_file = tmp_path / 'exists.txt'
    existing_file.write_text('ok', encoding='utf-8')

    assert core_utils.file_exists(str(existing_file)) is True
    assert core_utils.file_exists(str(tmp_path / 'missing.txt')) is False


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


def test_get_file_type_skips_comments_when_detecting_json_content(tmp_path) -> None:
    """Ensure comment lines are skipped before detecting JSON content."""
    unknown_file = tmp_path / 'commented.cfg'
    unknown_file.write_text('# comment\n# other comment\n{"ok": true}\n', encoding='utf-8')

    assert core_utils.get_file_type(str(unknown_file)) == 'json'


def test_get_file_type_raises_unknown_file_type_for_unrecognized_content(tmp_path) -> None:
    """Ensure UnknownFileTypeError is raised when the file type cannot be inferred."""
    unknown_file = tmp_path / 'unrecognized.cfg'
    unknown_file.write_text('# comment only\nkey=value\n', encoding='utf-8')

    with pytest.raises(errors.exceptions.UnknownFileTypeError):
        core_utils.get_file_type(str(unknown_file))


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


def test_get_base_url_raises_type_error_for_non_string_input() -> None:
    """Ensure get_base_url raises TypeError when provided a non-string value."""
    with pytest.raises(TypeError):
        core_utils.get_base_url(123)  # type: ignore[arg-type]


def test_get_base_url_raises_invalid_url_error_for_malformed_url() -> None:
    """Ensure get_base_url raises InvalidURLError for malformed URLs."""
    with pytest.raises(errors.exceptions.InvalidURLError):
        core_utils.get_base_url('not-a-valid-url')


def test_get_random_string_returns_expected_length_and_prefix() -> None:
    """Ensure random string generation honors length and prefix values."""
    generated = core_utils.get_random_string(length=12, prefix_string='pre_')
    assert generated.startswith('pre_')
    assert len(generated) == 16


def test_get_env_variable_name_by_environment_raises_value_error_for_invalid_field() -> None:
    """Ensure invalid environment-variable fields raise ValueError."""
    with pytest.raises(ValueError):
        core_utils.get_env_variable_name_by_environment('invalid-field')


def test_get_env_variable_name_by_environment_uses_default_for_missing_env_values() -> None:
    """Ensure default environment mapping is used when an environment is not provided."""
    default_var = core_utils.get_env_variable_name_by_environment(const.ENV_VARIABLES.VERIFY_SSL_FIELD)
    env_name_var = core_utils.get_env_variable_name_by_environment(const.ENV_VARIABLES.ENV_FIELD)

    assert default_var == const.ENV_VARIABLES.VERIFY_SSL
    assert env_name_var == const.ENV_VARIABLES.ENV_NAME


def test_get_env_variable_name_by_environment_supports_custom_and_named_envs() -> None:
    """Ensure custom, unknown, and known environment names map to expected variable names."""
    custom_var = core_utils.get_env_variable_name_by_environment(const.ENV_VARIABLES.BASE_URL_FIELD, env='custom')
    unknown_var = core_utils.get_env_variable_name_by_environment(const.ENV_VARIABLES.BASE_URL_FIELD, env='stage')
    prod_var = core_utils.get_env_variable_name_by_environment(const.ENV_VARIABLES.BASE_URL_FIELD, env='prod')

    assert custom_var == 'PYDPLUS_CUSTOM_BASE_URL'
    assert unknown_var == 'PYDPLUS_STAGE_BASE_URL'
    assert prod_var == const.ENV_VARIABLES.PROD_BASE_URL


def test_get_env_variable_name_by_environment_raises_runtime_error_for_unexpected_lookup_error() -> None:
    """Ensure unexpected lookup failures are wrapped in RuntimeError."""
    with pytest.raises(RuntimeError):
        core_utils.get_env_variable_name_by_environment(const.ENV_VARIABLES.BASE_URL_FIELD, env=123)  # type: ignore[arg-type]
