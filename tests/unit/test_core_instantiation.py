# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_core_instantiation
:Synopsis:          Unit tests for client object instantiation and connection-info compilation
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     18 Mar 2026
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
    )

    assert connection_info[const.CONNECTION_INFO.LEGACY][const.CONNECTION_INFO.LEGACY_ACCESS_ID] == 'legacy-access-id'
    assert connection_info[const.CONNECTION_INFO.LEGACY][const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH] == '/tmp/'
    assert connection_info[const.CONNECTION_INFO.LEGACY][const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE] == 'private.pem'
    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == 'https://example.com/oauth'
    assert connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_CLIENT_ID] == 'oauth-client-id'


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
