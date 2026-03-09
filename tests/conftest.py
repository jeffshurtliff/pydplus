# -*- coding: utf-8 -*-
"""
:Module:            tests.conftest
:Synopsis:          Shared pytest fixtures and test-session hooks
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     09 Mar 2026
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pydplus import constants as const


class MockResponse:
    """Mocked response object with a json() method and status code."""

    def __init__(self, json_body, status_code: int = 200):
        self.json_body = json_body
        self.status_code = status_code

    def json(self):
        """Return the mocked JSON response body."""
        return self.json_body


@pytest.fixture
def sample_base_url() -> str:
    """Return a deterministic base URL for tests."""
    return 'https://example.com'


@pytest.fixture
def sample_connection_info(sample_base_url: str) -> dict:
    """Return a deterministic connection_info dictionary for core object tests."""
    return {
        const.CONNECTION_INFO.LEGACY: {
            const.CONNECTION_INFO.LEGACY_ACCESS_ID: 'legacy-access-id',
            const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH: '/tmp/',
            const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE: 'private.pem',
        },
        const.CONNECTION_INFO.OAUTH: {
            const.CONNECTION_INFO.OAUTH_ISSUER_URL: const.URLS.OAUTH.format(base_url=sample_base_url),
            const.CONNECTION_INFO.OAUTH_CLIENT_ID: 'oauth-client-id',
            const.CONNECTION_INFO.OAUTH_GRANT_TYPE: const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE,
            const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION: const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH,
        },
    }


@pytest.fixture
def sample_helper_config(sample_base_url: str) -> dict:
    """Return a helper configuration payload usable for JSON and YAML fixtures."""
    return {
        const.HELPER_SETTINGS.BASE_URL: sample_base_url,
        const.HELPER_SETTINGS.CONNECTION_TYPE: const.CONNECTION_INFO.LEGACY,
        const.HELPER_SETTINGS.STRICT_MODE: False,
        const.HELPER_SETTINGS.VERIFY_SSL: True,
        const.HELPER_SETTINGS.CONNECTION: {
            const.CONNECTION_INFO.LEGACY: {
                const.CONNECTION_INFO.LEGACY_ACCESS_ID: 'legacy-access-id',
                const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH: '/tmp/',
                const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE: 'private.pem',
            },
            const.CONNECTION_INFO.OAUTH: {
                const.CONNECTION_INFO.OAUTH_CLIENT_ID: 'oauth-client-id',
            },
        },
    }


@pytest.fixture
def helper_json_file(tmp_path: Path, sample_helper_config: dict) -> Path:
    """Create a temporary JSON helper file and return its path."""
    helper_file = tmp_path / 'helper.json'
    helper_file.write_text(json.dumps(sample_helper_config), encoding='utf-8')
    return helper_file


@pytest.fixture
def helper_yaml_file(tmp_path: Path) -> Path:
    """Create a temporary YAML helper file and return its path."""
    helper_file = tmp_path / 'helper.yaml'
    helper_file.write_text(
        '\n'.join([
            'base_url: https://example.com',
            'connection_type: legacy',
            'strict_mode: false',
            'verify_ssl: true',
            'connection:',
            '  legacy:',
            '    access_id: legacy-access-id',
            '    private_key_path: /tmp/',
            '    private_key_file: private.pem',
            '  oauth:',
            '    client_id: oauth-client-id',
        ]),
        encoding='utf-8',
    )
    return helper_file


@pytest.fixture
def mock_success_response() -> MockResponse:
    """Return a mocked successful API response object."""
    return MockResponse({'id': '54082ac6-4713-6368-2251-df813c41159f'})


@pytest.fixture
def mock_error_response() -> MockResponse:
    """Return a mocked failed API response object."""
    return MockResponse(
        {
            'code': '404 NOT_FOUND',
            'description': 'User john.doe@example.com not found',
        },
        status_code=404,
    )


def pytest_addoption(parser) -> None:
    """Add command-line options for test selection behavior."""
    parser.addoption(
        '--run-integration',
        action='store_true',
        default=False,
        help='Run tests marked as integration.',
    )


def pytest_collection_modifyitems(config, items) -> None:
    """Skip integration tests unless explicitly enabled with --run-integration."""
    if config.getoption('--run-integration'):
        return

    skip_integration = pytest.mark.skip(reason='integration tests are disabled by default (use --run-integration)')
    for item in items:
        if 'integration' in item.keywords:
            item.add_marker(skip_integration)
