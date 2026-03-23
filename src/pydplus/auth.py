# -*- coding: utf-8 -*-
"""
:Module:            pydplus.auth
:Synopsis:          This module performs the authentication and authorization operations
:Usage:             ``from pydplus import auth``
:Example:           ``jwt_string = auth.get_legacy_jwt_string(base_url, connection_info)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     22 Mar 2026
"""

from __future__ import annotations

import logging
import datetime
from typing import Optional, Tuple

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from . import errors
from . import constants as const
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
    # Extract needed data from connection_info dictionary
    access_id, private_key_full_path, private_key_pem = _extract_legacy_connection_info(connection_info)

    # Define the JWT claims and load the private key
    jwt_claims = _define_jwt_claims(access_id, base_url)
    private_key = _load_private_key(private_key_full_path, private_key_pem)

    # Construct and return the JWT string
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
            error_msg = 'The base_url and connection_info parameters must be defined to connect to the tenant.'
            logger.error(error_msg)
            raise errors.exceptions.MissingRequiredDataError(error_msg)
        jwt_string = get_legacy_jwt_string(base_url, connection_info)
    headers = {
        const.HEADERS.AUTHORIZATION: const.AUTH_SCHEMES.BEARER.format(token=jwt_string),
        const.HEADERS.CONTENT_TYPE: const.CONTENT_TYPES.JSON,
    }
    return headers


def _extract_legacy_connection_info(_connection_info: dict) -> Tuple[str, Optional[str], Optional[str]]:
    """Extract the needed legacy authentication data from the connection info dictionary.

    :param _connection_info: The dictionary containing connection info from the client object
    :type _connection_info: dict
    :returns: The access ID, private key full path, and private key PEM in a tuple
    :raises: :py:exc:`TypeError`,
             :py:exc:`pydplus.errors.exceptions.MissingRequiredDataError`
    """
    # Extract the needed data
    _access_id = _connection_info[const.CONNECTION_INFO.LEGACY].get(const.CONNECTION_INFO.LEGACY_ACCESS_ID, '')
    _private_key_dir = _connection_info[const.CONNECTION_INFO.LEGACY].get(const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH, '')
    _private_key_file = _connection_info[const.CONNECTION_INFO.LEGACY].get(const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE, '')
    _private_key_pem = _connection_info[const.CONNECTION_INFO.LEGACY].get(const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PEM, '')
    _private_key_full_path = None
    if _private_key_file:
        _private_key_full_path = f"{core_utils.ensure_ending_slash(_private_key_dir, const.ARGUMENT_VALUES.FILE)}{_private_key_file}"

    # Raise an exception if the data is incomplete
    if not _access_id or (not _private_key_file and not _private_key_pem):
        if not _access_id:
            _missing_var = const.CONNECTION_INFO.LEGACY_ACCESS_ID
        else:
            _missing_var = (f"{const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE} or "
                            f"{const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PEM}")
        _error_msg = f'The {_missing_var} value is needed to connect to the tenant.'
        logger.error(_error_msg)
        raise errors.exceptions.MissingRequiredDataError(_error_msg)

    # Return the Access ID, private key full path, and private key PEM
    return _access_id, _private_key_full_path, _private_key_pem


def _define_jwt_claims(_access_id: str, _base_url: str) -> dict:
    """Define the JWT claims to use when generating the JWT string.

    :param _access_id: The access ID used for legacy authentication
    :type _access_id: str
    :param _base_url: The base URL for the ID Plus tenant
    :type _base_url: str
    :returns: Compiled JWT claims data in a dictionary
    """
    _claims_data = {
        const.AUTH_FIELDS.JWT_SUB: _access_id,
        const.AUTH_FIELDS.JWT_IAT: datetime.datetime.now(datetime.timezone.utc),     # This code supports Python 3.2+
        const.AUTH_FIELDS.JWT_EXP: datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=3600),
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
        _error_msg = 'A private key file path or private key PEM value must be defined.'
        logger.error(_error_msg)
        raise errors.exceptions.MissingRequiredDataError(_error_msg)

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
