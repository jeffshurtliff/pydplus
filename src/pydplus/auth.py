# -*- coding: utf-8 -*-
"""
:Module:            pydplus.auth
:Synopsis:          This module performs the authentication and authorization operations
:Usage:             ``from pydplus import auth``
:Example:           ``jwt_string = auth.get_legacy_jwt_string(base_url, connection_info)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     28 Mar 2026
"""

from __future__ import annotations

import json
import logging
import datetime
from uuid import uuid4
from typing import Any, Optional, Union, Tuple

import jwt
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from . import constants as const
from . import errors
from .utils import core_utils

logger = logging.getLogger(__name__)


def get_legacy_jwt_string(base_url: str, connection_info: dict) -> str:
    """Retrieve the JWT string used for Legacy API connections.

    :param base_url: The base URL for the Cloud Administration API
    :type base_url: str
    :param connection_info: Dictionary containing the connection information for the tenant
    :type connection_info: dict
    :returns: The generated JWT string
    :raises: :py:exc:`TypeError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    access_id, private_key_full_path, private_key_pem = _extract_legacy_connection_info(connection_info)
    jwt_claims = _define_jwt_claims(access_id, base_url)
    private_key = _load_private_key(private_key_full_path, private_key_pem)
    jwt_string = jwt.encode(
        payload=jwt_claims,
        key=private_key,
        algorithm=const.AUTH_VALUES.LEGACY_KEY_ALGORITHM,
    )
    return jwt_string


def get_legacy_headers(
        jwt_string: Optional[str] = None,
        base_url: Optional[str] = None,
        connection_info: Optional[dict] = None,
) -> dict[str, str]:
    """Construct the headers to use in legacy API calls.

    :param jwt_string: The constructed JWT string to provide in the Authorization header
    :type jwt_string: str, None
    :param base_url: The base URL for the Cloud Administration API
    :type base_url: str, None
    :param connection_info: Dictionary containing the connection information for the tenant
    :type connection_info: dict, None
    :returns: The headers dictionary to utilize in legacy API calls
    :raises: :py:exc:`TypeError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    if not jwt_string:
        if not all((base_url, connection_info)):
            error_msg = 'The base_url and connection_info parameters must be defined to connect to the tenant'
            logger.error(error_msg)
            raise errors.exceptions.MissingRequiredDataError(error_msg)
        jwt_string = get_legacy_jwt_string(base_url, connection_info)
    headers = {
        const.HEADERS.AUTHORIZATION: const.AUTH_SCHEMES.BEARER.format(token=jwt_string),
        const.HEADERS.CONTENT_TYPE: const.CONTENT_TYPES.JSON,
    }
    return headers


def get_oauth_headers(
        connection_info: dict,
        verify_ssl: bool = const.DEFAULT_VERIFY_SSL,
        token_data: Optional[dict[str, Any]] = None,
        force_refresh: bool = const.AUTH_VALUES.OAUTH_DEFAULT_FORCE_REFRESH,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
) -> Tuple[dict[str, str], dict[str, Any]]:
    """Construct OAuth headers for Administration API calls.

    :param connection_info: Dictionary containing the connection information for the tenant
    :type connection_info: dict
    :param verify_ssl: Determines if SSL certificates should be verified during token requests (``True`` by default)
    :type verify_ssl: bool
    :param token_data: Existing OAuth token metadata to reuse when still valid
    :type token_data: dict, None
    :param force_refresh: Forces an access-token refresh and bypasses the token cache (``False`` by default)
    :type force_refresh: bool
    :param timeout: The timeout period in seconds to use for token endpoint requests (``30`` by default)
    :type timeout: int
    :returns: A tuple containing the headers dictionary and token metadata
    :raises: :py:exc:`TypeError`,
             :py:exc:`ValueError`,
             :py:exc:`errors.exceptions.APIConnectionError`,
             :py:exc:`errors.exceptions.FeatureNotConfiguredError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    token_data = get_oauth_access_token(
        connection_info=connection_info,
        verify_ssl=verify_ssl,
        token_data=token_data,
        force_refresh=force_refresh,
        timeout=timeout,
    )

    access_token = token_data.get(const.AUTH_FIELDS.OAUTH_ACCESS_TOKEN)
    token_type = token_data.get(const.AUTH_FIELDS.OAUTH_TOKEN_TYPE, const.AUTH_VALUES.OAUTH_TOKEN_TYPE_BEARER)
    if not isinstance(access_token, str) or not access_token:
        error_msg = f'The OAuth token response did not include a valid {const.AUTH_FIELDS.OAUTH_ACCESS_TOKEN}'
        logger.error(error_msg)
        raise errors.exceptions.APIConnectionError(error_msg)

    authorization_header_value = (
        const.AUTH_SCHEMES.BEARER.format(token=access_token)
        if token_type.lower() == const.AUTH_VALUES.OAUTH_TOKEN_TYPE_BEARER.lower()
        else f'{token_type} {access_token}'
    )
    headers = {
        const.HEADERS.AUTHORIZATION: authorization_header_value,
        const.HEADERS.CONTENT_TYPE: const.CONTENT_TYPES.JSON,
    }
    return headers, token_data


def get_oauth_access_token(
        connection_info: dict,
        verify_ssl: bool = const.DEFAULT_VERIFY_SSL,
        token_data: Optional[dict[str, Any]] = None,
        force_refresh: bool = const.AUTH_VALUES.OAUTH_DEFAULT_FORCE_REFRESH,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Retrieve an OAuth access token and associated metadata.

    :param connection_info: Dictionary containing the connection information for the tenant
    :type connection_info: dict
    :param verify_ssl: Determines if SSL certificates should be verified during token requests (``True`` by default)
    :type verify_ssl: bool
    :param token_data: Existing OAuth token metadata to reuse when still valid
    :type token_data: dict, None
    :param force_refresh: Forces an access-token refresh and bypasses the token cache (``False`` by default)
    :type force_refresh: bool
    :param timeout: The timeout period in seconds to use for token endpoint requests (``30`` by default)
    :type timeout: int
    :returns: OAuth token metadata containing token and expiration values
    :raises: :py:exc:`TypeError`,
             :py:exc:`ValueError`,
             :py:exc:`errors.exceptions.APIConnectionError`,
             :py:exc:`errors.exceptions.FeatureNotConfiguredError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    oauth_connection_info = _extract_oauth_connection_info(connection_info)
    requested_scope = oauth_connection_info[const.CONNECTION_INFO.OAUTH_SCOPE]

    if not force_refresh and _is_oauth_token_valid(token_data, _expected_scope=requested_scope):
        return token_data
    elif force_refresh:
        logger.debug('The OAuth access token is being force-refreshed')
    else:
        logger.debug('The OAuth access token is no longer valid and will be refreshed')

    return _request_oauth_access_token(
        oauth_connection_info=oauth_connection_info,
        verify_ssl=verify_ssl,
        timeout=timeout,
    )


def _extract_legacy_connection_info(_connection_info: dict) -> Tuple[str, Optional[str], Optional[str]]:
    """Extract the needed legacy authentication data from the connection info dictionary.

    :param _connection_info: The dictionary containing connection info from the client object
    :type _connection_info: dict
    :returns: The access ID, private key full path, and private key PEM in a tuple
    :raises: :py:exc:`TypeError`,
             :py:exc:`pydplus.errors.exceptions.MissingRequiredDataError`
    """
    _access_id = _connection_info[const.CONNECTION_INFO.LEGACY].get(const.CONNECTION_INFO.LEGACY_ACCESS_ID, '')
    _private_key_dir = _connection_info[const.CONNECTION_INFO.LEGACY].get(const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH, '')
    _private_key_file = _connection_info[const.CONNECTION_INFO.LEGACY].get(const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE, '')
    _private_key_pem = _connection_info[const.CONNECTION_INFO.LEGACY].get(const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PEM, '')
    _private_key_full_path = None
    if _private_key_file:
        _private_key_full_path = f"{core_utils.ensure_ending_slash(_private_key_dir, const.ARGUMENT_VALUES.FILE)}{_private_key_file}"

    if not _access_id or (not _private_key_file and not _private_key_pem):
        if not _access_id:
            _missing_var = const.CONNECTION_INFO.LEGACY_ACCESS_ID
        else:
            _missing_var = (f'{const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE} or '
                            f'{const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PEM}')
        _error_msg = f'The {_missing_var} value is needed to connect to the tenant'
        logger.error(_error_msg)
        raise errors.exceptions.MissingRequiredDataError(_error_msg)
    return _access_id, _private_key_full_path, _private_key_pem


def _extract_oauth_connection_info(_connection_info: dict) -> dict[str, Any]:
    """Extract and validate OAuth connection data from the ``connection_info`` dictionary."""
    _oauth_info = _connection_info.get(const.CONNECTION_INFO.OAUTH, {})
    if not isinstance(_oauth_info, dict):
        _error_msg = 'The OAuth connection info must be provided as a dictionary'
        logger.error(_error_msg)
        raise TypeError(_error_msg)

    issuer_url = _oauth_info.get(const.CONNECTION_INFO.OAUTH_ISSUER_URL)
    client_id = _oauth_info.get(const.CONNECTION_INFO.OAUTH_CLIENT_ID)
    scope = core_utils.normalize_oauth_scope(_oauth_info.get(const.CONNECTION_INFO.OAUTH_SCOPE), required=True)
    grant_type = _normalize_oauth_grant_type(_oauth_info.get(const.CONNECTION_INFO.OAUTH_GRANT_TYPE))
    client_auth = _normalize_oauth_client_auth(_oauth_info.get(const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION))

    if isinstance(issuer_url, str) and issuer_url:
        issuer_url = core_utils.remove_ending_slash(issuer_url)

    if not issuer_url or not client_id:
        missing_var = []
        if not issuer_url:
            missing_var.append(const.CONNECTION_INFO.OAUTH_ISSUER_URL)
        if not client_id:
            missing_var.append(const.CONNECTION_INFO.OAUTH_CLIENT_ID)
        _error_msg = f"The {' and '.join(missing_var)} value(s) are needed to connect to the tenant via OAuth"
        logger.error(_error_msg)
        raise errors.exceptions.MissingRequiredDataError(_error_msg)

    if grant_type != const.CONNECTION_INFO.OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS:
        _error_msg = (
            f"The OAuth {const.CONNECTION_INFO.OAUTH_GRANT_TYPE} '{grant_type}' is currently unsupported "
            f"(Only {const.CONNECTION_INFO.OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS} is currently supported)"
        )
        logger.error(_error_msg)
        raise errors.exceptions.FeatureNotConfiguredError(_error_msg)

    private_key_path = _oauth_info.get(const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_PATH)
    private_key_file = _oauth_info.get(const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_FILE)
    private_key_jwk = _oauth_info.get(const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK)

    if client_auth == const.CONNECTION_INFO.OAUTH_CLIENT_AUTH_PRIVATE_KEY_JWT:
        if not any((private_key_jwk, private_key_file)):
            _error_msg = (
                f"The '{const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK}' or "
                f"'{const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_FILE}' value is needed for Private Key JWT authentication"
            )
            logger.error(_error_msg)
            raise errors.exceptions.MissingRequiredDataError(_error_msg)
    else:
        _error_msg = (
            f"The OAuth client authentication method '{client_auth}' is currently unsupported "
            f"({const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH} is currently the only supported method)"
        )
        logger.error(_error_msg)
        raise errors.exceptions.FeatureNotConfiguredError(_error_msg)

    return {
        const.CONNECTION_INFO.OAUTH_ISSUER_URL: issuer_url,
        const.CONNECTION_INFO.OAUTH_CLIENT_ID: client_id,
        const.CONNECTION_INFO.OAUTH_SCOPE: scope,
        const.CONNECTION_INFO.OAUTH_GRANT_TYPE: grant_type,
        const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION: client_auth,
        const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_PATH: private_key_path,
        const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_FILE: private_key_file,
        const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK: private_key_jwk,
    }


def _define_jwt_claims(_access_id: str, _base_url: str) -> dict:
    """Define the JWT claims to use when generating the JWT string.

    :param _access_id: The access ID used for legacy authentication
    :type _access_id: str
    :param _base_url: The base URL for the ID Plus tenant
    :type _base_url: str
    :returns: Compiled JWT claims data in a dictionary
    """
    _lifespan = const.AUTH_VALUES.LEGACY_DEFAULT_EXPIRATION
    _claims_data = {
        const.AUTH_FIELDS.JWT_SUB: _access_id,
        const.AUTH_FIELDS.JWT_IAT: datetime.datetime.now(datetime.timezone.utc),
        const.AUTH_FIELDS.JWT_EXP: datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=_lifespan),
        const.AUTH_FIELDS.JWT_AUD: _base_url,
    }
    return _claims_data


def _load_private_key(_key_path: Optional[str] = None, _key_pem: Optional[str] = None) -> RSAPrivateKey:
    """Load the private key file for use in generating the JWT string.

    :param _key_path: The full path to the private key
    :type _key_path: str, None
    :param _key_pem: The private key in PEM format
    :type _key_pem: str, None
    :returns: The loaded private key data
    :raises: :py:exc:`FileNotFoundError`,
             :py:exc:`pydplus.errors.exceptions.MissingRequiredDataError`
    """
    if _key_pem:
        _private_key = serialization.load_pem_private_key(
            _key_pem.encode(const.UTF8_ENCODING),
            password=None,
            backend=default_backend()
        )
        return _private_key

    if not _key_path:
        _error_msg = 'A private key file path or private key PEM value must be defined'
        logger.error(_error_msg)
        raise errors.exceptions.MissingRequiredDataError(_error_msg)

    if not core_utils.file_exists(_key_path):
        _error_msg = f"The file '{_key_path}' does not exist and cannot be used for the private key"
        logger.error(_error_msg)
        raise FileNotFoundError(_error_msg)
    with open(_key_path, 'rb') as _key_file:
        _private_key = serialization.load_pem_private_key(
            _key_file.read(),
            password=None,
            backend=default_backend()
        )
    return _private_key


def _normalize_oauth_grant_type(_grant_type: Optional[str]) -> str:
    """Normalize the OAuth grant type to its canonical value."""
    if _grant_type is None:
        _grant_type = const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE
    if not isinstance(_grant_type, str):
        _error_msg = f'The OAuth {const.CONNECTION_INFO.OAUTH_GRANT_TYPE} must be a string (provided: {type(_grant_type)})'
        logger.error(_error_msg)
        raise TypeError(_error_msg)

    _raw_value = _grant_type.strip().lower()
    _lookup_values = {
        _raw_value,
        _raw_value.replace('-', '_'),
        _raw_value.replace('_', ' '),
        _raw_value.replace('-', ' '),
    }
    for _lookup in _lookup_values:
        if _lookup in const.CONNECTION_INFO.OAUTH_GRANT_TYPE_MAPPING:
            return const.CONNECTION_INFO.OAUTH_GRANT_TYPE_MAPPING[_lookup]

    _error_msg = (
        f"Unsupported OAuth {const.CONNECTION_INFO.OAUTH_GRANT_TYPE} value '{_grant_type}' "
        f"(Only {const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE} "
        f"({const.CONNECTION_INFO.OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS}) is currently supported)"
    )
    logger.error(_error_msg)
    raise errors.exceptions.FeatureNotConfiguredError(_error_msg)


def _normalize_oauth_client_auth(_client_auth: Optional[str]) -> str:
    """Normalize the OAuth client authentication value to its canonical form."""
    if _client_auth is None:
        _client_auth = const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH
    if not isinstance(_client_auth, str):
        _error_msg = (
            f'The OAuth {const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION} value must be a string '
            f'(provided: {type(_client_auth)})'
        )
        logger.error(_error_msg)
        raise TypeError(_error_msg)

    _raw_value = _client_auth.strip().lower()
    _lookup_values = {
        _raw_value,
        _raw_value.replace('-', '_'),
        _raw_value.replace('_', ' '),
        _raw_value.replace('-', ' '),
    }
    for _lookup in _lookup_values:
        if _lookup in const.CONNECTION_INFO.OAUTH_CLIENT_AUTH_MAPPING:
            return const.CONNECTION_INFO.OAUTH_CLIENT_AUTH_MAPPING[_lookup]

    _error_msg = f"Unsupported OAuth {const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION} value '{_client_auth}'"
    logger.error(_error_msg)
    raise errors.exceptions.FeatureNotConfiguredError(_error_msg)


def _resolve_oauth_private_key_path(_key_path: Optional[str], _key_file: str) -> str:
    """Resolve the full path to the OAuth private-key JWK file."""
    if not _key_path:
        return _key_file
    return f'{core_utils.ensure_ending_slash(_key_path, const.ARGUMENT_VALUES.FILE)}{_key_file}'


def _load_oauth_private_key_jwk(
        _key_path: Optional[str] = None,
        _key_file: Optional[str] = None,
        _key_jwk: Optional[Any] = None,
) -> dict[str, Any]:
    """Load and validate OAuth private key data represented as JWK."""
    _parsed_jwk: Optional[dict[str, Any]] = None

    if _key_jwk is not None:
        if isinstance(_key_jwk, dict):
            _parsed_jwk = dict(_key_jwk)
        elif isinstance(_key_jwk, str):
            if not _key_jwk.strip():
                _parsed_jwk = None
            else:
                try:
                    _parsed_jwk = json.loads(_key_jwk)
                except json.JSONDecodeError as _exc:
                    _error_msg = f'Failed to parse OAuth private key JWK string due to JSONDecodeError: {_exc}'
                    logger.error(_error_msg)
                    raise ValueError(_error_msg)
        else:
            _error_msg = (
                f'The {const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK} value must be a dict or JSON string '
                f'(provided: {type(_key_jwk)})'
            )
            logger.error(_error_msg)
            raise TypeError(_error_msg)

    if _parsed_jwk is None and _key_file:
        _full_key_path = _resolve_oauth_private_key_path(_key_path, _key_file)
        if not core_utils.file_exists(_full_key_path):
            _error_msg = f'The file {_full_key_path} does not exist and cannot be used for OAuth private-key JWK data'
            logger.error(_error_msg)
            raise FileNotFoundError(_error_msg)
        with open(_full_key_path, 'r', encoding=const.UTF8_ENCODING) as _jwk_file:
            _parsed_jwk = json.load(_jwk_file)

    if _parsed_jwk is None:
        _error_msg = (
            f'A {const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_FILE} or '
            f'{const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK} value must be defined for OAuth Private Key JWT'
        )
        logger.error(_error_msg)
        raise errors.exceptions.MissingRequiredDataError(_error_msg)

    if not isinstance(_parsed_jwk, dict):
        _error_msg = 'The OAuth private key JWK payload must be a dictionary'
        logger.error(_error_msg)
        raise TypeError(_error_msg)

    _kty_value = _parsed_jwk.get(const.AUTH_FIELDS.JWA_KEY_TYPE)
    if _kty_value == const.AUTH_VALUES.JWA_RSA:
        _required_fields = {
            const.AUTH_FIELDS.JWA_KEY_TYPE,                 # kty
            const.AUTH_FIELDS.JWA_RSA_MODULUS,              # n
            const.AUTH_FIELDS.JWA_RSA_EXPONENT,             # e
            const.AUTH_FIELDS.JWA_RSA_PRIVATE_EXPONENT,     # d
        }
    elif _kty_value == const.AUTH_VALUES.JWA_EC:
        _required_fields = {
            const.AUTH_FIELDS.JWA_KEY_TYPE,                 # kty
            const.AUTH_FIELDS.JWA_EC_CURVE,                 # crv
            const.AUTH_FIELDS.JWA_EC_X_COORDINATE,          # x
            const.AUTH_FIELDS.JWA_EC_Y_COORDINATE,          # y
            const.AUTH_FIELDS.JWA_EC_PRIVATE_KEY,           # d
        }
    else:
        _error_msg = (
            f"The OAuth private key JWK type '{_kty_value}' is unsupported "
            f"(Only {const.AUTH_VALUES.JWA_RSA} and {const.AUTH_VALUES.JWA_EC} key types are supported)"
        )
        logger.error(_error_msg)
        raise errors.exceptions.FeatureNotConfiguredError(_error_msg)

    _missing_fields = sorted(_required_fields.difference(_parsed_jwk.keys()))
    if _missing_fields:
        _error_msg = f"The OAuth private key JWK data is missing required field(s): {', '.join(_missing_fields)}"
        logger.error(_error_msg)
        raise errors.exceptions.MissingRequiredDataError(_error_msg)

    return _parsed_jwk


def _convert_oauth_jwk_to_signing_key(_private_key_jwk: dict[str, Any]):
    """Convert JWK key material to a signing key supported by PyJWT."""
    try:
        return jwt.PyJWK.from_dict(_private_key_jwk).key
    except Exception as _exc:
        _exc_type = core_utils.get_exception_type(_exc)
        _error_msg = f'Failed to parse OAuth private key JWK data due to {_exc_type} exception: {_exc}'
        logger.error(_error_msg)
        raise ValueError(_error_msg)


def _create_private_key_jwt_client_assertion(
        _client_id: str,
        _token_endpoint: str,
        _private_key_jwk: dict[str, Any],
) -> str:
    """Generate a signed private_key_jwt assertion string."""
    _signing_key = _convert_oauth_jwk_to_signing_key(_private_key_jwk)
    _now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    _jwt_claims = {
        const.AUTH_FIELDS.JWT_ISSUER: _client_id,
        const.AUTH_FIELDS.JWT_SUBJECT: _client_id,
        const.AUTH_FIELDS.JWT_AUDIENCE: _token_endpoint,
        const.AUTH_FIELDS.JWT_ISSUED_AT: _now,
        const.AUTH_FIELDS.JWT_EXPIRATION: _now + const.AUTH_VALUES._OAUTH_ASSERTION_LIFETIME_SECONDS,
        const.AUTH_FIELDS.JWT_ID: str(uuid4()),
    }

    _algorithm = _private_key_jwk.get(const.AUTH_FIELDS.JWK_ALGORITHM)
    if not _algorithm:
        _algorithm = (
            const.RSA_KEY_ALGORITHM                                                             # RS256
            if _private_key_jwk.get(const.AUTH_FIELDS.JWA_KEY_TYPE) == const.RSA_KEY_TYPE
            else const.EC_KEY_ALGORITHM                                                         # ES256
        )

    _headers = {}
    if _private_key_jwk.get(const.AUTH_FIELDS.JWK_KEY_ID):
        _headers[const.AUTH_FIELDS.JWK_KEY_ID] = _private_key_jwk[const.AUTH_FIELDS.JWK_KEY_ID]

    try:
        return jwt.encode(
            payload=_jwt_claims,
            key=_signing_key,
            algorithm=_algorithm,
            headers=_headers if _headers else None,
        )
    except Exception as _exc:
        _exc_type = core_utils.get_exception_type(_exc)
        _error_msg = f'Failed to generate private_key_jwt assertion due to {_exc_type} exception: {_exc}'
        logger.error(_error_msg)
        raise errors.exceptions.APIConnectionError(_error_msg)


def _get_oauth_token_endpoint(_issuer_url: str) -> str:
    """Return the OAuth token endpoint URL based on issuer URL."""
    _normalized_issuer = core_utils.remove_ending_slash(_issuer_url)
    return const.URLS.OAUTH_TOKEN.format(issuer_url=_normalized_issuer)


def _request_oauth_access_token(
        oauth_connection_info: dict[str, Any],
        verify_ssl: bool = const.DEFAULT_VERIFY_SSL,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Request an OAuth access token from the configured token endpoint."""
    _issuer_url = oauth_connection_info[const.CONNECTION_INFO.OAUTH_ISSUER_URL]
    _client_id = oauth_connection_info[const.CONNECTION_INFO.OAUTH_CLIENT_ID]
    _scope = oauth_connection_info[const.CONNECTION_INFO.OAUTH_SCOPE]
    _request_scope = ' '.join(_scope.split('+'))
    _grant_type = oauth_connection_info[const.CONNECTION_INFO.OAUTH_GRANT_TYPE]
    _client_auth = oauth_connection_info[const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION]
    _token_endpoint = _get_oauth_token_endpoint(_issuer_url)

    _request_data = {
        const.CONNECTION_INFO.OAUTH_GRANT_TYPE: _grant_type,
        const.CONNECTION_INFO.OAUTH_CLIENT_ID: _client_id,
        const.CONNECTION_INFO.OAUTH_SCOPE: _request_scope,
    }

    if _client_auth == const.CONNECTION_INFO.OAUTH_CLIENT_AUTH_PRIVATE_KEY_JWT:
        _private_key_jwk = _load_oauth_private_key_jwk(
            _key_path=oauth_connection_info.get(const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_PATH),
            _key_file=oauth_connection_info.get(const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_FILE),
            _key_jwk=oauth_connection_info.get(const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK),
        )
        _request_data.update({
            const.AUTH_FIELDS.OAUTH_CLIENT_ASSERTION_TYPE: const.AUTH_VALUES.OAUTH_CLIENT_ASSERT_TYPE_JWT_BEARER,
            const.AUTH_FIELDS.OAUTH_CLIENT_ASSERTION: _create_private_key_jwt_client_assertion(
                _client_id=_client_id,
                _token_endpoint=_token_endpoint,
                _private_key_jwk=_private_key_jwk,
            ),
        })
    else:
        _error_msg = (
            f"The OAuth {const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION} method '{_client_auth}' is currently "
            f"unsupported (Private Key JWT is currently the only supported method)"
        )
        logger.error(_error_msg)
        raise errors.exceptions.FeatureNotConfiguredError(_error_msg)

    _headers = {
        const.HEADERS.ACCEPT: const.CONTENT_TYPES.JSON,
        const.HEADERS.CONTENT_TYPE: const.CONTENT_TYPES.FORM_URLENCODED_UTF8,
    }
    _response = requests.post(
        _token_endpoint,
        headers=_headers,
        data=_request_data,
        timeout=timeout,
        verify=verify_ssl,
    )

    if _response.status_code >= 300:
        _error_msg = (
            f'The OAuth token request failed with a {_response.status_code} status code.\n{_response.text}'
        )
        logger.error(_error_msg)
        raise errors.exceptions.APIConnectionError(_error_msg)

    try:
        _response_data = _response.json()
    except Exception as _exc:
        _exc_type = core_utils.get_exception_type(_exc)
        _error_msg = f'Failed to parse OAuth token response due to {_exc_type} exception: {_exc}'
        logger.error(_error_msg)
        raise errors.exceptions.APIConnectionError(_error_msg)

    _token_data = _parse_oauth_token_response(_response_data)
    _token_data[const.AUTH_FIELDS.OAUTH_SCOPE] = _scope
    return _token_data


def _parse_oauth_token_response(_response_data: dict[str, Any]) -> dict[str, Any]:
    """Parse and validate an OAuth token endpoint response payload."""
    _access_token = _response_data.get(const.AUTH_FIELDS.OAUTH_ACCESS_TOKEN)
    if not isinstance(_access_token, str) or not _access_token:
        _error_msg = f'The OAuth token response did not include a valid {const.AUTH_FIELDS.OAUTH_ACCESS_TOKEN}'
        logger.error(_error_msg)
        raise errors.exceptions.APIConnectionError(_error_msg)

    _token_type = _response_data.get(const.AUTH_FIELDS.OAUTH_TOKEN_TYPE, const.AUTH_VALUES.OAUTH_TOKEN_TYPE_BEARER)
    if not isinstance(_token_type, str) or not _token_type:
        _token_type = const.AUTH_VALUES.OAUTH_TOKEN_TYPE_BEARER

    _expires_in = _response_data.get(const.AUTH_FIELDS.OAUTH_EXPIRES_IN, const.AUTH_VALUES.OAUTH_DEFAULT_TOKEN_EXPIRATION)
    if not isinstance(_expires_in, int):
        try:
            _expires_in = int(_expires_in)
        except (TypeError, ValueError):
            _expires_in = const.AUTH_VALUES.OAUTH_DEFAULT_TOKEN_EXPIRATION                              # 3600
    if _expires_in < 0:
        _expires_in = 0

    _now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    return {
        const.AUTH_FIELDS.OAUTH_ACCESS_TOKEN: _access_token,
        const.AUTH_FIELDS.OAUTH_TOKEN_TYPE: _token_type,
        const.AUTH_FIELDS.OAUTH_EXPIRES_IN: _expires_in,
        const.AUTH_FIELDS.OAUTH_EXPIRES_AT: _now + _expires_in,
    }


def _is_oauth_token_valid(
        _token_data: Optional[dict[str, Any]],
        _expected_scope: Optional[str] = None,
) -> bool:
    """Return whether cached OAuth token data is still valid."""
    if not _token_data:
        logger.debug('No OAauth token data was provided when checking if the token is valid')
        return False
    elif not isinstance(_token_data, dict):
        logger.error(f'The OAuth token data is an invalid type (Expected: dict, Provided: {type(_token_data)})')
        return False

    _access_token = _token_data.get(const.AUTH_FIELDS.OAUTH_ACCESS_TOKEN)
    _expires_at = _token_data.get(const.AUTH_FIELDS.OAUTH_EXPIRES_AT)
    _cached_scope = _token_data.get(const.AUTH_FIELDS.OAUTH_SCOPE)
    if not isinstance(_access_token, str) or not _access_token:
        logger.error('The OAuth access token is not a string or is missing')
        return False
    if not isinstance(_expires_at, (int, float)):
        _error_msg = f"The '{const.AUTH_FIELDS.OAUTH_EXPIRES_AT}' value is an invalid type "
        _error_msg += f"(Expected: int, float; Provided: {type(_expires_at)})"
        logger.error(_error_msg)
        return False
    if _expected_scope is not None and _cached_scope != _expected_scope:
        logger.error(f"The cached '{const.AUTH_FIELDS.OAUTH_SCOPE}' does not match the expected value")
        return False

    _now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    return _expires_at > (_now + const.AUTH_VALUES._OAUTH_TOKEN_EXPIRY_BUFFER_SECONDS)


def _get_scope_from_preset(
        _preset: Union[Optional[str], Optional[tuple], Optional[list], Optional[set], Optional[frozenset]] = None,
        _existing_scope: Union[Optional[str], Optional[tuple], Optional[list], Optional[set], Optional[frozenset]] = None,
) -> set[str]:
    """Retrieves one or more groupings of OAuth scope permissions based on presets."""
    _merged_scope: set[str] = set()
    _preset_mapping: dict[str, frozenset[str]] = {
        # All scopes (or all scopes for a given API)
        'all': const.OAUTH_SCOPES.ALL_SCOPES,
        'admin': const.OAUTH_SCOPES.ADMIN_API_SCOPES,
        'auth': const.OAUTH_SCOPES.AUTH_API_SCOPES,

        # Administration API scopes by type/category
        'agent': const.OAUTH_SCOPES.AGENT_SCOPES,
        'audit': const.OAUTH_SCOPES.AUDIT_SCOPES,
        'authenticator': const.OAUTH_SCOPES.AUTHENTICATOR_SCOPES,
        'fido': const.OAUTH_SCOPES.FIDO_CONFIGURATION_SCOPES,
        'group': const.OAUTH_SCOPES.GROUP_SCOPES,
        'report': const.OAUTH_SCOPES.REPORT_SCOPES,
        'user': const.OAUTH_SCOPES.USER_SCOPES,

        # Read-only scopes
        'all_read_only': const.OAUTH_SCOPES.ALL_READ_ONLY_PRESET,
        'agent_read_only': const.OAUTH_SCOPES.AGENT_READ_ONLY_PRESET,
        'authenticator_read_only': const.OAUTH_SCOPES.AUTHENTICATOR_READ_ONLY_PRESET,
        'fido_read_only': const.OAUTH_SCOPES.FIDO_READ_ONLY_PRESET,
        'group_read_only': const.OAUTH_SCOPES.GROUP_READ_ONLY_PRESET,
        'report_read_only': const.OAUTH_SCOPES.REPORT_READ_ONLY_PRESET,
        'user_read_only': const.OAUTH_SCOPES.USER_READ_ONLY_PRESET,

        # TODO: Add additional presets
    }

    if _existing_scope:
        if isinstance(_existing_scope, str):
            _existing_scope = set(_existing_scope.strip().replace(' ', '+').split('+'))
        _merged_scope.update(_existing_scope)

    if not _preset:
        logger.debug('No OAuth scope preset was provided')
        return _merged_scope

    _preset = {_preset} if isinstance(_preset, str) else _preset
    _added: list[str] = []
    _skipped: list[str] = []
    for _val in _preset:
        if _val.lower() in _preset_mapping:
            _merged_scope.update(_preset_mapping.get(_val.lower(), {}))
            _added.append(_val.lower())
        else:
            logger.warning(f"'{_val.lower()}' is not a valid OAuth scope preset and will be ignored")
            _skipped.append(_val.lower())

    _results_msg = (f"Processed {len(_preset)} OAuth scope presets "
                    f"(Added: {','.join(_added)}; Skipped: {','.join(_skipped)})")
    if _added or _skipped:
        logger.info(_results_msg)
    else:
        logger.debug(_results_msg)
    return _merged_scope
