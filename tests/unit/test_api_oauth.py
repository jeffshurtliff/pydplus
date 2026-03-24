# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_api_oauth
:Synopsis:          Unit tests for OAuth token refresh and retry behavior in API helpers
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     23 Mar 2026
"""

from __future__ import annotations

import pytest

from pydplus import api, constants as const


pytestmark = pytest.mark.unit


class DummyResponse:
    """Simple stand-in for an HTTP response object."""

    def __init__(self, status_code: int, payload: dict, text: str = '') -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = text

    def json(self):
        """Return the configured JSON payload."""
        return self._payload


class MockOAuthClient:
    """Minimal pydplus-like object for API helper tests."""

    def __init__(self) -> None:
        self.strict_mode = True
        self.verify_ssl = True
        self.connection_type = const.CONNECTION_INFO.OAUTH
        self.admin_base_rest_url = 'https://example.com/AdminInterface/restapi'
        self.auth_base_rest_url = None
        self.base_headers = {
            const.HEADERS.AUTHORIZATION: 'Bearer original-token',
            const.HEADERS.CONTENT_TYPE: const.CONTENT_TYPES.JSON,
        }
        self.ensure_calls = 0
        self.refresh_calls = 0

    def _ensure_oauth_headers(self):
        """Simulate ensuring non-expired OAuth headers."""
        self.ensure_calls += 1
        self.base_headers = {
            const.HEADERS.AUTHORIZATION: 'Bearer ensured-token',
            const.HEADERS.CONTENT_TYPE: const.CONTENT_TYPES.JSON,
        }
        return dict(self.base_headers)

    def refresh_oauth_token(self):
        """Simulate forcing an OAuth token refresh."""
        self.refresh_calls += 1
        self.base_headers = {
            const.HEADERS.AUTHORIZATION: 'Bearer refreshed-token',
            const.HEADERS.CONTENT_TYPE: const.CONTENT_TYPES.JSON,
        }
        return dict(self.base_headers)


def test_get_retries_once_after_oauth_401(monkeypatch) -> None:
    """Ensure GET requests refresh OAuth token and retry exactly once on 401."""
    pydp_object = MockOAuthClient()
    request_auth_headers = []
    responses = [
        DummyResponse(401, {'error': 'invalid_token'}, text='unauthorized'),
        DummyResponse(200, {'ok': True}),
    ]

    def _fake_get(url, headers, params, timeout, verify):
        request_auth_headers.append(headers[const.HEADERS.AUTHORIZATION])
        return responses.pop(0)

    monkeypatch.setattr(api.requests, 'get', _fake_get)

    response = api.get(
        pydp_object,
        endpoint='v1/users',
        return_json=True,
    )

    assert response == {'ok': True}
    assert request_auth_headers == ['Bearer ensured-token', 'Bearer refreshed-token']
    assert pydp_object.ensure_calls == 1
    assert pydp_object.refresh_calls == 1


def test_post_retries_once_after_oauth_401(monkeypatch) -> None:
    """Ensure payload-based requests refresh OAuth token and retry exactly once on 401."""
    pydp_object = MockOAuthClient()
    request_auth_headers = []
    responses = [
        DummyResponse(401, {'error': 'invalid_token'}, text='unauthorized'),
        DummyResponse(200, {'created': True}),
    ]

    def _fake_post(url, json, headers, params, timeout, verify):
        request_auth_headers.append(headers[const.HEADERS.AUTHORIZATION])
        return responses.pop(0)

    monkeypatch.setattr(api.requests, 'post', _fake_post)

    response = api.post(
        pydp_object,
        endpoint='v1/users',
        payload={'name': 'test-user'},
        return_json=True,
    )

    assert response == {'created': True}
    assert request_auth_headers == ['Bearer ensured-token', 'Bearer refreshed-token']
    assert pydp_object.ensure_calls == 1
    assert pydp_object.refresh_calls == 1
