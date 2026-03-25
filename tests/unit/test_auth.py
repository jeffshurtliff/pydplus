# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_auth
:Synopsis:          Unit tests for OAuth and legacy authentication helper functions
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     25 Mar 2026
"""

from __future__ import annotations

import datetime
import json

import pytest

from pydplus import auth, constants as const
from pydplus import errors


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


def _oauth_connection_info(scope: object = const.OAUTH_SCOPES.USER_READ) -> dict:
    """Return a reusable OAuth connection_info payload for tests."""
    oauth_connection = {
        const.CONNECTION_INFO.OAUTH: {
            const.CONNECTION_INFO.OAUTH_ISSUER_URL: 'https://example.com/oauth',
            const.CONNECTION_INFO.OAUTH_CLIENT_ID: 'oauth-client-id',
            const.CONNECTION_INFO.OAUTH_GRANT_TYPE: const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE,
            const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION: const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH,
            const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK: '{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}',
        },
    }
    if scope is not None:
        oauth_connection[const.CONNECTION_INFO.OAUTH][const.CONNECTION_INFO.OAUTH_SCOPE] = scope
    return oauth_connection


def test_get_oauth_access_token_reuses_valid_cached_token(monkeypatch) -> None:
    """Ensure valid cached OAuth token metadata is returned without token-endpoint calls."""
    now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    cached_token = {
        'access_token': 'cached-token',
        'token_type': 'Bearer',
        'expires_at': now + 600,
        'scope': const.OAUTH_SCOPES.USER_READ,
    }

    def _unexpected_post(*args, **kwargs):
        raise AssertionError('requests.post should not be called when cached token is valid')

    monkeypatch.setattr(auth.requests, 'post', _unexpected_post)

    token_data = auth.get_oauth_access_token(
        connection_info=_oauth_connection_info(),
        token_data=cached_token,
        force_refresh=False,
    )

    assert token_data is cached_token


def test_load_oauth_private_key_jwk_reads_json_file(tmp_path) -> None:
    """Ensure OAuth private-key JWK data can be loaded from a file path."""
    jwk_payload = {'kty': 'RSA', 'n': 'abc', 'e': 'AQAB', 'd': 'xyz'}
    jwk_file = tmp_path / 'oauth-private-key.jwk'
    jwk_file.write_text(json.dumps(jwk_payload), encoding='utf-8')

    parsed_jwk = auth._load_oauth_private_key_jwk(_key_file=jwk_file.name, _key_path=str(tmp_path))

    assert parsed_jwk == jwk_payload


def test_load_oauth_private_key_jwk_supports_ec_keys() -> None:
    """Ensure EC JWK payloads pass structural validation for OAuth private keys."""
    ec_jwk_payload = {
        'kty': 'EC',
        'crv': 'P-256',
        'x': 'abc',
        'y': 'def',
        'd': 'ghi',
    }

    parsed_jwk = auth._load_oauth_private_key_jwk(_key_jwk=ec_jwk_payload)

    assert parsed_jwk == ec_jwk_payload


def test_extract_oauth_connection_info_normalizes_grant_and_client_auth() -> None:
    """Ensure OAuth grant/client-auth values normalize to canonical forms."""
    connection_info = {
        const.CONNECTION_INFO.OAUTH: {
            const.CONNECTION_INFO.OAUTH_ISSUER_URL: 'https://example.com/oauth/',
            const.CONNECTION_INFO.OAUTH_CLIENT_ID: 'oauth-client-id',
            const.CONNECTION_INFO.OAUTH_SCOPE: f'{const.OAUTH_SCOPES.USER_READ}+{const.OAUTH_SCOPES.USER_READ}',
            const.CONNECTION_INFO.OAUTH_GRANT_TYPE: 'Client Credentials',
            const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION: 'Private Key JWT',
            const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK: '{"kty":"RSA","n":"abc","e":"AQAB","d":"xyz"}',
        }
    }

    parsed = auth._extract_oauth_connection_info(connection_info)

    assert parsed[const.CONNECTION_INFO.OAUTH_GRANT_TYPE] == const.CONNECTION_INFO.OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS
    assert parsed[const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION] == const.CONNECTION_INFO.OAUTH_CLIENT_AUTH_PRIVATE_KEY_JWT
    assert parsed[const.CONNECTION_INFO.OAUTH_ISSUER_URL] == 'https://example.com/oauth'
    assert parsed[const.CONNECTION_INFO.OAUTH_SCOPE] == const.OAUTH_SCOPES.USER_READ


def test_extract_oauth_connection_info_raises_when_scope_missing() -> None:
    """Ensure OAuth scope is required for token requests."""
    with pytest.raises(errors.exceptions.MissingRequiredDataError):
        auth._extract_oauth_connection_info(_oauth_connection_info(scope=None))


def test_extract_oauth_connection_info_raises_for_unknown_scope_values() -> None:
    """Ensure unknown scope values are rejected during OAuth connection parsing."""
    with pytest.raises(ValueError):
        auth._extract_oauth_connection_info(_oauth_connection_info(scope='rsa.unknown.scope'))


def test_get_oauth_access_token_posts_expected_private_key_jwt_payload(monkeypatch) -> None:
    """Ensure OAuth token requests include client assertion parameters for private_key_jwt auth."""
    observed_request = {}

    def _fake_load_oauth_private_key_jwk(**kwargs):
        return {'kty': 'RSA', 'n': 'abc', 'e': 'AQAB', 'd': 'xyz', 'kid': 'kid-123'}

    def _fake_assertion(**kwargs):
        return 'signed-client-assertion'

    def _fake_post(url, headers, data, timeout, verify):
        observed_request['url'] = url
        observed_request['headers'] = headers
        observed_request['data'] = data
        observed_request['timeout'] = timeout
        observed_request['verify'] = verify
        return DummyResponse(
            200,
            {
                'access_token': 'fresh-token',
                'token_type': 'Bearer',
                'expires_in': 3600,
            },
        )

    monkeypatch.setattr(auth, '_load_oauth_private_key_jwk', _fake_load_oauth_private_key_jwk)
    monkeypatch.setattr(auth, '_create_private_key_jwt_client_assertion', _fake_assertion)
    monkeypatch.setattr(auth.requests, 'post', _fake_post)

    token_data = auth.get_oauth_access_token(
        connection_info=_oauth_connection_info(),
        verify_ssl=False,
        timeout=17,
    )

    assert observed_request['url'] == 'https://example.com/oauth/token'
    assert observed_request['headers'][const.HEADERS.ACCEPT] == const.CONTENT_TYPES.JSON
    assert observed_request['data']['grant_type'] == const.CONNECTION_INFO.OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS
    assert observed_request['data']['client_id'] == 'oauth-client-id'
    assert observed_request['data']['scope'] == const.OAUTH_SCOPES.USER_READ
    assert observed_request['data']['client_assertion_type'] == 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    assert observed_request['data']['client_assertion'] == 'signed-client-assertion'
    assert observed_request['timeout'] == 17
    assert observed_request['verify'] is False
    assert token_data['access_token'] == 'fresh-token'
    assert token_data['scope'] == const.OAUTH_SCOPES.USER_READ


def test_get_oauth_headers_returns_bearer_authorization_header(monkeypatch) -> None:
    """Ensure OAuth headers include a bearer Authorization value."""
    monkeypatch.setattr(
        auth,
        'get_oauth_access_token',
        lambda **kwargs: {
            'access_token': 'abc123',
            'token_type': 'Bearer',
            'expires_at': 9999999999,
            'scope': const.OAUTH_SCOPES.USER_READ,
        },
    )

    headers, token_data = auth.get_oauth_headers(connection_info=_oauth_connection_info())

    assert headers[const.HEADERS.AUTHORIZATION] == 'Bearer abc123'
    assert headers[const.HEADERS.CONTENT_TYPE] == const.CONTENT_TYPES.JSON
    assert token_data['access_token'] == 'abc123'


def test_parse_oauth_token_response_raises_when_access_token_missing() -> None:
    """Ensure invalid OAuth token responses raise APIConnectionError."""
    with pytest.raises(errors.exceptions.APIConnectionError):
        auth._parse_oauth_token_response({'token_type': 'Bearer', 'expires_in': 3600})


def test_get_oauth_access_token_refreshes_when_cached_scope_differs(monkeypatch) -> None:
    """Ensure cached OAuth token metadata is not reused when scope values differ."""
    observed = {'called': False}
    now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    cached_token = {
        'access_token': 'cached-token',
        'token_type': 'Bearer',
        'expires_at': now + 600,
        'scope': const.OAUTH_SCOPES.USER_READ,
    }

    def _fake_request_oauth_access_token(**kwargs):
        observed['called'] = True
        return {
            'access_token': 'fresh-token',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'expires_at': now + 3600,
            'scope': kwargs['oauth_connection_info'][const.CONNECTION_INFO.OAUTH_SCOPE],
        }

    monkeypatch.setattr(auth, '_request_oauth_access_token', _fake_request_oauth_access_token)

    token_data = auth.get_oauth_access_token(
        connection_info=_oauth_connection_info(scope=const.OAUTH_SCOPES.USER_MANAGE),
        token_data=cached_token,
        force_refresh=False,
    )

    assert observed['called'] is True
    assert token_data['access_token'] == 'fresh-token'
    assert token_data['scope'] == const.OAUTH_SCOPES.USER_MANAGE
