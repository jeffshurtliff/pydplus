# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_core_instantiation
:Synopsis:          Unit tests for client object instantiation and connection-info compilation
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     29 Mar 2026
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pydplus import PyDPlus, constants as const
from pydplus import errors
from pydplus.core import compile_connection_info


pytestmark = pytest.mark.unit


def test_instantiate_empty_core_object_raises_missing_required_data_error() -> None:
    """Ensure missing base_url raises the expected exception."""
    with pytest.raises(errors.exceptions.MissingRequiredDataError):
        PyDPlus(auto_connect=False)


def test_compile_connection_info_builds_expected_structure(sample_base_url: str) -> None:
    """Ensure connection info is compiled with normalized values."""
    connection_info = compile_connection_info(
        base_url=sample_base_url,
        private_key='/tmp/private.pem',
        legacy_access_id='legacy-access-id',
        oauth_client_id='oauth-client-id',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
    )

    assert connection_info[const.CONNECTION_INFO.LEGACY][const.CONNECTION_INFO.LEGACY_ACCESS_ID] == 'legacy-access-id'
    assert connection_info[const.CONNECTION_INFO.LEGACY][const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH] == '/tmp/'
    assert connection_info[const.CONNECTION_INFO.LEGACY][const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE] == 'private.pem'
    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == 'https://example.com/oauth'
    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_CLIENT_ID] == 'oauth-client-id'
    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_SCOPE] == const.OAUTH_SCOPES.USER_READ


def test_compile_connection_info_adds_oauth_private_key_fields(sample_base_url: str) -> None:
    """Ensure OAuth private-key configuration fields are compiled into connection_info."""
    connection_info = compile_connection_info(
        base_url=sample_base_url,
        oauth_client_id='oauth-client-id',
        oauth_private_key='/tmp/oauth-private-key.jwk',
        oauth_private_key_jwk='{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
    )

    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_PATH] == '/tmp/'
    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_FILE] == 'oauth-private-key.jwk'
    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK] == (
        '{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}'
    )


def test_compile_connection_info_normalizes_oauth_scope_iterable(sample_base_url: str) -> None:
    """Ensure iterable OAuth scope input is normalized to a canonical plus-delimited string."""
    connection_info = compile_connection_info(
        base_url=sample_base_url,
        oauth_client_id='oauth-client-id',
        oauth_scope=(const.OAUTH_SCOPES.USER_READ, const.OAUTH_SCOPES.USER_MANAGE, const.OAUTH_SCOPES.USER_READ),
    )

    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_SCOPE] == (
        f'{const.OAUTH_SCOPES.USER_READ}+{const.OAUTH_SCOPES.USER_MANAGE}'
    )


def test_compile_connection_info_merges_oauth_scope_preset_with_explicit_scope(sample_base_url: str) -> None:
    """Ensure explicit OAuth scopes are merged with preset scopes without duplicates."""
    connection_info = compile_connection_info(
        base_url=sample_base_url,
        oauth_client_id='oauth-client-id',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
        oauth_scope_preset='user_read_only',
    )
    parsed_scopes = connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_SCOPE].split('+')

    assert set(parsed_scopes) == {
        const.OAUTH_SCOPES.USER_READ,
        const.OAUTH_SCOPES.USER_RISKY_READ,
    }
    assert parsed_scopes.count(const.OAUTH_SCOPES.USER_READ) == 1


def test_compile_connection_info_ignores_invalid_oauth_scope_preset_values(sample_base_url: str) -> None:
    """Ensure invalid OAuth scope preset names are ignored while valid ones are applied."""
    connection_info = compile_connection_info(
        base_url=sample_base_url,
        oauth_client_id='oauth-client-id',
        oauth_scope_preset=('user_read_only', 'unknown_preset'),
    )
    parsed_scopes = connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_SCOPE].split('+')

    assert set(parsed_scopes) == {
        const.OAUTH_SCOPES.USER_READ,
        const.OAUTH_SCOPES.USER_RISKY_READ,
    }


def test_compile_connection_info_defaults_to_auth_base_url_for_oauth_issuer(sample_base_url: str) -> None:
    """Ensure OAuth issuer_url defaults to auth_base_url when both admin and auth URLs are defined."""
    connection_info = compile_connection_info(
        base_url=sample_base_url,
        admin_base_url='https://example-admin.com',
        auth_base_url='https://example-auth.com',
        oauth_client_id='oauth-client-id',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
    )

    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == (
        'https://example-auth.com/oauth'
    )


def test_compile_connection_info_uses_admin_base_url_when_oauth_api_type_is_admin(sample_base_url: str) -> None:
    """Ensure OAuth issuer_url uses admin_base_url when oauth_api_type is explicitly set to admin."""
    connection_info = compile_connection_info(
        base_url=sample_base_url,
        admin_base_url='https://example-admin.com',
        auth_base_url='https://example-auth.com',
        oauth_api_type=const.ADMIN_API_TYPE,
        oauth_client_id='oauth-client-id',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
    )

    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == (
        'https://example-admin.com/oauth'
    )


def test_compile_connection_info_infers_auth_base_url_from_admin_url() -> None:
    """Ensure OAuth issuer_url can be inferred from an access-domain admin base URL."""
    connection_info = compile_connection_info(
        admin_base_url='https://example-company.access.securid.com',
        oauth_client_id='oauth-client-id',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
    )

    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == (
        'https://example-company.auth.securid.com/oauth'
    )


def test_compile_connection_info_uses_explicit_oauth_issuer_url(sample_base_url: str) -> None:
    """Ensure explicit oauth_issuer_url takes precedence over inferred issuer values."""
    connection_info = compile_connection_info(
        base_url=sample_base_url,
        admin_base_url='https://example-admin.com',
        auth_base_url='https://example-auth.com',
        oauth_client_id='oauth-client-id',
        oauth_issuer_url='https://issuer.example.com/oauth/',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
    )

    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == (
        'https://issuer.example.com/oauth'
    )


def test_compile_connection_info_raises_for_invalid_oauth_api_type(sample_base_url: str) -> None:
    """Ensure invalid oauth_api_type values raise ValueError."""
    with pytest.raises(ValueError):
        compile_connection_info(
            base_url=sample_base_url,
            oauth_api_type='unsupported',
            oauth_client_id='oauth-client-id',
            oauth_scope=const.OAUTH_SCOPES.USER_READ,
        )


def test_instantiate_core_object_with_connection_info_and_no_auto_connect(
    sample_base_url: str,
    sample_connection_info: dict,
) -> None:
    """Ensure deterministic object creation without network calls when auto_connect is disabled."""
    pydp_object = PyDPlus(
        base_url=sample_base_url,
        connection_info=sample_connection_info,
        auto_connect=False,
    )

    assert pydp_object.base_url == sample_base_url
    assert pydp_object.connected is False
    assert pydp_object.base_headers == {}
    assert pydp_object.admin_base_url == sample_base_url
    assert pydp_object.admin_base_rest_url.endswith('/AdminInterface/restapi')
    assert pydp_object.auth_base_url is None
    assert pydp_object.auth_base_rest_url is None


def test_connection_type_auto_detects_oauth_when_oauth_credentials_are_complete(sample_base_url: str) -> None:
    """Ensure OAuth is auto-selected when complete OAuth credentials are provided and no type is explicit."""
    pydp_object = PyDPlus(
        base_url=sample_base_url,
        oauth_client_id='oauth-client-id',
        oauth_private_key_jwk='{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
        auto_connect=False,
    )

    assert pydp_object.connection_type == const.CONNECTION_INFO.OAUTH


def test_oauth_issuer_url_defaults_to_base_auth_url_when_present() -> None:
    """Ensure inferred OAuth issuer_url defaults to base_auth_url when both base URLs are defined."""
    pydp_object = PyDPlus(
        base_admin_url='https://example-admin.access.securid.com',
        base_auth_url='https://example-auth.auth.securid.com',
        oauth_client_id='oauth-client-id',
        oauth_private_key_jwk='{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
        auto_connect=False,
    )

    assert pydp_object.connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == (
        'https://example-auth.auth.securid.com/oauth'
    )


def test_oauth_issuer_url_uses_base_admin_url_when_oauth_api_type_is_admin() -> None:
    """Ensure inferred OAuth issuer_url uses base_admin_url when oauth_api_type is explicitly set to admin."""
    pydp_object = PyDPlus(
        base_admin_url='https://example-admin.access.securid.com',
        base_auth_url='https://example-auth.auth.securid.com',
        oauth_api_type=const.ADMIN_API_TYPE,
        oauth_client_id='oauth-client-id',
        oauth_private_key_jwk='{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
        auto_connect=False,
    )

    assert pydp_object.connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == (
        'https://example-admin.access.securid.com/oauth'
    )


def test_oauth_issuer_url_is_inferred_from_admin_base_url_when_auth_url_is_missing() -> None:
    """Ensure OAuth issuer_url is inferred from access-domain admin_base_url when auth_base_url is omitted."""
    pydp_object = PyDPlus(
        base_admin_url='https://example-company.access.securid.com',
        oauth_client_id='oauth-client-id',
        oauth_private_key_jwk='{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
        auto_connect=False,
    )

    assert pydp_object.connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == (
        'https://example-company.auth.securid.com/oauth'
    )
    assert pydp_object.auth_base_url == 'https://example-company.auth.securid.com'


def test_oauth_issuer_url_uses_explicit_value_when_defined() -> None:
    """Ensure explicit oauth_issuer_url is retained even when base URLs are available."""
    pydp_object = PyDPlus(
        base_admin_url='https://example-admin.access.securid.com',
        base_auth_url='https://example-auth.auth.securid.com',
        oauth_client_id='oauth-client-id',
        oauth_issuer_url='https://issuer.example.com/oauth',
        oauth_private_key_jwk='{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
        auto_connect=False,
    )

    assert pydp_object.connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == (
        'https://issuer.example.com/oauth'
    )


def test_explicit_connection_type_takes_precedence_over_auto_detect(sample_base_url: str) -> None:
    """Ensure explicit connection_type values are not overwritten by auto-detection."""
    pydp_object = PyDPlus(
        base_url=sample_base_url,
        connection_type=const.CONNECTION_INFO.LEGACY,
        legacy_access_id='legacy-access-id',
        private_key='/tmp/private.pem',
        oauth_client_id='oauth-client-id',
        oauth_private_key_jwk='{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}',
        oauth_scope=const.OAUTH_SCOPES.USER_READ,
        auto_connect=False,
    )

    assert pydp_object.connection_type == const.CONNECTION_INFO.LEGACY


def test_instantiate_core_object_with_legacy_key_material_path(tmp_path: Path) -> None:
    """Ensure legacy key-material paths are parsed and merged into connection info during initialization."""
    key_payload = {
        const.CREDENTIAL_VALUES.JSON_FIELD_CUSTOMER_NAME: 'Example Tenant',
        const.CREDENTIAL_VALUES.JSON_FIELD_ACCESS_ID: 'legacy-access-id',
        const.CREDENTIAL_VALUES.JSON_FIELD_ACCESS_KEY: (
            '-----BEGIN RSA PRIVATE KEY-----\n'
            'test-private-key\n'
            '-----END RSA PRIVATE KEY-----\n'
        ),
        const.CREDENTIAL_VALUES.JSON_FIELD_ADMIN_REST_API_URL: 'https://example.com/AdminInterface/restapi',
    }
    key_file = tmp_path / 'tenant.key'
    key_file.write_text(json.dumps(key_payload), encoding='utf-8')

    pydp_object = PyDPlus(
        connection_type=const.CONNECTION_INFO.LEGACY,
        legacy_key_material=str(key_file),
        auto_connect=False,
    )

    assert pydp_object.base_url == 'https://example.com'
    assert pydp_object.admin_base_url == 'https://example.com'
    assert pydp_object.connection_info[const.CONNECTION_INFO.LEGACY][const.CONNECTION_INFO.LEGACY_ACCESS_ID] == 'legacy-access-id'
    assert pydp_object.connection_info[const.CONNECTION_INFO.LEGACY][const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PEM].startswith(
        '-----BEGIN RSA PRIVATE KEY-----'
    )
