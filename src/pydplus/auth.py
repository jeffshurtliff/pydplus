# -*- coding: utf-8 -*-
"""
:Module:            pydplus.auth
:Synopsis:          This module performs the authentication and authorization operations
:Usage:             ``from pydplus import auth``
:Example:           ``jwt_string = auth.get_legacy_jwt_string(base_url, connection_info)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     29 May 2025
"""

import datetime

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from . import errors
from .utils import core_utils, log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)

# Define constants
DEFAULT_CONNECTION_TYPE = 'oauth'
VALID_CONNECTION_TYPES = {'oauth', 'legacy'}
EMPTY_CONNECTION_INFO = {'legacy': {}, 'oauth': {}}
LEGACY_CONNECTION_FIELDS = {'access_id', 'private_key_path', 'private_key_file'}
OAUTH_CONNECTION_FIELDS = {'issuer_url', 'client_id', 'grant_type', 'client_authentication'}
STRUCTURED_CONNECTION_FIELDS = {'legacy': LEGACY_CONNECTION_FIELDS, 'oauth': OAUTH_CONNECTION_FIELDS}
OAUTH_GRANT_TYPE = 'Client Credentials'
OAUTH_CLIENT_AUTH = 'Private Key JWT'
LEGACY_KEY_ALGORITHM = 'RS256'


def get_legacy_jwt_string(base_url, connection_info):
    """This function retrieves the JWT string used for Legacy API connections.

    :param base_url: The base URL for the Cloud Administration API
    :type base_url: str
    :param connection_info: Dictionary containing the connection information for the tenant
    :type connection_info: dict
    :returns: The generated JWT string
    :raises: :py:exc:`TypeError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    # Extract needed data from connection_info dictionary
    access_id, private_key_full_path = _extract_legacy_connection_info(connection_info)

    # Define the JWT claims and load the private key
    jwt_claims = _define_jwt_claims(access_id, base_url)
    private_key = _load_private_key(private_key_full_path)

    # Construct and return the JWT string
    jwt_string = jwt.encode(
        payload=jwt_claims,
        key=private_key,
        algorithm=LEGACY_KEY_ALGORITHM
    )
    return jwt_string


def get_legacy_headers(jwt_string=None, base_url=None, connection_info=None):
    """This function constructs the headers to use in legacy API calls.

    .. versionadded:: 1.0.0

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
            error_msg = 'The base_url and connection_info parameters must be defined to connect to the tenant.'
            logger.error(error_msg)
            raise errors.exceptions.MissingRequiredDataError(error_msg)
        jwt_string = get_legacy_jwt_string(base_url, connection_info)
    headers = {
        "Authorization": f"Bearer {jwt_string}",
        "Content-Type": "application/json",
    }
    return headers


def _extract_legacy_connection_info(_connection_info):
    """This function extracts the needed legacy authentication data from the connection info dictionary.

    .. versionadded:: 1.0.0
    """
    # Extract the needed data
    _access_id = _connection_info['legacy'].get('access_id', '')
    _private_key_dir = _connection_info['legacy'].get('private_key_path', '')
    _private_key_file = _connection_info['legacy'].get('private_key_file', '')
    _private_key_full_path = f"{core_utils.ensure_ending_slash(_private_key_dir, 'file')}{_private_key_file}"

    # Raise an exception if the data is incomplete
    if not _access_id or not _private_key_file:
        _missing_var = 'access_id' if not _access_id else 'private_key_file'
        _error_msg = f'The {_missing_var} value is needed to connect to the tenant.'
        logger.error(_error_msg)
        raise errors.exceptions.MissingRequiredDataError(_error_msg)

    # Return the Access ID and private key full path
    return _access_id, _private_key_full_path


def _define_jwt_claims(_access_id, _base_url):
    """This function defines the JWT claims to use when generating the JWT string.

    .. versionadded:: 1.0.0
    """
    _claims_data = {
        "sub": _access_id,
        "iat": datetime.datetime.now(datetime.timezone.utc),     # This code supports Python 3.2+
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=3600),
        "aud": _base_url,
    }
    return _claims_data


def _load_private_key(_key_path):
    """This function loads the private key file for use in generating the JWT string.

    .. versionadded:: 1.0.0
    """
    if not core_utils.file_exists(_key_path):
        _error_msg = f"The file '{_key_path}' does not exist and cannot be used for the private key."
        logger.error(_error_msg)
        raise FileNotFoundError(_error_msg)
    with open(_key_path, 'rb') as _key_file:
        _private_key = serialization.load_pem_private_key(
            _key_file.read(),
            password=None,
            backend=default_backend()
        )
    return _private_key
