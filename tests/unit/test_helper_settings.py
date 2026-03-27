# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_helper_settings
:Synopsis:          Unit tests for helper configuration functions in pydplus.utils.helper
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     25 Mar 2026
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pydplus import constants as const
from pydplus import errors
from pydplus.utils import helper


pytestmark = pytest.mark.unit


def _write_json_file(tmp_path: Path, file_name: str, payload: dict) -> str:
    """Write a JSON payload to a temporary file and return its path."""
    helper_file = tmp_path / file_name
    helper_file.write_text(json.dumps(payload), encoding='utf-8')
    return str(helper_file)


def test_import_helper_file_parses_json_when_extension_uses_dot_prefix(tmp_path: Path) -> None:
    """Ensure JSON helper files parse successfully when file_type includes a leading dot."""
    helper_path = _write_json_file(tmp_path, 'helper.json', {const.HELPER_SETTINGS.TENANT_NAME: 'tenant-a'})
    parsed = helper.import_helper_file(helper_path, '.json')

    assert parsed == {const.HELPER_SETTINGS.TENANT_NAME: 'tenant-a'}


def test_import_helper_file_parses_yaml_content(tmp_path: Path) -> None:
    """Ensure YAML helper files are parsed with yaml.safe_load."""
    helper_file = tmp_path / 'helper.yaml'
    helper_file.write_text('tenant_name: tenant-a\nstrict_mode: yes\n', encoding='utf-8')

    parsed = helper.import_helper_file(str(helper_file), const.FILE_EXTENSIONS.YAML)

    assert parsed[const.HELPER_SETTINGS.TENANT_NAME] == 'tenant-a'
    assert parsed[const.HELPER_SETTINGS.STRICT_MODE] is True


def test_import_helper_file_raises_invalid_helper_file_type_error(tmp_path: Path) -> None:
    """Ensure unsupported helper file types raise InvalidHelperFileTypeError."""
    helper_path = _write_json_file(tmp_path, 'helper.data', {'ok': True})

    with pytest.raises(errors.exceptions.InvalidHelperFileTypeError):
        helper.import_helper_file(helper_path, 'txt')


def test_import_helper_file_raises_file_not_found_for_missing_file(tmp_path: Path) -> None:
    """Ensure missing helper files raise FileNotFoundError."""
    missing_file = tmp_path / 'missing.json'

    with pytest.raises(FileNotFoundError):
        helper.import_helper_file(str(missing_file), const.FILE_EXTENSIONS.JSON)


@pytest.mark.parametrize(
    ('yaml_value', 'expected'),
    [
        ('yes', True),
        ('TRUE', True),
        ('no', False),
        ('false', False),
    ],
)
def test_convert_yaml_to_bool(yaml_value: str, expected: bool) -> None:
    """Ensure helper YAML-style conversion returns expected Boolean values."""
    assert helper._convert_yaml_to_bool(yaml_value) is expected


def test_convert_yaml_to_bool_raises_value_error_for_invalid_value() -> None:
    """Ensure helper YAML-style conversion raises ValueError for unknown values."""
    with pytest.raises(ValueError):
        helper._convert_yaml_to_bool('something-else')


def test_get_connection_info_returns_known_nested_connection_fields_only() -> None:
    """Ensure helper connection parsing keeps supported keys and drops unsupported ones."""
    helper_cfg = {
        const.HELPER_SETTINGS.CONNECTION: {
            const.CONNECTION_INFO.LEGACY: {
                const.CONNECTION_INFO.LEGACY_ACCESS_ID: 'legacy-access-id',
                'unexpected': 'ignore-me',
            },
            const.CONNECTION_INFO.OAUTH: {
                const.CONNECTION_INFO.OAUTH_CLIENT_ID: 'oauth-client-id',
                const.CONNECTION_INFO.OAUTH_SCOPE: const.OAUTH_SCOPES.USER_READ,
                const.CONNECTION_INFO.OAUTH_GRANT_TYPE: const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE,
                'unexpected': 'ignore-me',
            },
        },
    }

    connection_info = helper._get_connection_info(helper_cfg)

    assert connection_info == {
        const.CONNECTION_INFO.LEGACY: {
            const.CONNECTION_INFO.LEGACY_ACCESS_ID: 'legacy-access-id',
        },
        const.CONNECTION_INFO.OAUTH: {
            const.CONNECTION_INFO.OAUTH_CLIENT_ID: 'oauth-client-id',
            const.CONNECTION_INFO.OAUTH_SCOPE: const.OAUTH_SCOPES.USER_READ,
            const.CONNECTION_INFO.OAUTH_GRANT_TYPE: const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE,
        },
    }


def test_get_connection_info_returns_empty_mappings_when_connection_section_missing() -> None:
    """Ensure missing connection sections still return legacy and oauth keys with empty values."""
    assert helper._get_connection_info({}) == {
        const.CONNECTION_INFO.LEGACY: {},
        const.CONNECTION_INFO.OAUTH: {},
    }


def test_collect_values_converts_boolean_values_and_assigns_expected_defaults() -> None:
    """Ensure helper value collection converts YAML bool values and sets defaults for missing keys."""
    helper_cfg = {
        const.HELPER_SETTINGS.STRICT_MODE: 'no',
        const.HELPER_SETTINGS.TENANT_NAME: 'tenant-a',
    }

    collected = helper._collect_values(
        (
            const.HELPER_SETTINGS.STRICT_MODE,
            const.HELPER_SETTINGS.VERIFY_SSL,
            const.HELPER_SETTINGS.TENANT_NAME,
            const.HELPER_SETTINGS.ENV_NAME,
        ),
        helper_cfg,
    )

    assert collected[const.HELPER_SETTINGS.STRICT_MODE] is False
    assert collected[const.HELPER_SETTINGS.VERIFY_SSL] is True
    assert collected[const.HELPER_SETTINGS.TENANT_NAME] == 'tenant-a'
    assert collected[const.HELPER_SETTINGS.ENV_NAME] is None


def test_collect_values_handles_single_key_input_and_ignore_missing_mode() -> None:
    """Ensure string key input and ignore-missing mode do not inject null placeholder fields."""
    existing_values = {const.HELPER_SETTINGS.BASE_URL: 'https://idp.example.com'}

    collected = helper._collect_values(
        const.HELPER_SETTINGS.ENV_NAME,
        {},
        _helper_dict=existing_values,
        _ignore_missing=True,
    )

    assert collected is existing_values
    assert collected == {const.HELPER_SETTINGS.BASE_URL: 'https://idp.example.com'}


def test_get_helper_settings_parses_root_and_nested_settings(tmp_path: Path) -> None:
    """Ensure get_helper_settings reads root, URL, connection, and env-variable helper sections."""
    helper_payload = {
        const.HELPER_SETTINGS.ENV_NAME: 'DEV',
        const.HELPER_SETTINGS.TENANT_NAME: 'tenant-a',
        const.HELPER_SETTINGS.BASE_URL: 'https://idp.example.com',
        const.HELPER_SETTINGS.CONNECTION_TYPE: const.CONNECTION_INFO.OAUTH,
        const.HELPER_SETTINGS.STRICT_MODE: 'yes',
        const.HELPER_SETTINGS.BASE_URLS: {
            const.HELPER_SETTINGS.ADMIN: 'https://admin.example.com',
            const.HELPER_SETTINGS.AUTH: 'https://auth.example.com',
        },
        const.HELPER_SETTINGS.CONNECTION: {
            const.CONNECTION_INFO.LEGACY: {
                const.CONNECTION_INFO.LEGACY_ACCESS_ID: 'legacy-access-id',
                const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH: '/tmp/private.key',
            },
            const.CONNECTION_INFO.OAUTH: {
                const.CONNECTION_INFO.OAUTH_ISSUER_URL: 'https://issuer.example.com',
                const.CONNECTION_INFO.OAUTH_CLIENT_ID: 'oauth-client-id',
                const.CONNECTION_INFO.OAUTH_SCOPE: const.OAUTH_SCOPES.USER_READ,
                const.CONNECTION_INFO.OAUTH_GRANT_TYPE: const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE,
                const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION: const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH,
            },
        },
        const.HELPER_SETTINGS.ENV_VARIABLES: 'CUSTOM_ENV_VARS',
    }
    helper_path = _write_json_file(tmp_path, 'helper.json', helper_payload)

    settings = helper.get_helper_settings(helper_path, const.FILE_EXTENSIONS.JSON)

    assert settings[const.HELPER_SETTINGS.ENV_NAME] == 'DEV'
    assert settings[const.HELPER_SETTINGS.TENANT_NAME] == 'tenant-a'
    assert settings[const.HELPER_SETTINGS.BASE_URL] == 'https://idp.example.com'
    assert settings[const.HELPER_SETTINGS.CONNECTION_TYPE] == const.CONNECTION_INFO.OAUTH
    assert settings[const.HELPER_SETTINGS.STRICT_MODE] is True
    assert settings[const.HELPER_SETTINGS.VERIFY_SSL] is True
    assert settings[const.HELPER_SETTINGS.ADMIN_BASE_URL] == 'https://admin.example.com'
    assert settings[const.HELPER_SETTINGS.AUTH_BASE_URL] == 'https://auth.example.com'
    assert settings[const.HELPER_SETTINGS.CONNECTION][const.CONNECTION_INFO.LEGACY] == {
        const.CONNECTION_INFO.LEGACY_ACCESS_ID: 'legacy-access-id',
        const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH: '/tmp/private.key',
    }
    assert settings[const.HELPER_SETTINGS.CONNECTION][const.CONNECTION_INFO.OAUTH] == {
        const.CONNECTION_INFO.OAUTH_ISSUER_URL: 'https://issuer.example.com',
        const.CONNECTION_INFO.OAUTH_CLIENT_ID: 'oauth-client-id',
        const.CONNECTION_INFO.OAUTH_SCOPE: const.OAUTH_SCOPES.USER_READ,
        const.CONNECTION_INFO.OAUTH_GRANT_TYPE: const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE,
        const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION: const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH,
    }
    assert settings[const.HELPER_SETTINGS.ENV_VARIABLES] == 'CUSTOM_ENV_VARS'


def test_get_helper_settings_infers_file_type_for_invalid_file_type(tmp_path: Path, monkeypatch) -> None:
    """Ensure invalid file_type values trigger get_file_type inference."""
    helper_path = _write_json_file(tmp_path, 'helper.custom', {const.HELPER_SETTINGS.TENANT_NAME: 'tenant-a'})
    observed_file_path = {'value': None}

    def _fake_get_file_type(file_path: str) -> str:
        observed_file_path['value'] = file_path
        return const.FILE_EXTENSIONS.JSON

    monkeypatch.setattr(helper, 'get_file_type', _fake_get_file_type)

    settings = helper.get_helper_settings(helper_path, file_type='custom')

    assert observed_file_path['value'] == helper_path
    assert settings[const.HELPER_SETTINGS.TENANT_NAME] == 'tenant-a'
    assert settings[const.HELPER_SETTINGS.VERIFY_SSL] is True


def test_get_helper_settings_preserves_defined_connection_and_env_variables(tmp_path: Path) -> None:
    """Ensure predefined connection/env-variable settings are not replaced by helper file content."""
    helper_payload = {
        const.HELPER_SETTINGS.TENANT_NAME: 'tenant-from-file',
        const.HELPER_SETTINGS.CONNECTION: {
            const.CONNECTION_INFO.LEGACY: {
                const.CONNECTION_INFO.LEGACY_ACCESS_ID: 'file-access-id',
            },
        },
        const.HELPER_SETTINGS.ENV_VARIABLES: {
            const.HELPER_SETTINGS.BASE_URL: 'FILE_BASE_URL',
        },
    }
    helper_path = _write_json_file(tmp_path, 'defined.json', helper_payload)

    expected_connection = {
        const.CONNECTION_INFO.LEGACY: {const.CONNECTION_INFO.LEGACY_ACCESS_ID: 'defined-access-id'},
        const.CONNECTION_INFO.OAUTH: {},
    }
    expected_env_variables = {const.HELPER_SETTINGS.BASE_URL: 'DEFINED_BASE_URL'}
    defined_settings = {
        const.HELPER_SETTINGS.CONNECTION: expected_connection,
        const.HELPER_SETTINGS.ENV_VARIABLES: expected_env_variables,
    }

    settings = helper.get_helper_settings(
        file_path=helper_path,
        file_type=const.FILE_EXTENSIONS.JSON,
        defined_settings=defined_settings,
    )

    assert settings[const.HELPER_SETTINGS.CONNECTION] == expected_connection
    assert settings[const.HELPER_SETTINGS.ENV_VARIABLES] == expected_env_variables
