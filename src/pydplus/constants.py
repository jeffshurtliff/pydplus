# -*- coding: utf-8 -*-
"""
:Module:            pydplus.constants
:Synopsis:          Constants that are utilized throughout the package
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Mar 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Final, ClassVar, Mapping, Union


# --------------------------------------
# Common Validation Criteria / Mapping
# --------------------------------------
YAML_BOOLEAN_MAPPING: Final[Mapping[Union[str, bool], bool]] = MappingProxyType({
    True: True,
    False: False,
    'yes': True,
    'no': False,
})


# -----------------------------
# Error Handling
# -----------------------------
_DEFAULT_WARNING_CATEGORY: Final[type[Warning]] = UserWarning


# -----------------------------
# Common Argument Values
# -----------------------------
@dataclass(frozen=True)
class ArgumentValues:
    """Common argument values leveraged throughout the package."""
    # Common values
    FILE: ClassVar[str] = 'file'
    URL: ClassVar[str] = 'url'

    # User status actions
    ENABLE: ClassVar[str] = 'enable'
    DISABLE: ClassVar[str] = 'disable'
    VALID_USER_STATUS_ACTIONS: ClassVar[frozenset[str]] = frozenset({
        ENABLE,
        DISABLE,
    })


# -----------------------------
# Exception Classes
# -----------------------------
@dataclass(frozen=True)
class ExceptionClasses:
    """Constants utilized by the exception classes in the :py:mod:`pydplus.errors.exceptions` module."""
    # Keyword arguments
    _DATA: ClassVar[str] = 'data'
    _FEATURE: ClassVar[str] = 'feature'
    _FIELD: ClassVar[str] = 'field'
    _FILE: ClassVar[str] = 'file'
    _IDENTIFIER: ClassVar[str] = 'identifier'
    _INIT: ClassVar[str] = 'init'
    _INITIALIZE: ClassVar[str] = 'initialize'
    _MESSAGE: ClassVar[str] = 'message'
    _OBJECT: ClassVar[str] = 'object'
    _PARAM: ClassVar[str] = 'param'
    _REQUEST_TYPE: ClassVar[str] = 'request_type'
    _STATUS_CODE: ClassVar[str] = 'status_code'
    _URL: ClassVar[str] = 'url'
    _VAL: ClassVar[str] = 'val'
    _VALUE: ClassVar[str] = 'value'

    # Exception messages and message segments
    _API_CUSTOM_MSG: ClassVar[str] = 'The {type} request failed with the following message:'
    _API_DEFAULT_MSG: ClassVar[str] = 'The {type} request did not return a successful response.'
    _CANNOT_LOCATE_FILE: ClassVar[str] = 'Unable to locate the following file: {file_path}'
    _INVALID_HELPER_DEFAULT_MSG: ClassVar[str] = "The helper configuration file can only have the 'yml', 'yaml' or 'json' file type."
    _WITH_THE_FOLLOWING_SEGMENT: ClassVar[str] = ' with the following'


# -----------------------------
# File Type Extensions
# -----------------------------
@dataclass(frozen=True)
class FileExtensions:
    """Common file extensions leveraged throughout the package."""
    # Without delimiter
    JPEG: ClassVar[str] = 'jpeg'
    JSON: ClassVar[str] = 'json'
    YAML: ClassVar[str] = 'yaml'
    YML: ClassVar[str] = 'yml'

    # With delimiter
    DOT_JPEG: ClassVar[str] = f'.{JPEG}'
    DOT_JSON: ClassVar[str] = f'.{JSON}'
    DOT_YAML: ClassVar[str] = f'.{YAML}'
    DOT_YML: ClassVar[str] = f'.{YML}'


# -------------------------------
# Client Configuration Settings
# -------------------------------
@dataclass(frozen=True)
class ClientSettings:
    """Fields, values, and other constants relating to the :py:class:`pydplus.PyDPlus`
    client configuration settings.
    """
    # Connection types
    CONNECTION_TYPE_LEGACY: ClassVar[str] = 'legacy'
    CONNECTION_TYPE_OAUTH: ClassVar[str] = 'oauth'


# -------------------------------
# Helper Configuration Settings
# -------------------------------
@dataclass(frozen=True)
class HelperSettings:
    """Fields, values, and other constants relating to the helper configuration settings and
       the :py:mod:`pydplus.utils.helper` module.

    .. note::
       If values are updated in this class for constants related to environment variables, then the
       corresponding values should be updated in the :py:class:`pydplus.constants.EnvVariables` class.
    """
    # Validation criteria
    VALID_HELPER_FILE_TYPES: ClassVar[frozenset[str]] = frozenset({'json', 'yml', 'yaml'})
    VALID_YAML_TRUE_VALUES: ClassVar[frozenset[str]] = frozenset({'yes', 'true'})

    # Root-level helper fields
    ENV_NAME: ClassVar[str] = 'env'
    BASE_URL: ClassVar[str] = 'base_url'
    CONNECTION: ClassVar[str] = 'connection'
    CONNECTION_TYPE: ClassVar[str] = 'connection_type'
    STRICT_MODE: ClassVar[str] = 'strict_mode'
    VERIFY_SSL: str = 'verify_ssl'
    ENV_VARIABLES: ClassVar[str] = 'env_variables'
    ROOT_LEVEL_BASIC_FIELDS: ClassVar[frozenset[str]] = frozenset({
        ENV_NAME,
        BASE_URL,
        CONNECTION_TYPE,
        STRICT_MODE,
        VERIFY_SSL,
    })

    # Environment variable fields
    ENV_CONNECTION_TYPE: ClassVar[str] = 'connection_type'
    ENV_LEGACY_ACCESS_ID: ClassVar[str] = 'legacy_access_id'
    ENV_LEGACY_KEY_PATH: ClassVar[str] = 'legacy_key_path'
    ENV_LEGACY_KEY_FILE: ClassVar[str] = 'legacy_key_file'
    ENV_OAUTH_ISSUER_URL: ClassVar[str] = 'oauth_issuer_url'
    ENV_OAUTH_CLIENT_ID: ClassVar[str] = 'oauth_client_id'
    ENV_OAUTH_GRANT_TYPE: ClassVar[str] = 'oauth_grant_type'
    ENV_OAUTH_CLIENT_AUTH: ClassVar[str] = 'oauth_client_authentication'
    ENV_STRICT_MODE: ClassVar[str] = 'strict_mode'
    ENV_VERIFY_SSL: ClassVar[str] = 'verify_ssl'

    # Environment variable default values
    ENV_DEFAULT_ENV_NAME: ClassVar[str] = 'PYDPLUS_ENV_NAME'
    ENV_DEFAULT_CONNECTION_TYPE: ClassVar[str] = 'PYDPLUS_CONNECTION_TYPE'
    ENV_DEFAULT_LEGACY_ACCESS_ID: ClassVar[str] = 'PYDPLUS_LEGACY_ACCESS_ID'
    ENV_DEFAULT_LEGACY_KEY_PATH: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_PATH'
    ENV_DEFAULT_LEGACY_KEY_FILE: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_FILE'
    ENV_DEFAULT_OAUTH_ISSUER_URL: ClassVar[str] = 'PYDPLUS_OAUTH_ISSUER_URL'
    ENV_DEFAULT_OAUTH_CLIENT_ID: ClassVar[str] = 'PYDPLUS_OAUTH_CLIENT_ID'
    ENV_DEFAULT_OAUTH_GRANT_TYPE: ClassVar[str] = 'PYDPLUS_OAUTH_GRANT_TYPE'
    ENV_DEFAULT_OAUTH_CLIENT_AUTH: ClassVar[str] = 'PYDPLUS_OAUTH_CLIENT_AUTH'
    ENV_DEFAULT_STRICT_MODE: ClassVar[str] = 'PYDPLUS_STRICT_MODE'
    ENV_DEFAULT_VERIFY_SSL: ClassVar[str] = 'PYDPLUS_VERIFY_SSL'

    # Environment variable default mapping
    ENV_VARIABLE_DEFAULT_MAPPING: ClassVar[Mapping[str, str]] = MappingProxyType({
        ENV_NAME: ENV_DEFAULT_ENV_NAME,
        ENV_CONNECTION_TYPE: ENV_DEFAULT_CONNECTION_TYPE,
        ENV_LEGACY_ACCESS_ID: ENV_DEFAULT_LEGACY_ACCESS_ID,
        ENV_LEGACY_KEY_PATH: ENV_DEFAULT_LEGACY_KEY_PATH,
        ENV_LEGACY_KEY_FILE: ENV_DEFAULT_LEGACY_KEY_FILE,
        ENV_OAUTH_ISSUER_URL: ENV_DEFAULT_OAUTH_ISSUER_URL,
        ENV_OAUTH_CLIENT_ID: ENV_DEFAULT_OAUTH_CLIENT_ID,
        ENV_OAUTH_GRANT_TYPE: ENV_DEFAULT_OAUTH_GRANT_TYPE,
        ENV_OAUTH_CLIENT_AUTH: ENV_DEFAULT_OAUTH_CLIENT_AUTH,
        ENV_STRICT_MODE: ENV_DEFAULT_STRICT_MODE,
        ENV_VERIFY_SSL: ENV_DEFAULT_VERIFY_SSL,
    })

    # Environment variable to connection field mappings
    ENV_LEGACY_CONNECTION_MAPPING: ClassVar[Mapping[str, str]] = MappingProxyType({
        'access_id': ENV_LEGACY_ACCESS_ID,
        'private_key_path': ENV_LEGACY_KEY_PATH,
        'private_key_file': ENV_LEGACY_KEY_FILE,
    })
    ENV_OAUTH_CONNECTION_MAPPING: ClassVar[Mapping[str, str]] = MappingProxyType({
        'issuer_url': ENV_OAUTH_ISSUER_URL,
        'client_id': ENV_OAUTH_CLIENT_ID,
        'grant_type': ENV_OAUTH_GRANT_TYPE,
        'client_authentication': ENV_OAUTH_CLIENT_AUTH,
    })

    # Other default values
    DEFAULT_ENV_NAME = None
    DEFAULT_HELPER_FILE_TYPE = 'json'
    DEFAULT_VERIFY_SSL_VALUE = True
    # DEFAULT_STRICT_MODE is defined at the module level


# -------------------------------
# Environment Variables
# -------------------------------
@dataclass(frozen=True)
class EnvVariables:
    """Constants relating to environment variable names.

    .. note::
       If values are updated in this class then the corresponding values should be updated
       in the :py:class:`pydplus.constants.HelperSettings` class.
    """
    # ----------------------------------
    # Standard Environment Variables
    # ----------------------------------
    # These environment variables are generic and used by default, and do not indicate a PROD or DEV environment.

    # Environment Information
    ENV_NAME: ClassVar[str] = 'PYDPLUS_ENV_NAME'

    # Tenant Information
    BASE_URL: ClassVar[str] = 'PYDPLUS_BASE_URL'

    # General Settings
    STRICT_MODE: ClassVar[str] = 'PYDPLUS_STRICT_MODE'
    VERIFY_SSL: ClassVar[str] = 'PYDPLUS_VERIFY_SSL'

    # Authentication / Connection
    CONNECTION_TYPE: ClassVar[str] = 'PYDPLUS_CONNECTION_TYPE'
    LEGACY_ACCESS_ID: ClassVar[str] = 'PYDPLUS_LEGACY_ACCESS_ID'
    LEGACY_KEY_PATH: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_PATH'
    LEGACY_KEY_FILE: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_FILE'
    OAUTH_ISSUER_URL: ClassVar[str] = 'PYDPLUS_OAUTH_ISSUER_URL'
    OAUTH_CLIENT_ID: ClassVar[str] = 'PYDPLUS_OAUTH_CLIENT_ID'
    OAUTH_GRANT_TYPE: ClassVar[str] = 'PYDPLUS_OAUTH_GRANT_TYPE'
    OAUTH_CLIENT_AUTH: ClassVar[str] = 'PYDPLUS_OAUTH_CLIENT_AUTH'

    # ------------------------------------
    # Production Environment Variables
    # ------------------------------------
    # These environment variables are specific to a Production (PROD) environment.

    # Tenant Information
    PROD_BASE_URL: ClassVar[str] = 'PYDPLUS_PROD_BASE_URL'

    # General Settings
    PROD_STRICT_MODE: ClassVar[str] = 'PYDPLUS_PROD_STRICT_MODE'
    PROD_VERIFY_SSL: ClassVar[str] = 'PYDPLUS_PROD_VERIFY_SSL'

    # Authentication / Connection
    PROD_CONNECTION_TYPE: ClassVar[str] = 'PYDPLUS_PROD_CONNECTION_TYPE'
    PROD_LEGACY_ACCESS_ID: ClassVar[str] = 'PYDPLUS_PROD_LEGACY_ACCESS_ID'
    PROD_LEGACY_KEY_PATH: ClassVar[str] = 'PYDPLUS_PROD_LEGACY_KEY_PATH'
    PROD_LEGACY_KEY_FILE: ClassVar[str] = 'PYDPLUS_PROD_LEGACY_KEY_FILE'
    PROD_OAUTH_ISSUER_URL: ClassVar[str] = 'PYDPLUS_PROD_OAUTH_ISSUER_URL'
    PROD_OAUTH_CLIENT_ID: ClassVar[str] = 'PYDPLUS_PROD_OAUTH_CLIENT_ID'
    PROD_OAUTH_GRANT_TYPE: ClassVar[str] = 'PYDPLUS_PROD_OAUTH_GRANT_TYPE'
    PROD_OAUTH_CLIENT_AUTH: ClassVar[str] = 'PYDPLUS_PROD_OAUTH_CLIENT_AUTH'

    # -------------------------------------
    # Development Environment Variables
    # -------------------------------------
    # These environment variables are specific to a Development (DEV) environment.

    # Tenant Information
    DEV_BASE_URL: ClassVar[str] = 'PYDPLUS_DEV_BASE_URL'

    # General Settings
    DEV_STRICT_MODE: ClassVar[str] = 'PYDPLUS_DEV_STRICT_MODE'
    DEV_VERIFY_SSL: ClassVar[str] = 'PYDPLUS_DEV_VERIFY_SSL'

    # Authentication / Connection
    DEV_CONNECTION_TYPE: ClassVar[str] = 'PYDPLUS_DEV_CONNECTION_TYPE'
    DEV_LEGACY_ACCESS_ID: ClassVar[str] = 'PYDPLUS_DEV_LEGACY_ACCESS_ID'
    DEV_LEGACY_KEY_PATH: ClassVar[str] = 'PYDPLUS_DEV_LEGACY_KEY_PATH'
    DEV_LEGACY_KEY_FILE: ClassVar[str] = 'PYDPLUS_DEV_LEGACY_KEY_FILE'
    DEV_OAUTH_ISSUER_URL: ClassVar[str] = 'PYDPLUS_DEV_OAUTH_ISSUER_URL'
    DEV_OAUTH_CLIENT_ID: ClassVar[str] = 'PYDPLUS_DEV_OAUTH_CLIENT_ID'
    DEV_OAUTH_GRANT_TYPE: ClassVar[str] = 'PYDPLUS_DEV_OAUTH_GRANT_TYPE'
    DEV_OAUTH_CLIENT_AUTH: ClassVar[str] = 'PYDPLUS_DEV_OAUTH_CLIENT_AUTH'

    # --------------------------------
    # Custom Environment Variables
    # --------------------------------
    # These environment variables are specific to a custom environment defined by the ENV_NAME variable.

    # Tenant Information
    CUSTOM_BASE_URL: ClassVar[str] = 'PYDPLUS_{env_name}_BASE_URL'                                  # Vars: env_name

    # General Settings
    CUSTOM_STRICT_MODE: ClassVar[str] = 'PYDPLUS_{env_name}_STRICT_MODE'                            # Vars: env_name
    CUSTOM_VERIFY_SSL: ClassVar[str] = 'PYDPLUS_{env_name}_VERIFY_SSL'                              # Vars: env_name

    # Authentication / Connection
    CUSTOM_CONNECTION_TYPE: ClassVar[str] = 'PYDPLUS_{env_name}_CONNECTION_TYPE'                    # Vars: env_name
    CUSTOM_LEGACY_ACCESS_ID: ClassVar[str] = 'PYDPLUS_{env_name}_LEGACY_ACCESS_ID'                  # Vars: env_name
    CUSTOM_LEGACY_KEY_PATH: ClassVar[str] = 'PYDPLUS_{env_name}_LEGACY_KEY_PATH'                    # Vars: env_name
    CUSTOM_LEGACY_KEY_FILE: ClassVar[str] = 'PYDPLUS_{env_name}_LEGACY_KEY_FILE'                    # Vars: env_name
    CUSTOM_OAUTH_ISSUER_URL: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_ISSUER_URL'                  # Vars: env_name
    CUSTOM_OAUTH_CLIENT_ID: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_CLIENT_ID'                    # Vars: env_name
    CUSTOM_OAUTH_GRANT_TYPE: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_GRANT_TYPE'                  # Vars: env_name
    CUSTOM_OAUTH_CLIENT_AUTH: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_CLIENT_AUTH'                # Vars: env_name

    # --------------------------------
    # Environment Variable Mapping
    # --------------------------------
    # Environment Fields
    DEFAULT_ENVIRONMENT: ClassVar[str] = 'DEFAULT'
    PROD_ENVIRONMENT: ClassVar[str] = 'PROD'
    DEV_ENVIRONMENT: ClassVar[str] = 'DEV'
    CUSTOM_ENVIRONMENT: ClassVar[str] = 'CUSTOM'

    # Mapping Fields
    ENV_FIELD: ClassVar[str] = 'env'
    BASE_URL_FIELD: ClassVar[str] = 'base_url'
    CONNECTION_TYPE_FIELD: ClassVar[str] = 'connection_type'
    LEGACY_ACCESS_ID_FIELD: ClassVar[str] = 'legacy_access_id'
    LEGACY_KEY_PATH_FIELD: ClassVar[str] = 'legacy_key_path'
    LEGACY_KEY_FILE_FIELD: ClassVar[str] = 'legacy_key_file'
    OAUTH_ISSUER_URL_FIELD: ClassVar[str] = 'oauth_issuer_url'
    OAUTH_CLIENT_ID_FIELD: ClassVar[str] = 'oauth_client_id'
    OAUTH_GRANT_TYPE_FIELD: ClassVar[str] = 'oauth_grant_type'
    OAUTH_CLIENT_AUTH_FIELD: ClassVar[str] = 'oauth_client_auth'
    STRICT_MODE_FIELD: ClassVar[str] = 'strict_mode'
    VERIFY_SSL_FIELD: ClassVar[str] = 'verify_ssl'

    # Environment mapping
    MAPPING: ClassVar[Mapping[str, Mapping[str, str]]] = MappingProxyType({
        DEFAULT_ENVIRONMENT: {
            ENV_FIELD: ENV_NAME,
            BASE_URL_FIELD: BASE_URL,
            CONNECTION_TYPE_FIELD: CONNECTION_TYPE,
            LEGACY_ACCESS_ID_FIELD: LEGACY_ACCESS_ID,
            LEGACY_KEY_PATH_FIELD: LEGACY_KEY_PATH,
            LEGACY_KEY_FILE_FIELD: LEGACY_KEY_FILE,
            OAUTH_ISSUER_URL_FIELD: OAUTH_ISSUER_URL,
            OAUTH_CLIENT_ID_FIELD: OAUTH_CLIENT_ID,
            OAUTH_GRANT_TYPE_FIELD: OAUTH_GRANT_TYPE,
            OAUTH_CLIENT_AUTH_FIELD: OAUTH_CLIENT_AUTH,
            STRICT_MODE_FIELD: STRICT_MODE,
            VERIFY_SSL_FIELD: VERIFY_SSL,
        },
        PROD_ENVIRONMENT: {
            BASE_URL_FIELD: PROD_BASE_URL,
            CONNECTION_TYPE_FIELD: PROD_CONNECTION_TYPE,
            LEGACY_ACCESS_ID_FIELD: PROD_LEGACY_ACCESS_ID,
            LEGACY_KEY_PATH_FIELD: PROD_LEGACY_KEY_PATH,
            LEGACY_KEY_FILE_FIELD: PROD_LEGACY_KEY_FILE,
            OAUTH_ISSUER_URL_FIELD: PROD_OAUTH_ISSUER_URL,
            OAUTH_CLIENT_ID_FIELD: PROD_OAUTH_CLIENT_ID,
            OAUTH_GRANT_TYPE_FIELD: PROD_OAUTH_GRANT_TYPE,
            OAUTH_CLIENT_AUTH_FIELD: PROD_OAUTH_CLIENT_AUTH,
            STRICT_MODE_FIELD: PROD_STRICT_MODE,
            VERIFY_SSL_FIELD: PROD_VERIFY_SSL,
        },
        DEV_ENVIRONMENT: {
            BASE_URL_FIELD: DEV_BASE_URL,
            CONNECTION_TYPE_FIELD: DEV_CONNECTION_TYPE,
            LEGACY_ACCESS_ID_FIELD: DEV_LEGACY_ACCESS_ID,
            LEGACY_KEY_PATH_FIELD: DEV_LEGACY_KEY_PATH,
            LEGACY_KEY_FILE_FIELD: DEV_LEGACY_KEY_FILE,
            OAUTH_ISSUER_URL_FIELD: DEV_OAUTH_ISSUER_URL,
            OAUTH_CLIENT_ID_FIELD: DEV_OAUTH_CLIENT_ID,
            OAUTH_GRANT_TYPE_FIELD: DEV_OAUTH_GRANT_TYPE,
            OAUTH_CLIENT_AUTH_FIELD: DEV_OAUTH_CLIENT_AUTH,
            STRICT_MODE_FIELD: DEV_STRICT_MODE,
            VERIFY_SSL_FIELD: DEV_VERIFY_SSL,
        },
        CUSTOM_ENVIRONMENT: {
            BASE_URL_FIELD: CUSTOM_BASE_URL,
            CONNECTION_TYPE_FIELD: CUSTOM_CONNECTION_TYPE,
            LEGACY_ACCESS_ID_FIELD: CUSTOM_LEGACY_ACCESS_ID,
            LEGACY_KEY_PATH_FIELD: CUSTOM_LEGACY_KEY_PATH,
            LEGACY_KEY_FILE_FIELD: CUSTOM_LEGACY_KEY_FILE,
            OAUTH_ISSUER_URL_FIELD: CUSTOM_OAUTH_ISSUER_URL,
            OAUTH_CLIENT_ID_FIELD: CUSTOM_OAUTH_CLIENT_ID,
            OAUTH_GRANT_TYPE_FIELD: CUSTOM_OAUTH_GRANT_TYPE,
            OAUTH_CLIENT_AUTH_FIELD: CUSTOM_OAUTH_CLIENT_AUTH,
            STRICT_MODE_FIELD: CUSTOM_STRICT_MODE,
            VERIFY_SSL_FIELD: CUSTOM_VERIFY_SSL,
        },
    })

    # --------------------------------------------
    # Environment Variable Validation Criteria
    # --------------------------------------------
    VALID_ENVIRONMENTS: ClassVar[frozenset[str]] = frozenset({
        DEFAULT_ENVIRONMENT,
        PROD_ENVIRONMENT,
        DEV_ENVIRONMENT,
        CUSTOM_ENVIRONMENT,
    })
    VALID_FIELDS: ClassVar[frozenset[str]] = frozenset({
        ENV_FIELD,
        BASE_URL_FIELD,
        CONNECTION_TYPE_FIELD,
        LEGACY_ACCESS_ID_FIELD,
        LEGACY_KEY_PATH_FIELD,
        LEGACY_KEY_FILE_FIELD,
        OAUTH_ISSUER_URL_FIELD,
        OAUTH_CLIENT_ID_FIELD,
        OAUTH_GRANT_TYPE_FIELD,
        OAUTH_CLIENT_AUTH_FIELD,
        STRICT_MODE_FIELD,
        VERIFY_SSL_FIELD,
    })


# -----------------------------
# API Connection Information
# -----------------------------
@dataclass(frozen=True)
class ConnectionInfo:
    """Fields, values, and other constants relating to the ``connection_info``
    dictionary within the client object and the :py:mod:`pydplus.utils.helper` module.
    """
    # Authentication/Connection type parent fields
    LEGACY: ClassVar[str] = 'legacy'
    OAUTH: ClassVar[str] = 'oauth'
    VALID_CONNECTION_TYPES: ClassVar[frozenset[str]] = frozenset({
        LEGACY,
        OAUTH,
    })
    DEFAULT_CONNECTION_TYPE: ClassVar[str] = OAUTH

    # Legacy authentication fields
    LEGACY_ACCESS_ID: ClassVar[str] = 'access_id'
    LEGACY_PRIVATE_KEY_FILE: ClassVar[str] = 'private_key_file'
    LEGACY_PRIVATE_KEY_PATH: ClassVar[str] = 'private_key_path'
    LEGACY_FIELDS: ClassVar[frozenset[str]] = frozenset({
        LEGACY_ACCESS_ID,
        LEGACY_PRIVATE_KEY_FILE,
        LEGACY_PRIVATE_KEY_PATH,
    })

    # OAuth authentication fields
    OAUTH_ISSUER_URL: ClassVar[str] = 'issuer_url'
    OAUTH_CLIENT_ID: ClassVar[str] = 'client_id'
    OAUTH_GRANT_TYPE: ClassVar[str] = 'grant_type'
    OAUTH_CLIENT_AUTHENTICATION: ClassVar[str] = 'client_authentication'
    OAUTH_FIELDS: ClassVar[frozenset[str]] = frozenset({
        OAUTH_ISSUER_URL,
        OAUTH_CLIENT_ID,
        OAUTH_GRANT_TYPE,
        OAUTH_CLIENT_AUTHENTICATION,
    })

    # OAuth default values
    OAUTH_DEFAULT_GRANT_TYPE: ClassVar[str] = 'Client Credentials'
    OAUTH_DEFAULT_CLIENT_AUTH: ClassVar[str] = 'Private Key JWT'

    # Connection fields
    EMPTY_CONNECTION_INFO: ClassVar[Mapping[str, Mapping[str, Any]]] = MappingProxyType({
        LEGACY: MappingProxyType({}),
        OAUTH: MappingProxyType({}),
    })
    CONNECTION_FIELDS: ClassVar[Mapping[str, frozenset[str]]] = MappingProxyType({
        LEGACY: LEGACY_FIELDS,
        OAUTH: OAUTH_FIELDS,
    })


# -----------------------------
# HTTP / Networking Defaults
# -----------------------------
# API types
ADMIN_API_TYPE: Final[str] = 'admin'
AUTH_API_TYPE: Final[str] = 'auth'

# Default values
DEFAULT_API_TIMEOUT_SECONDS: Final[int] = 30
DEFAULT_API_MAX_RETRIES: Final[int] = 3
DEFAULT_API_TYPE: Final[str] = ADMIN_API_TYPE
DEFAULT_STRICT_MODE: Final[bool] = False
DEFAULT_HEADER_TYPE: Final[str] = 'default'

# Validation criteria
VALID_API_TYPES: Final[frozenset[str]] = frozenset({
    ADMIN_API_TYPE,
    AUTH_API_TYPE,
})
VALID_HEADER_TYPES: Final[frozenset[str]] = frozenset({
    DEFAULT_HEADER_TYPE,
})


# -----------------------------
# API Authentication Fields
# -----------------------------
@dataclass(frozen=True)
class AuthFields:
    """Fields relating to API authentication."""
    # Authentication/Connection type parent fields
    LEGACY: ClassVar[str] = 'legacy'
    OAUTH: ClassVar[str] = 'oauth'

    # JWT Claims fields
    JWT_SUB: ClassVar[str] = 'sub'
    JWT_IAT: ClassVar[str] = 'iat'
    JWT_EXP: ClassVar[str] = 'exp'
    JWT_AUD: ClassVar[str] = 'aud'


# -----------------------------
# API Authentication Values
# -----------------------------
@dataclass(frozen=True)
class AuthValues:
    """Field/Parameter values relating to API authentication."""
    # Legacy default values
    LEGACY_KEY_ALGORITHM = 'RS256'

    # OAuth default values
    OAUTH_DEFAULT_GRANT_TYPE: ClassVar[str] = 'Client Credentials'
    OAUTH_DEFAULT_CLIENT_AUTH: ClassVar[str] = 'Private Key JWT'


# -----------------------------
# HTTP / REST API Request Types
# -----------------------------
@dataclass(frozen=True)
class ApiRequestTypes:
    """Standard REST API Request types used by the package."""
    GET: ClassVar[str] = 'GET'
    PATCH: ClassVar[str] = 'PATCH'
    POST: ClassVar[str] = 'POST'
    PUT: ClassVar[str] = 'PUT'
    DELETE: ClassVar[str] = 'DELETE'


# -----------------------------
# HTTP Header Fields / Names
# -----------------------------
@dataclass(frozen=True)
class Headers:
    """Standard HTTP header names used by the package.

    This immutable namespace centralizes common header keys to avoid
    magic strings throughout the codebase and to reduce the risk of
    typographical errors. These values are intended for constructing
    outbound HTTP requests to the RSA REST API.
    """
    AUTHORIZATION: ClassVar[str] = 'Authorization'
    CONTENT_TYPE: ClassVar[str] = 'Content-Type'
    ACCEPT: ClassVar[str] = 'Accept'
    ACCEPT_ENCODING: ClassVar[str] = 'Accept-Encoding'
    ACCEPT_LANGUAGE: ClassVar[str] = 'Accept-Language'


# -----------------------------
# HTTP Authentication Schemes
# -----------------------------
@dataclass(frozen=True)
class AuthSchemes:
    """Authentication schemes that are leveraged with the HTTP ``Authorization`` header.
       (`Reference <https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Authentication>`__)
    """
    BEARER: ClassVar[str] = 'Bearer {token}'


# -----------------------------
# HTTP Content Types
# -----------------------------
@dataclass(frozen=True)
class ContentTypes:
    """Common HTTP ``Content-Type`` header values used by the package.

    This immutable namespace provides canonical MIME types used when
    sending or receiving data from the RSA REST API.
    """
    JSON: ClassVar[str] = 'application/json'


# -----------------------------
# HTTP Encoding Types
# -----------------------------
@dataclass(frozen=True)
class EncodingTypes:
    """Common HTTP ``Accept-Encoding`` header values.
       (`Reference <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-Encoding>`__)
    """
    GZIP: ClassVar[str] = 'gzip'
    COMPRESS: ClassVar[str] = 'compress'
    DEFLATE: ClassVar[str] = 'deflate'
    BR: ClassVar[str] = 'br'
    ZSTD: ClassVar[str] = 'zstd'
    DCB: ClassVar[str] = 'dcb'
    DCZ: ClassVar[str] = 'dcz'
    IDENTITY: ClassVar[str] = 'identity'
    WILDCARD: ClassVar[str] = '*'
    Q: ClassVar[str] = ';q={weight}'


# -----------------------------
# HTTP Language Tags
# -----------------------------
@dataclass(frozen=True)
class Languages:
    """Common IETF language tags for use in the Accept-Language HTTP header.

    Additional valid IETF language tags may be supplied manually
    when constructing request headers.
    """
    EN_US: ClassVar[str] = 'en-US'
    EN_GB: ClassVar[str] = 'en-GB'
    FR_FR: ClassVar[str] = 'fr-FR'
    DE_DE: ClassVar[str] = 'de-DE'
    ES_ES: ClassVar[str] = 'es-ES'
    PT_BR: ClassVar[str] = 'pt-BR'
    JA_JP: ClassVar[str] = 'ja-JP'
    IT_IT: ClassVar[str] = 'it-IT'
    ZH_CN: ClassVar[str] = 'zh-CN'
    ZH_TW: ClassVar[str] = 'zh-TW'
    WILDCARD: ClassVar[str] = '*'
    Q: ClassVar[str] = ';q={weight}'


# -------------------------------
# Relevant URLs
# -------------------------------
@dataclass(frozen=True)
class Urls:
    """Common URLs leveraged throughout the package."""
    # General URLs
    OAUTH: ClassVar[str] = '{base_url}/oauth'                                                       # Vars: base_url


# -------------------------------
# REST API endpoint paths
# -------------------------------
@dataclass(frozen=True)
class RestPaths:
    """Template paths for RSA REST API endpoints.

    This immutable namespace centralizes commonly used REST endpoint
    templates to avoid duplicating hard-coded paths throughout the
    codebase. The templates are designed to be formatted with runtime
    values such as ``user_id``, ``timeout``, and so forth.
    """
    # General REST paths
    # TODO: Add constants here as needed

    # Users endpoint paths
    # TODO: Update the base URL to end in a slash for consistency
    USERS: ClassVar[str] = 'v1/users'
    USERS_LOOKUP: ClassVar[str] = USERS + '/lookup'
    USER_BY_ID: ClassVar[str] = USERS + '/{user_id}'                                            # Vars: user_id
    USER_MARK_DELETED: ClassVar[str] = USER_BY_ID + '/markDeleted'                              # Vars: user_id
    USER_STATUS: ClassVar[str] = USER_BY_ID + '/userStatus'                                     # Vars: user_id
    USER_SYNC: ClassVar[str] = USERS + '/sync'                                                  # Vars: user_id


# --------------------------------------
# REST API Query Parameters and values
# --------------------------------------
@dataclass(frozen=True)
class QueryParams:
    """Standard query and payload parameter names used in RSA ID Plus REST API requests.

    This immutable namespace provides canonical parameter keys for
    constructing query strings when interacting with the RSA ID Plus
    REST API. Centralizing these values helps prevent typographical
    errors and ensures consistent request construction.
    """
    # Common parameter names
    Q: ClassVar[str] = 'q'
    BODY: ClassVar[str] = 'body'
    EMAIL: ClassVar[str] = 'email'
    MARK_DELETED: ClassVar[str] = 'markDeleted'
    SEARCH_UNSYNCED: ClassVar[str] = 'searchUnsynched'
    USER_STATUS: ClassVar[str] = 'userStatus'


# -----------------------------
# REST API Payload Values
# -----------------------------
@dataclass(frozen=True)
class PayloadValues:
    """Standard and common payload values used in RSA ID Plus REST API requests."""
    # User status
    ENABLED: ClassVar[str] = 'Enabled'
    DISABLED: ClassVar[str] = 'Disabled'


# -----------------------------
# REST API Response Keys
# -----------------------------
@dataclass(frozen=True)
class ResponseKeys:
    """Standard and common keys / fields for RSA ID Plus REST API responses."""
    # Common keys / fields
    ID: ClassVar[str] = 'id'


# -----------------------------
# Log Messages
# -----------------------------
@dataclass(frozen=True)
class LogMessages:
    """Common log messages that are utilized in multiple locations throughout the package."""
    _INVALID_PARAM_VALUE_DEFAULT: ClassVar[str] = 'The {param} value is not valid and will default to {default}'
    _INVALID_PARAM_VALUE_IGNORE: ClassVar[str] = "The {param} value '{value}' is not valid and will be ignored"
    _MISSING_REQUIRED_DATA: ClassVar[str] = '{data} is missing and must be provided as it is required'
    _MUST_BE_PROVIDED_ERROR: ClassVar[str] = 'The {data} must be provided.'
    _PARAM_EXCEEDS_MAX_VALUE: ClassVar[str] = 'The {param} value exceeds the maximum and will default to {default}'


# -----------------------------
# Exported namespaces
# -----------------------------
# Common (Public)
ARGUMENT_VALUES: Final[ArgumentValues] = ArgumentValues()
FILE_EXTENSIONS: Final[FileExtensions] = FileExtensions()
URLS: Final[Urls] = Urls()

# Common (Private)
_EXCEPTION_CLASSES: Final[ExceptionClasses] = ExceptionClasses()
_LOG_MESSAGES: Final[LogMessages] = LogMessages()

# Client Settings
CLIENT_SETTINGS: Final[ClientSettings] = ClientSettings()

# Helper Utility
HELPER_SETTINGS: Final[HelperSettings] = HelperSettings()

# Environment Variables
ENV_VARIABLES: Final[EnvVariables] = EnvVariables()

# Connection Information (Client and Helper)
CONNECTION_INFO: Final[ConnectionInfo] = ConnectionInfo()

# HTTP / API
API_REQUEST_TYPES: Final[ApiRequestTypes] = ApiRequestTypes()
AUTH_FIELDS: Final[AuthFields] = AuthFields()
AUTH_SCHEMES: Final[AuthSchemes] = AuthSchemes()
AUTH_VALUES: Final[AuthValues] = AuthValues()
CONTENT_TYPES: Final[ContentTypes] = ContentTypes()
ENCODING_TYPES: Final[EncodingTypes] = EncodingTypes()
HEADERS: Final[Headers] = Headers()
LANGUAGES: Final[Languages] = Languages()
PAYLOAD_VALUES: Final[PayloadValues] = PayloadValues()
QUERY_PARAMS: Final[QueryParams] = QueryParams()
RESPONSE_KEYS: Final[ResponseKeys] = ResponseKeys()
REST_PATHS: Final[RestPaths] = RestPaths()
