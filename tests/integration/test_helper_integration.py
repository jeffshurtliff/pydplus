# -*- coding: utf-8 -*-
"""
:Module:            tests.integration.test_helper_integration
:Synopsis:          Integration tests for helper-file parsing and core object initialization
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     30 Mar 2026
"""

from __future__ import annotations

import pytest

from pydplus import PyDPlus
from pydplus import constants as const
from pydplus.utils.helper import get_helper_settings

pytestmark = [pytest.mark.integration]


def test_get_helper_settings_reads_json_file(helper_json_file) -> None:
    """Ensure JSON helper files are parsed into expected settings."""
    helper_settings = get_helper_settings(str(helper_json_file), file_type='json')

    assert helper_settings[const.HELPER_SETTINGS.BASE_URL] == 'https://example.com'
    assert (
        helper_settings[const.HELPER_SETTINGS.CONNECTION][const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_CLIENT_ID]
        == 'oauth-client-id'
    )


def test_get_helper_settings_reads_yaml_file(helper_yaml_file) -> None:
    """Ensure YAML helper files are parsed into expected settings."""
    helper_settings = get_helper_settings(str(helper_yaml_file), file_type='yaml')

    assert helper_settings[const.HELPER_SETTINGS.BASE_URL] == 'https://example.com'
    assert (
        helper_settings[const.HELPER_SETTINGS.CONNECTION][const.CONNECTION_INFO.LEGACY][const.CONNECTION_INFO.LEGACY_ACCESS_ID]
        == 'legacy-access-id'
    )


def test_core_object_can_initialize_from_helper_file_without_network(helper_json_file) -> None:
    """Ensure helper-based object setup works when auto_connect is disabled."""
    pydp_object = PyDPlus(helper=str(helper_json_file), auto_connect=False)

    assert pydp_object.connected is False
    assert pydp_object.base_url == 'https://example.com'
    assert pydp_object.connection_type == const.CONNECTION_INFO.LEGACY
    assert pydp_object.connection_info[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_ISSUER_URL] == (
        'https://example.com/oauth'
    )
