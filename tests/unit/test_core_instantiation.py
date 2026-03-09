# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_core_instantiation
:Synopsis:          Unit tests for client object instantiation and connection-info compilation
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     09 Mar 2026
"""

from __future__ import annotations

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
    assert pydp_object.admin_base_url.endswith('/AdminInterface/restapi')
    assert pydp_object.auth_base_url.endswith('/mfa/v1_1/authn')
