# -*- coding: utf-8 -*-
"""
:Module:            pydplus.constants
:Synopsis:          Constants that are utilized throughout the package
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     26 Mar 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Final, ClassVar, Mapping, Union


# --------------------------------------
# Common and Generic Values
# --------------------------------------
UTF8_ENCODING: Final[str] = 'utf-8'


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

    # Methods that settings are provided
    PROVIDED_METHODS: ClassVar[tuple] = (
        'passed argument',
        'helper settings',
        'environment variable',
    )

    # User status actions
    ENABLE: ClassVar[str] = 'enable'
    DISABLE: ClassVar[str] = 'disable'
    VALID_USER_STATUS_ACTIONS: ClassVar[frozenset[str]] = frozenset({
        ENABLE,
        DISABLE,
    })


# -------------------------------
# Credential Parsing / Security
# -------------------------------
@dataclass(frozen=True)
class CredentialValues:
    """Constants used by secure credential parsing and private-key persistence helpers."""
    JSON_FIELD_CUSTOMER_NAME: ClassVar[str] = 'customerName'
    JSON_FIELD_ACCESS_ID: ClassVar[str] = 'accessID'
    JSON_FIELD_ACCESS_KEY: ClassVar[str] = 'accessKey'
    JSON_FIELD_ADMIN_REST_API_URL: ClassVar[str] = 'adminRestApiUrl'
    JSON_FIELD_DESCRIPTION: ClassVar[str] = 'description'

    PEM_BEGIN_MARKER: ClassVar[str] = 'BEGIN RSA PRIVATE KEY'

    DEFAULT_CERT_HOME_DIR: ClassVar[str] = '.pydplus'
    DEFAULT_CERT_SUBDIR: ClassVar[str] = 'certs'
    DEFAULT_PEM_BASENAME: ClassVar[str] = 'idplus-legacy'
    DEFAULT_PEM_EXTENSION: ClassVar[str] = '.pem'
    DEFAULT_FILENAME_FALLBACK: ClassVar[str] = 'tenant'

    PRIVATE_DIR_MODE: ClassVar[int] = 0o700
    PRIVATE_FILE_MODE: ClassVar[int] = 0o600


# -----------------------------
# Log Messages
# -----------------------------
@dataclass(frozen=True)
class LogMessages:
    """Common log messages that are utilized in multiple locations throughout the package."""
    # Generic argument messages
    _INVALID_ARG_IGNORE: ClassVar[str] = 'The {arg} argument is invalid and will be ignored'                            # Vars: arg

    # Generic parameter value messages
    _INVALID_PARAM_VALUE_DEFAULT: ClassVar[str] = "The {param} value is not valid and will default to '{default}'"      # Vars: param, default
    _INVALID_PARAM_VALUE_IGNORE: ClassVar[str] = "The {param} value '{value}' is not valid and will be ignored"         # Vars: param, value
    _MUST_BE_DATA_TYPE_ERROR: ClassVar[str] = "The data type of the {param} parameter must be '{data_type}'"            # Vars: param, data_type
    _PARAM_EXCEEDS_MAX_VALUE: ClassVar[str] = 'The {param} value exceeds the maximum and will default to {default}'     # Vars: param, default

    # Generic data messages
    _MISSING_REQUIRED_DATA: ClassVar[str] = '{data} is missing and must be provided as it is required'                  # Vars: data
    _MUST_BE_PROVIDED_ERROR: ClassVar[str] = 'The {data} must be provided.'                                             # Vars: data

    # Client instantiation messages
    _CLIENT_SETTING_CONFIGURED: ClassVar[str] = "The {setting} setting was configured as '{value}' via {method}"        # Vars: setting, value, method
    _WILL_USE_DEFAULT_VALUE: ClassVar[str] = (                                                                          # Vars: setting, value
        "The {setting} setting was not defined and will use "
        "the default value '{value}'"
    )


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
    _API_CUSTOM_MSG: ClassVar[str] = 'The {type} request failed with the following message:'                            # Vars: type
    _API_DEFAULT_MSG: ClassVar[str] = 'The {type} request did not return a successful response.'                        # Vars: type
    _CANNOT_LOCATE_FILE: ClassVar[str] = 'Unable to locate the following file: {file_path}'                             # Vars: file_path
    _INVALID_HELPER_DEFAULT_MSG: ClassVar[str] = "The helper configuration file can only have the 'yml', 'yaml' or 'json' file type."
    _PRIVATE_KEY_ALREADY_EXISTS: ClassVar[str] = "The private key file already exists at '{final_path}'"                # Vars: final_path
    _VALUE_NEEDED_TO_CONNECT_OAUTH: ClassVar[str] = "The '{field}' value is needed to connect to the tenant via OAuth"  # Vars: field
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
    PEM: ClassVar[str] = 'pem'
    TMP: ClassVar[str] = 'tmp'
    YAML: ClassVar[str] = 'yaml'
    YML: ClassVar[str] = 'yml'

    # With delimiter
    DOT_JPEG: ClassVar[str] = f'.{JPEG}'
    DOT_JSON: ClassVar[str] = f'.{JSON}'
    DOT_PEM: ClassVar[str] = f'.{PEM}'
    DOT_TMP: ClassVar[str] = f'.{TMP}'
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
    # Client properties
    BASE_URL: ClassVar[str] = 'base_url'
    CONNECTION_INFO: ClassVar[str] = 'connection_info'
    CONNECTION_TYPE: ClassVar[str] = 'connection_type'
    OAUTH_API_TYPE: ClassVar[str] = 'oauth_api_type'
    STRICT_MODE: ClassVar[str] = 'strict_mode'
    VERIFY_SSL: ClassVar[str] = 'verify_ssl'

    # Connection types
    CONNECTION_TYPE_LEGACY: ClassVar[str] = 'legacy'
    CONNECTION_TYPE_OAUTH: ClassVar[str] = 'oauth'

    # Default values
    DEFAULT_AUTO_CONNECT_VALUE = True
    DEFAULT_VERIFY_SSL_VALUE = True


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
    VALID_YAML_FALSE_VALUES: ClassVar[frozenset[str]] = frozenset({'no', 'false'})

    # Root-level helper fields
    ENV_NAME: ClassVar[str] = 'env'
    TENANT_NAME: ClassVar[str] = 'tenant_name'
    BASE_URL: ClassVar[str] = 'base_url'
    BASE_URLS: ClassVar[str] = 'base_urls'
    CONNECTION: ClassVar[str] = 'connection'
    CONNECTION_TYPE: ClassVar[str] = 'connection_type'
    STRICT_MODE: ClassVar[str] = 'strict_mode'
    VERIFY_SSL: str = 'verify_ssl'
    ENV_VARIABLES: ClassVar[str] = 'env_variables'
    ROOT_LEVEL_BASIC_FIELDS: ClassVar[frozenset[str]] = frozenset({
        ENV_NAME,
        TENANT_NAME,
        BASE_URL,
        CONNECTION_TYPE,
        STRICT_MODE,
        VERIFY_SSL,
    })

    # Base URL fields
    ADMIN: ClassVar[str] = 'admin'
    ADMIN_BASE_URL: ClassVar[str] = 'admin_base_url'
    AUTH: ClassVar[str] = 'auth'
    AUTH_BASE_URL: ClassVar[str] = 'auth_base_url'
    API_BASE_URL: ClassVar[str] = '{type}_base_url'                                                 # Vars: type

    # Environment variable fields
    ENV_ENV_NAME: ClassVar[str] = 'env'
    ENV_TENANT_NAME: ClassVar[str] = 'tenant_name'
    ENV_BASE_URL: ClassVar[str] = 'base_url'
    ENV_ADMIN_BASE_URL: ClassVar[str] = 'admin_base_url'
    ENV_AUTH_BASE_URL: ClassVar[str] = 'auth_base_url'
    ENV_CONNECTION_TYPE: ClassVar[str] = 'connection_type'
    ENV_LEGACY_ACCESS_ID: ClassVar[str] = 'legacy_access_id'
    ENV_LEGACY_KEY_PATH: ClassVar[str] = 'legacy_key_path'
    ENV_LEGACY_KEY_FILE: ClassVar[str] = 'legacy_key_file'
    ENV_LEGACY_KEY_PEM: ClassVar[str] = 'legacy_key_pem'
    ENV_LEGACY_KEY_MATERIAL_PATH: ClassVar[str] = 'legacy_key_material_path'
    ENV_LEGACY_KEY_MATERIAL_FILE: ClassVar[str] = 'legacy_key_material_file'
    ENV_OAUTH_ISSUER_URL: ClassVar[str] = 'oauth_issuer_url'
    ENV_OAUTH_CLIENT_ID: ClassVar[str] = 'oauth_client_id'
    ENV_OAUTH_SCOPE: ClassVar[str] = 'oauth_scope'
    ENV_OAUTH_GRANT_TYPE: ClassVar[str] = 'oauth_grant_type'
    ENV_OAUTH_CLIENT_AUTH: ClassVar[str] = 'oauth_client_authentication'
    ENV_OAUTH_PRIVATE_KEY_PATH: ClassVar[str] = 'oauth_private_key_path'
    ENV_OAUTH_PRIVATE_KEY_FILE: ClassVar[str] = 'oauth_private_key_file'
    ENV_OAUTH_PRIVATE_KEY_JWK: ClassVar[str] = 'oauth_private_key_jwk'
    ENV_STRICT_MODE: ClassVar[str] = 'strict_mode'
    ENV_VERIFY_SSL: ClassVar[str] = 'verify_ssl'

    # Environment variable default values
    ENV_DEFAULT_ENV_NAME: ClassVar[str] = 'PYDPLUS_ENV_NAME'
    ENV_DEFAULT_TENANT_NAME: ClassVar[str] = 'PYDPLUS_TENANT_NAME'
    ENV_DEFAULT_BASE_URL: ClassVar[str] = 'PYDPLUS_BASE_URL'
    ENV_DEFAULT_ADMIN_BASE_URL: ClassVar[str] = 'PYDPLUS_ADMIN_BASE_URL'
    ENV_DEFAULT_AUTH_BASE_URL: ClassVar[str] = 'PYDPLUS_AUTH_BASE_URL'
    ENV_DEFAULT_CONNECTION_TYPE: ClassVar[str] = 'PYDPLUS_CONNECTION_TYPE'
    ENV_DEFAULT_LEGACY_ACCESS_ID: ClassVar[str] = 'PYDPLUS_LEGACY_ACCESS_ID'
    ENV_DEFAULT_LEGACY_KEY_PATH: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_PATH'
    ENV_DEFAULT_LEGACY_KEY_FILE: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_FILE'
    ENV_DEFAULT_LEGACY_KEY_PEM: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_PEM'
    ENV_DEFAULT_LEGACY_KEY_MATERIAL_PATH: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_MATERIAL_PATH'
    ENV_DEFAULT_LEGACY_KEY_MATERIAL_FILE: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_MATERIAL_FILE'
    ENV_DEFAULT_OAUTH_ISSUER_URL: ClassVar[str] = 'PYDPLUS_OAUTH_ISSUER_URL'
    ENV_DEFAULT_OAUTH_CLIENT_ID: ClassVar[str] = 'PYDPLUS_OAUTH_CLIENT_ID'
    ENV_DEFAULT_OAUTH_SCOPE: ClassVar[str] = 'PYDPLUS_OAUTH_SCOPE'
    ENV_DEFAULT_OAUTH_GRANT_TYPE: ClassVar[str] = 'PYDPLUS_OAUTH_GRANT_TYPE'
    ENV_DEFAULT_OAUTH_CLIENT_AUTH: ClassVar[str] = 'PYDPLUS_OAUTH_CLIENT_AUTH'
    ENV_DEFAULT_OAUTH_PRIVATE_KEY_PATH: ClassVar[str] = 'PYDPLUS_OAUTH_PRIVATE_KEY_PATH'
    ENV_DEFAULT_OAUTH_PRIVATE_KEY_FILE: ClassVar[str] = 'PYDPLUS_OAUTH_PRIVATE_KEY_FILE'
    ENV_DEFAULT_OAUTH_PRIVATE_KEY_JWK: ClassVar[str] = 'PYDPLUS_OAUTH_PRIVATE_KEY_JWK'
    ENV_DEFAULT_STRICT_MODE: ClassVar[str] = 'PYDPLUS_STRICT_MODE'
    ENV_DEFAULT_VERIFY_SSL: ClassVar[str] = 'PYDPLUS_VERIFY_SSL'

    # Environment variable default mapping
    ENV_VARIABLE_DEFAULT_MAPPING: ClassVar[Mapping[str, str]] = MappingProxyType({
        ENV_ENV_NAME: ENV_DEFAULT_ENV_NAME,
        ENV_TENANT_NAME: ENV_DEFAULT_TENANT_NAME,
        ENV_BASE_URL: ENV_DEFAULT_BASE_URL,
        ENV_ADMIN_BASE_URL: ENV_DEFAULT_ADMIN_BASE_URL,
        ENV_AUTH_BASE_URL: ENV_DEFAULT_AUTH_BASE_URL,
        ENV_CONNECTION_TYPE: ENV_DEFAULT_CONNECTION_TYPE,
        ENV_LEGACY_ACCESS_ID: ENV_DEFAULT_LEGACY_ACCESS_ID,
        ENV_LEGACY_KEY_PATH: ENV_DEFAULT_LEGACY_KEY_PATH,
        ENV_LEGACY_KEY_FILE: ENV_DEFAULT_LEGACY_KEY_FILE,
        ENV_LEGACY_KEY_PEM: ENV_DEFAULT_LEGACY_KEY_PEM,
        ENV_LEGACY_KEY_MATERIAL_PATH: ENV_DEFAULT_LEGACY_KEY_MATERIAL_PATH,
        ENV_LEGACY_KEY_MATERIAL_FILE: ENV_DEFAULT_LEGACY_KEY_MATERIAL_FILE,
        ENV_OAUTH_ISSUER_URL: ENV_DEFAULT_OAUTH_ISSUER_URL,
        ENV_OAUTH_CLIENT_ID: ENV_DEFAULT_OAUTH_CLIENT_ID,
        ENV_OAUTH_SCOPE: ENV_DEFAULT_OAUTH_SCOPE,
        ENV_OAUTH_GRANT_TYPE: ENV_DEFAULT_OAUTH_GRANT_TYPE,
        ENV_OAUTH_CLIENT_AUTH: ENV_DEFAULT_OAUTH_CLIENT_AUTH,
        ENV_OAUTH_PRIVATE_KEY_PATH: ENV_DEFAULT_OAUTH_PRIVATE_KEY_PATH,
        ENV_OAUTH_PRIVATE_KEY_FILE: ENV_DEFAULT_OAUTH_PRIVATE_KEY_FILE,
        ENV_OAUTH_PRIVATE_KEY_JWK: ENV_DEFAULT_OAUTH_PRIVATE_KEY_JWK,
        ENV_STRICT_MODE: ENV_DEFAULT_STRICT_MODE,
        ENV_VERIFY_SSL: ENV_DEFAULT_VERIFY_SSL,
    })

    # Environment variable to connection field mappings
    ENV_LEGACY_CONNECTION_MAPPING: ClassVar[Mapping[str, str]] = MappingProxyType({
        'access_id': ENV_LEGACY_ACCESS_ID,
        'private_key_path': ENV_LEGACY_KEY_PATH,
        'private_key_file': ENV_LEGACY_KEY_FILE,
        'private_key_pem': ENV_LEGACY_KEY_PEM,
        'private_key_material_path': ENV_LEGACY_KEY_MATERIAL_PATH,
        'private_key_material_file': ENV_LEGACY_KEY_MATERIAL_FILE,
    })
    ENV_OAUTH_CONNECTION_MAPPING: ClassVar[Mapping[str, str]] = MappingProxyType({
        'issuer_url': ENV_OAUTH_ISSUER_URL,
        'client_id': ENV_OAUTH_CLIENT_ID,
        'scope': ENV_OAUTH_SCOPE,
        'grant_type': ENV_OAUTH_GRANT_TYPE,
        'client_authentication': ENV_OAUTH_CLIENT_AUTH,
        'private_key_path': ENV_OAUTH_PRIVATE_KEY_PATH,
        'private_key_file': ENV_OAUTH_PRIVATE_KEY_FILE,
        'private_key_jwk': ENV_OAUTH_PRIVATE_KEY_JWK,
    })

    # Other default values
    DEFAULT_ENV_NAME = None
    DEFAULT_HELPER_FILE_TYPE = 'json'
    DEFAULT_VERIFY_SSL_VALUE = True
    # DEFAULT_STRICT_MODE is defined at the module level under the "HTTP / Networking Defaults" section


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
    # Environment Identifier Names
    # ----------------------------------
    DEFAULT_ENVIRONMENT: ClassVar[str] = 'DEFAULT'
    PROD_ENVIRONMENT: ClassVar[str] = 'PROD'
    DEV_ENVIRONMENT: ClassVar[str] = 'DEV'
    CUSTOM_ENVIRONMENT: ClassVar[str] = 'CUSTOM'

    # ----------------------------------
    # Standard Environment Variables
    # ----------------------------------
    # These environment variables are generic and used by default, and do not indicate a specific environment

    # Environment Information
    ENV_NAME: ClassVar[str] = 'PYDPLUS_ENV_NAME'

    # Tenant Information
    BASE_URL: ClassVar[str] = 'PYDPLUS_BASE_URL'
    ADMIN_BASE_URL: ClassVar[str] = 'PYDPLUS_ADMIN_BASE_URL'
    AUTH_BASE_URL: ClassVar[str] = 'PYDPLUS_AUTH_BASE_URL'

    # General Settings
    STRICT_MODE: ClassVar[str] = 'PYDPLUS_STRICT_MODE'
    VERIFY_SSL: ClassVar[str] = 'PYDPLUS_VERIFY_SSL'

    # Authentication / Connection
    CONNECTION_TYPE: ClassVar[str] = 'PYDPLUS_CONNECTION_TYPE'
    LEGACY_ACCESS_ID: ClassVar[str] = 'PYDPLUS_LEGACY_ACCESS_ID'
    LEGACY_KEY_PATH: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_PATH'
    LEGACY_KEY_FILE: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_FILE'
    LEGACY_KEY_PEM: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_PEM'
    LEGACY_KEY_MATERIAL_PATH: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_MATERIAL_PATH'
    LEGACY_KEY_MATERIAL_FILE: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_MATERIAL_FILE'
    OAUTH_ISSUER_URL: ClassVar[str] = 'PYDPLUS_OAUTH_ISSUER_URL'
    OAUTH_CLIENT_ID: ClassVar[str] = 'PYDPLUS_OAUTH_CLIENT_ID'
    OAUTH_SCOPE: ClassVar[str] = 'PYDPLUS_OAUTH_SCOPE'
    OAUTH_GRANT_TYPE: ClassVar[str] = 'PYDPLUS_OAUTH_GRANT_TYPE'
    OAUTH_CLIENT_AUTH: ClassVar[str] = 'PYDPLUS_OAUTH_CLIENT_AUTH'
    OAUTH_PRIVATE_KEY_PATH: ClassVar[str] = 'PYDPLUS_OAUTH_PRIVATE_KEY_PATH'
    OAUTH_PRIVATE_KEY_FILE: ClassVar[str] = 'PYDPLUS_OAUTH_PRIVATE_KEY_FILE'
    OAUTH_PRIVATE_KEY_JWK: ClassVar[str] = 'PYDPLUS_OAUTH_PRIVATE_KEY_JWK'

    # --------------------------------
    # Custom Environment Variables
    # --------------------------------
    # These environment variables are for a custom or otherwise specific environment defined by the env_name variable

    # Tenant Information
    CUSTOM_BASE_URL: ClassVar[str] = 'PYDPLUS_{env_name}_BASE_URL'                                  # Vars: env_name
    CUSTOM_ADMIN_BASE_URL: ClassVar[str] = 'PYDPLUS_{env_name}_ADMIN_BASE_URL'                      # Vars: env_name
    CUSTOM_AUTH_BASE_URL: ClassVar[str] = 'PYDPLUS_{env_name}_AUTH_BASE_URL'                        # Vars: env_name

    # General Settings
    CUSTOM_STRICT_MODE: ClassVar[str] = 'PYDPLUS_{env_name}_STRICT_MODE'                            # Vars: env_name
    CUSTOM_VERIFY_SSL: ClassVar[str] = 'PYDPLUS_{env_name}_VERIFY_SSL'                              # Vars: env_name

    # Authentication / Connection
    CUSTOM_CONNECTION_TYPE: ClassVar[str] = 'PYDPLUS_{env_name}_CONNECTION_TYPE'                    # Vars: env_name
    CUSTOM_LEGACY_ACCESS_ID: ClassVar[str] = 'PYDPLUS_{env_name}_LEGACY_ACCESS_ID'                  # Vars: env_name
    CUSTOM_LEGACY_KEY_PATH: ClassVar[str] = 'PYDPLUS_{env_name}_LEGACY_KEY_PATH'                    # Vars: env_name
    CUSTOM_LEGACY_KEY_FILE: ClassVar[str] = 'PYDPLUS_{env_name}_LEGACY_KEY_FILE'                    # Vars: env_name
    CUSTOM_LEGACY_KEY_PEM: ClassVar[str] = 'PYDPLUS_{env_name}_LEGACY_KEY_PEM'                      # Vars: env_name
    CUSTOM_LEGACY_KEY_MATERIAL_PATH: ClassVar[str] = 'PYDPLUS_{env_name}_LEGACY_KEY_MATERIAL_PATH'  # Vars: env_name
    CUSTOM_LEGACY_KEY_MATERIAL_FILE: ClassVar[str] = 'PYDPLUS_{env_name}_LEGACY_KEY_MATERIAL_FILE'  # Vars: env_name
    CUSTOM_OAUTH_ISSUER_URL: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_ISSUER_URL'                  # Vars: env_name
    CUSTOM_OAUTH_CLIENT_ID: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_CLIENT_ID'                    # Vars: env_name
    CUSTOM_OAUTH_SCOPE: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_SCOPE'                            # Vars: env_name
    CUSTOM_OAUTH_GRANT_TYPE: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_GRANT_TYPE'                  # Vars: env_name
    CUSTOM_OAUTH_CLIENT_AUTH: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_CLIENT_AUTH'                # Vars: env_name
    CUSTOM_OAUTH_PRIVATE_KEY_PATH: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_PRIVATE_KEY_PATH'      # Vars: env_name
    CUSTOM_OAUTH_PRIVATE_KEY_FILE: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_PRIVATE_KEY_FILE'      # Vars: env_name
    CUSTOM_OAUTH_PRIVATE_KEY_JWK: ClassVar[str] = 'PYDPLUS_{env_name}_OAUTH_PRIVATE_KEY_JWK'        # Vars: env_name

    # ------------------------------------
    # Production Environment Variables
    # ------------------------------------
    # These environment variables are specific to a Production (PROD) environment

    # Tenant Information
    PROD_BASE_URL: ClassVar[str] = CUSTOM_BASE_URL.format(env_name=PROD_ENVIRONMENT)
    PROD_ADMIN_BASE_URL: ClassVar[str] = CUSTOM_ADMIN_BASE_URL.format(env_name=PROD_ENVIRONMENT)
    PROD_AUTH_BASE_URL: ClassVar[str] = CUSTOM_AUTH_BASE_URL.format(env_name=PROD_ENVIRONMENT)

    # General Settings
    PROD_STRICT_MODE: ClassVar[str] = CUSTOM_STRICT_MODE.format(env_name=PROD_ENVIRONMENT)
    PROD_VERIFY_SSL: ClassVar[str] = CUSTOM_VERIFY_SSL.format(env_name=PROD_ENVIRONMENT)

    # Authentication / Connection
    PROD_CONNECTION_TYPE: ClassVar[str] = CONNECTION_TYPE.format(env_name=PROD_ENVIRONMENT)
    PROD_LEGACY_ACCESS_ID: ClassVar[str] = CUSTOM_LEGACY_ACCESS_ID.format(env_name=PROD_ENVIRONMENT)
    PROD_LEGACY_KEY_PATH: ClassVar[str] = CUSTOM_LEGACY_KEY_PATH.format(env_name=PROD_ENVIRONMENT)
    PROD_LEGACY_KEY_FILE: ClassVar[str] = CUSTOM_LEGACY_KEY_FILE.format(env_name=PROD_ENVIRONMENT)
    PROD_LEGACY_KEY_PEM: ClassVar[str] = CUSTOM_LEGACY_KEY_PEM.format(env_name=PROD_ENVIRONMENT)
    PROD_LEGACY_KEY_MATERIAL_PATH: ClassVar[str] = CUSTOM_LEGACY_KEY_MATERIAL_PATH.format(env_name=PROD_ENVIRONMENT)
    PROD_LEGACY_KEY_MATERIAL_FILE: ClassVar[str] = CUSTOM_LEGACY_KEY_MATERIAL_FILE.format(env_name=PROD_ENVIRONMENT)
    PROD_OAUTH_ISSUER_URL: ClassVar[str] = CUSTOM_OAUTH_ISSUER_URL.format(env_name=PROD_ENVIRONMENT)
    PROD_OAUTH_CLIENT_ID: ClassVar[str] = CUSTOM_OAUTH_CLIENT_ID.format(env_name=PROD_ENVIRONMENT)
    PROD_OAUTH_SCOPE: ClassVar[str] = CUSTOM_OAUTH_SCOPE.format(env_name=PROD_ENVIRONMENT)
    PROD_OAUTH_GRANT_TYPE: ClassVar[str] = CUSTOM_OAUTH_GRANT_TYPE.format(env_name=PROD_ENVIRONMENT)
    PROD_OAUTH_CLIENT_AUTH: ClassVar[str] = CUSTOM_OAUTH_CLIENT_AUTH.format(env_name=PROD_ENVIRONMENT)
    PROD_OAUTH_PRIVATE_KEY_PATH: ClassVar[str] = CUSTOM_OAUTH_PRIVATE_KEY_PATH.format(env_name=PROD_ENVIRONMENT)
    PROD_OAUTH_PRIVATE_KEY_FILE: ClassVar[str] = CUSTOM_OAUTH_PRIVATE_KEY_FILE.format(env_name=PROD_ENVIRONMENT)
    PROD_OAUTH_PRIVATE_KEY_JWK: ClassVar[str] = CUSTOM_OAUTH_PRIVATE_KEY_JWK.format(env_name=PROD_ENVIRONMENT)

    # -------------------------------------
    # Development Environment Variables
    # -------------------------------------
    # These environment variables are specific to a Development (DEV) environment

    # Tenant Information
    DEV_BASE_URL: ClassVar[str] = CUSTOM_BASE_URL.format(env_name=DEV_ENVIRONMENT)
    DEV_ADMIN_BASE_URL: ClassVar[str] = CUSTOM_ADMIN_BASE_URL.format(env_name=DEV_ENVIRONMENT)
    DEV_AUTH_BASE_URL: ClassVar[str] = CUSTOM_AUTH_BASE_URL.format(env_name=DEV_ENVIRONMENT)

    # General Settings
    DEV_STRICT_MODE: ClassVar[str] = CUSTOM_STRICT_MODE.format(env_name=DEV_ENVIRONMENT)
    DEV_VERIFY_SSL: ClassVar[str] = CUSTOM_VERIFY_SSL.format(env_name=DEV_ENVIRONMENT)

    # Authentication / Connection
    DEV_CONNECTION_TYPE: ClassVar[str] = CONNECTION_TYPE.format(env_name=DEV_ENVIRONMENT)
    DEV_LEGACY_ACCESS_ID: ClassVar[str] = CUSTOM_LEGACY_ACCESS_ID.format(env_name=DEV_ENVIRONMENT)
    DEV_LEGACY_KEY_PATH: ClassVar[str] = CUSTOM_LEGACY_KEY_PATH.format(env_name=DEV_ENVIRONMENT)
    DEV_LEGACY_KEY_FILE: ClassVar[str] = CUSTOM_LEGACY_KEY_FILE.format(env_name=DEV_ENVIRONMENT)
    DEV_LEGACY_KEY_PEM: ClassVar[str] = CUSTOM_LEGACY_KEY_PEM.format(env_name=DEV_ENVIRONMENT)
    DEV_LEGACY_KEY_MATERIAL_PATH: ClassVar[str] = CUSTOM_LEGACY_KEY_MATERIAL_PATH.format(env_name=DEV_ENVIRONMENT)
    DEV_LEGACY_KEY_MATERIAL_FILE: ClassVar[str] = CUSTOM_LEGACY_KEY_MATERIAL_FILE.format(env_name=DEV_ENVIRONMENT)
    DEV_OAUTH_ISSUER_URL: ClassVar[str] = CUSTOM_OAUTH_ISSUER_URL.format(env_name=DEV_ENVIRONMENT)
    DEV_OAUTH_CLIENT_ID: ClassVar[str] = CUSTOM_OAUTH_CLIENT_ID.format(env_name=DEV_ENVIRONMENT)
    DEV_OAUTH_SCOPE: ClassVar[str] = CUSTOM_OAUTH_SCOPE.format(env_name=DEV_ENVIRONMENT)
    DEV_OAUTH_GRANT_TYPE: ClassVar[str] = CUSTOM_OAUTH_GRANT_TYPE.format(env_name=DEV_ENVIRONMENT)
    DEV_OAUTH_CLIENT_AUTH: ClassVar[str] = CUSTOM_OAUTH_CLIENT_AUTH.format(env_name=DEV_ENVIRONMENT)
    DEV_OAUTH_PRIVATE_KEY_PATH: ClassVar[str] = CUSTOM_OAUTH_PRIVATE_KEY_PATH.format(env_name=DEV_ENVIRONMENT)
    DEV_OAUTH_PRIVATE_KEY_FILE: ClassVar[str] = CUSTOM_OAUTH_PRIVATE_KEY_FILE.format(env_name=DEV_ENVIRONMENT)
    DEV_OAUTH_PRIVATE_KEY_JWK: ClassVar[str] = CUSTOM_OAUTH_PRIVATE_KEY_JWK.format(env_name=DEV_ENVIRONMENT)

    # --------------------------------
    # Environment Variable Mapping
    # --------------------------------
    # Mapping Fields
    ENV_FIELD: ClassVar[str] = 'env'
    BASE_URL_FIELD: ClassVar[str] = 'base_url'
    ADMIN_BASE_URL_FIELD: ClassVar[str] = 'admin_base_url'
    AUTH_BASE_URL_FIELD: ClassVar[str] = 'auth_base_url'
    CONNECTION_TYPE_FIELD: ClassVar[str] = 'connection_type'
    LEGACY_ACCESS_ID_FIELD: ClassVar[str] = 'legacy_access_id'
    LEGACY_KEY_PATH_FIELD: ClassVar[str] = 'legacy_key_path'
    LEGACY_KEY_FILE_FIELD: ClassVar[str] = 'legacy_key_file'
    LEGACY_KEY_PEM_FIELD: ClassVar[str] = 'legacy_key_pem'
    LEGACY_KEY_MATERIAL_PATH_FIELD: ClassVar[str] = 'legacy_key_material_path'
    LEGACY_KEY_MATERIAL_FILE_FIELD: ClassVar[str] = 'legacy_key_material_file'
    OAUTH_ISSUER_URL_FIELD: ClassVar[str] = 'oauth_issuer_url'
    OAUTH_CLIENT_ID_FIELD: ClassVar[str] = 'oauth_client_id'
    OAUTH_SCOPE_FIELD: ClassVar[str] = 'oauth_scope'
    OAUTH_GRANT_TYPE_FIELD: ClassVar[str] = 'oauth_grant_type'
    OAUTH_CLIENT_AUTH_FIELD: ClassVar[str] = 'oauth_client_authentication'
    OAUTH_PRIVATE_KEY_PATH_FIELD: ClassVar[str] = 'oauth_private_key_path'
    OAUTH_PRIVATE_KEY_FILE_FIELD: ClassVar[str] = 'oauth_private_key_file'
    OAUTH_PRIVATE_KEY_JWK_FIELD: ClassVar[str] = 'oauth_private_key_jwk'
    STRICT_MODE_FIELD: ClassVar[str] = 'strict_mode'
    VERIFY_SSL_FIELD: ClassVar[str] = 'verify_ssl'

    # Environment mapping
    MAPPING: ClassVar[Mapping[str, Mapping[str, str]]] = MappingProxyType({
        DEFAULT_ENVIRONMENT: {
            ENV_FIELD: ENV_NAME,
            BASE_URL_FIELD: BASE_URL,
            ADMIN_BASE_URL_FIELD: ADMIN_BASE_URL,
            AUTH_BASE_URL_FIELD: AUTH_BASE_URL,
            CONNECTION_TYPE_FIELD: CONNECTION_TYPE,
            LEGACY_ACCESS_ID_FIELD: LEGACY_ACCESS_ID,
            LEGACY_KEY_PATH_FIELD: LEGACY_KEY_PATH,
            LEGACY_KEY_FILE_FIELD: LEGACY_KEY_FILE,
            LEGACY_KEY_PEM_FIELD: LEGACY_KEY_PEM,
            LEGACY_KEY_MATERIAL_PATH_FIELD: LEGACY_KEY_MATERIAL_PATH,
            LEGACY_KEY_MATERIAL_FILE_FIELD: LEGACY_KEY_MATERIAL_FILE,
            OAUTH_ISSUER_URL_FIELD: OAUTH_ISSUER_URL,
            OAUTH_CLIENT_ID_FIELD: OAUTH_CLIENT_ID,
            OAUTH_SCOPE_FIELD: OAUTH_SCOPE,
            OAUTH_GRANT_TYPE_FIELD: OAUTH_GRANT_TYPE,
            OAUTH_CLIENT_AUTH_FIELD: OAUTH_CLIENT_AUTH,
            OAUTH_PRIVATE_KEY_PATH_FIELD: OAUTH_PRIVATE_KEY_PATH,
            OAUTH_PRIVATE_KEY_FILE_FIELD: OAUTH_PRIVATE_KEY_FILE,
            OAUTH_PRIVATE_KEY_JWK_FIELD: OAUTH_PRIVATE_KEY_JWK,
            STRICT_MODE_FIELD: STRICT_MODE,
            VERIFY_SSL_FIELD: VERIFY_SSL,
        },
        PROD_ENVIRONMENT: {
            BASE_URL_FIELD: PROD_BASE_URL,
            ADMIN_BASE_URL_FIELD: PROD_ADMIN_BASE_URL,
            AUTH_BASE_URL_FIELD: PROD_AUTH_BASE_URL,
            CONNECTION_TYPE_FIELD: PROD_CONNECTION_TYPE,
            LEGACY_ACCESS_ID_FIELD: PROD_LEGACY_ACCESS_ID,
            LEGACY_KEY_PATH_FIELD: PROD_LEGACY_KEY_PATH,
            LEGACY_KEY_FILE_FIELD: PROD_LEGACY_KEY_FILE,
            LEGACY_KEY_PEM_FIELD: PROD_LEGACY_KEY_PEM,
            LEGACY_KEY_MATERIAL_PATH_FIELD: PROD_LEGACY_KEY_MATERIAL_PATH,
            LEGACY_KEY_MATERIAL_FILE_FIELD: PROD_LEGACY_KEY_MATERIAL_FILE,
            OAUTH_ISSUER_URL_FIELD: PROD_OAUTH_ISSUER_URL,
            OAUTH_CLIENT_ID_FIELD: PROD_OAUTH_CLIENT_ID,
            OAUTH_SCOPE_FIELD: PROD_OAUTH_SCOPE,
            OAUTH_GRANT_TYPE_FIELD: PROD_OAUTH_GRANT_TYPE,
            OAUTH_CLIENT_AUTH_FIELD: PROD_OAUTH_CLIENT_AUTH,
            OAUTH_PRIVATE_KEY_PATH_FIELD: PROD_OAUTH_PRIVATE_KEY_PATH,
            OAUTH_PRIVATE_KEY_FILE_FIELD: PROD_OAUTH_PRIVATE_KEY_FILE,
            OAUTH_PRIVATE_KEY_JWK_FIELD: PROD_OAUTH_PRIVATE_KEY_JWK,
            STRICT_MODE_FIELD: PROD_STRICT_MODE,
            VERIFY_SSL_FIELD: PROD_VERIFY_SSL,
        },
        DEV_ENVIRONMENT: {
            BASE_URL_FIELD: DEV_BASE_URL,
            ADMIN_BASE_URL_FIELD: DEV_ADMIN_BASE_URL,
            AUTH_BASE_URL_FIELD: DEV_AUTH_BASE_URL,
            CONNECTION_TYPE_FIELD: DEV_CONNECTION_TYPE,
            LEGACY_ACCESS_ID_FIELD: DEV_LEGACY_ACCESS_ID,
            LEGACY_KEY_PATH_FIELD: DEV_LEGACY_KEY_PATH,
            LEGACY_KEY_FILE_FIELD: DEV_LEGACY_KEY_FILE,
            LEGACY_KEY_PEM_FIELD: DEV_LEGACY_KEY_PEM,
            LEGACY_KEY_MATERIAL_PATH_FIELD: DEV_LEGACY_KEY_MATERIAL_PATH,
            LEGACY_KEY_MATERIAL_FILE_FIELD: DEV_LEGACY_KEY_MATERIAL_FILE,
            OAUTH_ISSUER_URL_FIELD: DEV_OAUTH_ISSUER_URL,
            OAUTH_CLIENT_ID_FIELD: DEV_OAUTH_CLIENT_ID,
            OAUTH_SCOPE_FIELD: DEV_OAUTH_SCOPE,
            OAUTH_GRANT_TYPE_FIELD: DEV_OAUTH_GRANT_TYPE,
            OAUTH_CLIENT_AUTH_FIELD: DEV_OAUTH_CLIENT_AUTH,
            OAUTH_PRIVATE_KEY_PATH_FIELD: DEV_OAUTH_PRIVATE_KEY_PATH,
            OAUTH_PRIVATE_KEY_FILE_FIELD: DEV_OAUTH_PRIVATE_KEY_FILE,
            OAUTH_PRIVATE_KEY_JWK_FIELD: DEV_OAUTH_PRIVATE_KEY_JWK,
            STRICT_MODE_FIELD: DEV_STRICT_MODE,
            VERIFY_SSL_FIELD: DEV_VERIFY_SSL,
        },
        CUSTOM_ENVIRONMENT: {
            BASE_URL_FIELD: CUSTOM_BASE_URL,
            ADMIN_BASE_URL_FIELD: CUSTOM_ADMIN_BASE_URL,
            AUTH_BASE_URL_FIELD: CUSTOM_AUTH_BASE_URL,
            CONNECTION_TYPE_FIELD: CUSTOM_CONNECTION_TYPE,
            LEGACY_ACCESS_ID_FIELD: CUSTOM_LEGACY_ACCESS_ID,
            LEGACY_KEY_PATH_FIELD: CUSTOM_LEGACY_KEY_PATH,
            LEGACY_KEY_FILE_FIELD: CUSTOM_LEGACY_KEY_FILE,
            LEGACY_KEY_PEM_FIELD: CUSTOM_LEGACY_KEY_PEM,
            LEGACY_KEY_MATERIAL_PATH_FIELD: CUSTOM_LEGACY_KEY_MATERIAL_PATH,
            LEGACY_KEY_MATERIAL_FILE_FIELD: CUSTOM_LEGACY_KEY_MATERIAL_FILE,
            OAUTH_ISSUER_URL_FIELD: CUSTOM_OAUTH_ISSUER_URL,
            OAUTH_CLIENT_ID_FIELD: CUSTOM_OAUTH_CLIENT_ID,
            OAUTH_SCOPE_FIELD: CUSTOM_OAUTH_SCOPE,
            OAUTH_GRANT_TYPE_FIELD: CUSTOM_OAUTH_GRANT_TYPE,
            OAUTH_CLIENT_AUTH_FIELD: CUSTOM_OAUTH_CLIENT_AUTH,
            OAUTH_PRIVATE_KEY_PATH_FIELD: CUSTOM_OAUTH_PRIVATE_KEY_PATH,
            OAUTH_PRIVATE_KEY_FILE_FIELD: CUSTOM_OAUTH_PRIVATE_KEY_FILE,
            OAUTH_PRIVATE_KEY_JWK_FIELD: CUSTOM_OAUTH_PRIVATE_KEY_JWK,
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
        ADMIN_BASE_URL_FIELD,
        AUTH_BASE_URL_FIELD,
        CONNECTION_TYPE_FIELD,
        LEGACY_ACCESS_ID_FIELD,
        LEGACY_KEY_PATH_FIELD,
        LEGACY_KEY_FILE_FIELD,
        LEGACY_KEY_PEM_FIELD,
        LEGACY_KEY_MATERIAL_PATH_FIELD,
        LEGACY_KEY_MATERIAL_FILE_FIELD,
        OAUTH_ISSUER_URL_FIELD,
        OAUTH_CLIENT_ID_FIELD,
        OAUTH_SCOPE_FIELD,
        OAUTH_GRANT_TYPE_FIELD,
        OAUTH_CLIENT_AUTH_FIELD,
        OAUTH_PRIVATE_KEY_PATH_FIELD,
        OAUTH_PRIVATE_KEY_FILE_FIELD,
        OAUTH_PRIVATE_KEY_JWK_FIELD,
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
    LEGACY_PRIVATE_KEY_PEM: ClassVar[str] = 'private_key_pem'
    LEGACY_KEY_MATERIAL_PATH: ClassVar[str] = 'private_key_material_path'
    LEGACY_KEY_MATERIAL_FILE: ClassVar[str] = 'private_key_material_file'
    LEGACY_FIELDS: ClassVar[frozenset[str]] = frozenset({
        LEGACY_ACCESS_ID,
        LEGACY_PRIVATE_KEY_FILE,
        LEGACY_PRIVATE_KEY_PATH,
        LEGACY_PRIVATE_KEY_PEM,
        LEGACY_KEY_MATERIAL_PATH,
        LEGACY_KEY_MATERIAL_FILE,
    })

    # OAuth authentication fields
    OAUTH_ISSUER_URL: ClassVar[str] = 'issuer_url'
    OAUTH_CLIENT_ID: ClassVar[str] = 'client_id'
    OAUTH_SCOPE: ClassVar[str] = 'scope'
    OAUTH_GRANT_TYPE: ClassVar[str] = 'grant_type'
    OAUTH_CLIENT_AUTHENTICATION: ClassVar[str] = 'client_authentication'
    OAUTH_PRIVATE_KEY_PATH: ClassVar[str] = 'private_key_path'
    OAUTH_PRIVATE_KEY_FILE: ClassVar[str] = 'private_key_file'
    OAUTH_PRIVATE_KEY_JWK: ClassVar[str] = 'private_key_jwk'
    OAUTH_FIELDS: ClassVar[frozenset[str]] = frozenset({
        OAUTH_ISSUER_URL,
        OAUTH_CLIENT_ID,
        OAUTH_SCOPE,
        OAUTH_GRANT_TYPE,
        OAUTH_CLIENT_AUTHENTICATION,
        OAUTH_PRIVATE_KEY_PATH,
        OAUTH_PRIVATE_KEY_FILE,
        OAUTH_PRIVATE_KEY_JWK,
    })

    # OAuth default values
    OAUTH_DEFAULT_GRANT_TYPE: ClassVar[str] = 'Client Credentials'
    OAUTH_DEFAULT_CLIENT_AUTH: ClassVar[str] = 'Private Key JWT'
    OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS: ClassVar[str] = 'client_credentials'
    OAUTH_CLIENT_AUTH_PRIVATE_KEY_JWT: ClassVar[str] = 'private_key_jwt'
    OAUTH_CLIENT_AUTH_CLIENT_SECRET_BASIC: ClassVar[str] = 'client_secret_basic'
    OAUTH_GRANT_TYPE_MAPPING: ClassVar[Mapping[str, str]] = MappingProxyType({
        OAUTH_DEFAULT_GRANT_TYPE.lower(): OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS,
        OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS: OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS,
        'client credentials': OAUTH_GRANT_TYPE_CLIENT_CREDENTIALS,
    })
    OAUTH_CLIENT_AUTH_MAPPING: ClassVar[Mapping[str, str]] = MappingProxyType({
        OAUTH_DEFAULT_CLIENT_AUTH.lower(): OAUTH_CLIENT_AUTH_PRIVATE_KEY_JWT,
        OAUTH_CLIENT_AUTH_PRIVATE_KEY_JWT: OAUTH_CLIENT_AUTH_PRIVATE_KEY_JWT,
        'private key jwt': OAUTH_CLIENT_AUTH_PRIVATE_KEY_JWT,
        'private-key-jwt': OAUTH_CLIENT_AUTH_PRIVATE_KEY_JWT,
        'client_secret_basic': OAUTH_CLIENT_AUTH_CLIENT_SECRET_BASIC,
        'client secret basic': OAUTH_CLIENT_AUTH_CLIENT_SECRET_BASIC,
        'client-secret-basic': OAUTH_CLIENT_AUTH_CLIENT_SECRET_BASIC,
    })

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
# OAuth Scopes
# -----------------------------
@dataclass(frozen=True)
class OauthScopes:
    """Constants representing the OAuth 2.0 permission scopes.
    (`Reference <https://community.rsa.com/s/article/OAuth-2-0-Based-Permissions-for-the-Cloud-Administration-APIs-27c2ca90>`__)
    """
    # Agent permissions (Cloud Administration API)
    AGENT_READ: ClassVar[str] = 'rsa.agent.read'                                           # Retrieve Agent details
    AGENT_CERT: ClassVar[str] = 'rsa.agent.cert'                                           # Agent Certificate Provisioning
    AGENT_SCOPES: ClassVar[frozenset] = frozenset({
        AGENT_READ,
        AGENT_CERT,
    })

    # Audit permissions (Cloud Administration API)
    AUDIT_ADMIN: ClassVar[str] = 'rsa.audit.admin'                                         # Retrieve admin event logs from the Cloud Access Service (audit microservice)
    AUDIT_USER: ClassVar[str] = 'rsa.audit.user'                                           # Retrieve RSA authentication audit and user event logs
    AUDIT_SCOPES: ClassVar[frozenset] = frozenset({
        AUDIT_ADMIN,
        AUDIT_USER,
    })

    # Authenticator permissions (Cloud Administration API)
    AUTHENTICATOR_MOBILE_DELETE: ClassVar[str] = 'rsa.authenticator.mobile.delete'         # Delete a device for individual users
    AUTHENTICATOR_MOBILE_READ: ClassVar[str] = 'rsa.authenticator.mobile.read'             # Retrieve device details for individual users and user event logs
    AUTHENTICATOR_MOBILE_MANAGE: ClassVar[str] = 'rsa.authenticator.mobile.manage'         # Generate a code for users to register their iOS, Android, and Windows devices
    AUTHENTICATOR_DEVICE_DELETE: ClassVar[str] = 'rsa.authenticator.device.delete'         # Delete devices for individual users
    AUTHENTICATOR_EMERGENCY_MANAGE: ClassVar[str] = 'rsa.authenticator.emergency.manage'   # Enable/disable Emergency Token code for a user
    AUTHENTICATOR_FIDO_READ: ClassVar[str] = 'rsa.authenticator.fido.read'                 # Retrieve FIDO authenticator(s) assigned to a user
    AUTHENTICATOR_FIDO_DELETE: ClassVar[str] = 'rsa.authenticator.fido.delete'             # Delete FIDO authenticator assigned to a user
    AUTHENTICATOR_FIDO_MANAGE: ClassVar[str] = 'rsa.authenticator.fido.manage'             # Update, enroll, enable, and disable FIDO authenticators
    AUTHENTICATOR_SIDTOKEN_READ: ClassVar[str] = 'rsa.authenticator.sidtoken.read'         # Retrieve a hardware token's details
    AUTHENTICATOR_SIDTOKEN_MANAGE: ClassVar[str] = 'rsa.authenticator.sidtoken.manage'     # Update, enable, disable, assign, unassign, and clear pin for a hardware token
    AUTHENTICATOR_SIDTOKEN_DELETE: ClassVar[str] = 'rsa.authenticator.sidtoken.delete'     # Delete a hardware token from CAS
    AUTHENTICATOR_DS100_MANAGE: ClassVar[str] = 'rsa.authenticator.ds100.manage'           # Enable, disable, and clear pin for a SecurID DS100 OTP
    AUTHENTICATOR_DS100_DELETE: ClassVar[str] = 'rsa.authenticator.ds100.delete'           # Delete user's SecurID DS100 OTP credential
    AUTHENTICATOR_DS100_READ: ClassVar[str] = 'rsa.authenticator.ds100.read'               # Retrieve user's RSA DS100 OTP credential
    AUTHENTICATOR_SCOPES: ClassVar[frozenset] = frozenset({
        AUTHENTICATOR_MOBILE_DELETE,
        AUTHENTICATOR_MOBILE_READ,
        AUTHENTICATOR_MOBILE_MANAGE,
        AUTHENTICATOR_DEVICE_DELETE,
        AUTHENTICATOR_EMERGENCY_MANAGE,
        AUTHENTICATOR_FIDO_READ,
        AUTHENTICATOR_FIDO_DELETE,
        AUTHENTICATOR_FIDO_MANAGE,
        AUTHENTICATOR_SIDTOKEN_READ,
        AUTHENTICATOR_SIDTOKEN_MANAGE,
        AUTHENTICATOR_SIDTOKEN_DELETE,
        AUTHENTICATOR_DS100_MANAGE,
        AUTHENTICATOR_DS100_DELETE,
        AUTHENTICATOR_DS100_READ,
    })

    # FIDO configuration permissions (Cloud Administration API)
    FIDO_CONFIGURATION_MANAGE: ClassVar[str] = 'rsa.fido.configuration.manage'             # Manage configuration of FIDO authenticators
    FIDO_CONFIGURATION_READ: ClassVar[str] = 'rsa.fido.configuration.read'                 # Retrieve current configuration of FIDO authenticators
    FIDO_CONFIGURATION_SCOPES: ClassVar[frozenset] = frozenset({
        FIDO_CONFIGURATION_MANAGE,
        FIDO_CONFIGURATION_READ,
    })

    # Local group permissions (Cloud Administration API)
    GROUP_MANAGE: ClassVar[str] = 'rsa.group.manage'                                       # Local group management actions (create, update, delete)
    GROUP_READ: ClassVar[str] = 'rsa.group.read'                                           # Retrieve local group(s) details
    GROUP_USERS_MANAGE: ClassVar[str] = 'rsa.group.users.manage'                           # Local group membership actions (add/remove users)
    GROUPS_USERS_READ: ClassVar[str] = 'rsa.group.users.read'                              # Retrieve local group user details
    GROUPS_SCOPES: ClassVar[frozenset] = frozenset({
        GROUP_MANAGE,
        GROUP_READ,
        GROUP_USERS_MANAGE,
        GROUPS_USERS_READ,
    })

    # Report permissions (Cloud Administration API)
    REPORT_HEALTH: ClassVar[str] = 'rsa.report.health'                                     # Retrieve report on CAS availability
    REPORT_LICENSE_USAGE: ClassVar[str] = 'rsa.report.license.usage'                       # Retrieve MFA license usage to monitor license compliance
    REPORT_READ: ClassVar[str] = 'rsa.report.read'                                         # Generate and download users, hardware tokens, and MFA clients report
    REPORT_USER_RISKY: ClassVar[str] = 'rsa.report.user.risky'                             # Retrieve a list of users who exhibit anomalous behavior
    REPORT_SCOPES: ClassVar[frozenset] = frozenset({
        REPORT_HEALTH,
        REPORT_LICENSE_USAGE,
        REPORT_READ,
        REPORT_USER_RISKY,
    })

    # User permissions (Cloud Administration API)
    USER_READ: ClassVar[str] = 'rsa.user.read'                                             # Retrieve user information from the identity source
    USER_SYNC: ClassVar[str] = 'rsa.user.sync'                                             # User synchronization to user identity
    USER_DELETE_SOFT: ClassVar[str] = 'rsa.user.delete.soft'                               # Mark a disabled user as pending deletion
    USER_DELETE: ClassVar[str] = 'rsa.user.delete'                                         # Delete a single disabled user and immediately remove all devices associated with that user
    USER_MANAGE: ClassVar[str] = 'rsa.user.manage'                                         # Update, sync, enable, and disable users
    USER_FACTOR_MANAGE: ClassVar[str] = 'rsa.user.factor.manage'                           # Unlock, update, reset, and generate codes for users' authentication factors
    USER_RISKY_MANAGE: ClassVar[str] = 'rsa.user.risky.manage'                             # Add or remove one or more users from the high-risk user lisT
    USER_RISKY_READ: ClassVar[str] = 'rsa.user.risky.read'                                 # Retrieve a list of users who are identified as high risk
    USER_SCOPES: ClassVar[frozenset] = frozenset({
        USER_READ,
        USER_SYNC,
        USER_DELETE_SOFT,
        USER_DELETE,
        USER_MANAGE,
        USER_FACTOR_MANAGE,
        USER_RISKY_MANAGE,
        USER_RISKY_READ,
    })

    # MFA permissions (Cloud Authentication API)
    MFA_AUTHN: ClassVar[str] = 'rsa.mfa.authn'                                             # For multifactor, multistep authentications with CAS
    MFA_IDENTITY_CONFIDENCE: ClassVar[str] = 'rsa.mfa.identityconfidence'                  # View and update the identity confidence score of a user
    MFA_SCOPES: ClassVar[frozenset] = frozenset({
        MFA_AUTHN,
        MFA_IDENTITY_CONFIDENCE,
    })

    # Collection of all scopes
    ALL_SCOPES: ClassVar[frozenset[str]] = frozenset().union(
        AGENT_SCOPES,
        AUDIT_SCOPES,
        AUTHENTICATOR_SCOPES,
        FIDO_CONFIGURATION_SCOPES,
        GROUPS_SCOPES,
        REPORT_SCOPES,
        USER_SCOPES,
        MFA_SCOPES,
    )


# -----------------------------
# HTTP / Networking Defaults
# -----------------------------
# API types
ADMIN_API_TYPE: Final[str] = 'admin'
AUTH_API_TYPE: Final[str] = 'auth'

# JSON Web Key Set (JWK)
EC_KEY_TYPE: Final[str] = 'EC'
RSA_KEY_TYPE: Final[str] = 'RSA'
EC_KEY_ALGORITHM: Final[str] = 'ES256'
RSA_KEY_ALGORITHM: Final[str] = 'RS256'

# Default values
DEFAULT_API_TIMEOUT_SECONDS: Final[int] = 30
DEFAULT_API_MAX_RETRIES: Final[int] = 3
DEFAULT_API_TYPE: Final[str] = ADMIN_API_TYPE
DEFAULT_STRICT_MODE: Final[bool] = True
DEFAULT_VERIFY_SSL: Final[bool] = True
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

    # OAuth payload parameters
    OAUTH_ACCESS_TOKEN: ClassVar[str] = 'access_token'
    OAUTH_SCOPE: ClassVar[str] = 'scope'
    OAUTH_CLIENT_ASSERTION: ClassVar[str] = 'client_assertion'
    OAUTH_CLIENT_ASSERTION_TYPE: ClassVar[str] = 'client_assertion_type'
    OAUTH_EXPIRES_AT: ClassVar[str] = 'expires_at'
    OAUTH_EXPIRES_IN: ClassVar[str] = 'expires_in'
    OAUTH_TOKEN_TYPE: ClassVar[str] = 'token_type'

    # JWT Claims fields (RFC 7519 and RFC 7523)
    JWT_ISS: ClassVar[str] = 'iss'
    JWT_SUB: ClassVar[str] = 'sub'
    JWT_AUD: ClassVar[str] = 'aud'
    JWT_IAT: ClassVar[str] = 'iat'
    JWT_EXP: ClassVar[str] = 'exp'
    JWT_NBF: ClassVar[str] = 'nbf'
    JWT_JTI: ClassVar[str] = 'jti'

    JWT_ISSUER: ClassVar[str] = JWT_ISS         # Also a header parameter
    JWT_SUBJECT: ClassVar[str] = JWT_SUB        # Also a header parameter
    JWT_AUDIENCE: ClassVar[str] = JWT_AUD       # Also a header parameter
    JWT_ISSUED_AT: ClassVar[str] = JWT_IAT
    JWT_EXPIRATION: ClassVar[str] = JWT_EXP
    JWT_NOT_BEFORE: ClassVar[str] = JWT_NBF
    JWT_ID: ClassVar[str] = JWT_JTI

    # JWT Header Parameters (RFC 7519)
    JWT_TYP: ClassVar[str] = 'typ'
    JWT_CTY: ClassVar[str] = 'cty'
    JWT_ALG: ClassVar[str] = 'alg'
    JWT_ENC: ClassVar[str] = 'enc'

    JWT_CONTENT_TYPE: ClassVar[str] = JWT_CTY
    JWT_TYPE: ClassVar[str] = JWT_TYP
    JWT_ALGORITHM: ClassVar[str] = JWT_ALG
    JWT_ENCRYPTION: ClassVar[str] = JWT_ENC

    # JSON Web Key Set (JWK) properties (RFC 7515 and RFC 7518)
    JWK_ALG: ClassVar[str] = 'alg'
    JWK_JKU: ClassVar[str] = 'jku'
    JWK_JWK: ClassVar[str] = 'jwk'
    JWK_KID: ClassVar[str] = 'kid'
    JWK_X5U: ClassVar[str] = 'x5u'
    JWK_X5C: ClassVar[str] = 'x5c'
    JWK_TYP: ClassVar[str] = 'typ'
    JWK_CTY: ClassVar[str] = 'cty'
    JWK_CRIT: ClassVar[str] = 'crit'

    JWK_ALGORITHM: ClassVar[str] = JWK_ALG
    JWK_SET_URL: ClassVar[str] = JWK_JKU
    JWK_WEB_KEY: ClassVar[str] = JWK_JWK
    JWK_KEY_ID: ClassVar[str] = JWK_KID
    JWK_X509_URL: ClassVar[str] = JWK_X5U
    JWK_X509_CERT_CHAIN: ClassVar[str] = JWK_X5C
    JWK_TYPE: ClassVar[str] = JWK_TYP
    JWK_CONTENT_TYPE: ClassVar[str] = JWK_CTY
    JWK_CRITICAL: ClassVar[str] = JWK_CRIT

    # JSON Web Encryption (JWE) Properties (RFC 7516)
    JWE_ALG: ClassVar[str] = 'alg'
    JWE_ENC: ClassVar[str] = 'enc'
    JWE_ZIP: ClassVar[str] = 'zip'

    JWE_ALGORITHM: ClassVar[str] = JWE_ALG
    JWE_ENCRYPTION_ALGORITHM: ClassVar[str] = JWE_ENC
    JWE_COMPRESSION_ALGORITHM: ClassVar[str] = JWE_ZIP

    # JSON Web Algorithm (JWA) Properties (RFC 7518)
    JWA_KTY: ClassVar[str] = 'kty'

    JWA_KEY_TYPE: ClassVar[str] = JWA_KTY

    # JSON Web Algorithms - Elliptic Curve Key Parameters
    JWA_EC_CRV: ClassVar[str] = 'crv'
    JWA_EC_X: ClassVar[str] = 'x'
    JWA_EC_Y: ClassVar[str] = 'y'
    JWA_EC_D: ClassVar[str] = 'd'

    JWA_EC_CURVE: ClassVar[str] = JWA_EC_CRV
    JWA_EC_X_COORDINATE: ClassVar[str] = JWA_EC_X
    JWA_EC_Y_COORDINATE: ClassVar[str] = JWA_EC_Y
    JWA_EC_PRIVATE_KEY: ClassVar[str] = JWA_EC_D

    # JSON Web Algorithms - RSA Key Parameters
    JWA_RSA_N: ClassVar[str] = 'n'
    JWA_RSA_E: ClassVar[str] = 'e'
    JWA_RSA_D: ClassVar[str] = 'd'
    JWA_RSA_P: ClassVar[str] = 'p'
    JWA_RSA_Q: ClassVar[str] = 'q'
    JWA_RSA_DP: ClassVar[str] = 'dp'
    JWA_RSA_DQ: ClassVar[str] = 'dq'
    JWA_RSA_QI: ClassVar[str] = 'qi'
    JWA_RSA_OTH: ClassVar[str] = 'oth'
    JWA_RSA_R: ClassVar[str] = 'r'
    JWA_RSA_T: ClassVar[str] = 't'

    JWA_RSA_MODULUS: ClassVar[str] = JWA_RSA_N
    JWA_RSA_EXPONENT: ClassVar[str] = JWA_RSA_E
    JWA_RSA_PRIVATE_EXPONENT: ClassVar[str] = JWA_RSA_D
    JWA_RSA_FIRST_PRIME_FACTOR: ClassVar[str] = JWA_RSA_P
    JWA_RSA_SECOND_PRIME_FACTOR: ClassVar[str] = JWA_RSA_Q
    JWA_RSA_FIRST_FACTOR_CRT_EXPONENT: ClassVar[str] = JWA_RSA_DP
    JWA_RSA_SECOND_FACTOR_CRT_EXPONENT: ClassVar[str] = JWA_RSA_DQ
    JWA_RSA_FIRST_CRT_COEFFICIENT: ClassVar[str] = JWA_RSA_QI
    JWA_RSA_OTHER_PRIMES_INFO: ClassVar[str] = JWA_RSA_OTH
    JWA_RSA_PRIME_FACTOR: ClassVar[str] = JWA_RSA_R
    JWA_RSA_FACTOR_CRT_EXPONENT: ClassVar[str] = JWA_RSA_D
    JWA_RSA_FACTOR_CRT_COEFFICIENT: ClassVar[str] = JWA_RSA_T


# -----------------------------
# API Authentication Values
# -----------------------------
@dataclass(frozen=True)
class AuthValues:
    """Field/Parameter values relating to API authentication."""
    # Legacy default values
    LEGACY_KEY_ALGORITHM: ClassVar[str] = RSA_KEY_ALGORITHM
    LEGACY_DEFAULT_EXPIRATION: ClassVar[int] = 3600

    # OAuth default values
    OAUTH_DEFAULT_GRANT_TYPE: ClassVar[str] = 'Client Credentials'
    OAUTH_DEFAULT_CLIENT_AUTH: ClassVar[str] = 'Private Key JWT'
    OAUTH_CLIENT_ASSERT_TYPE_JWT_BEARER: ClassVar[str] = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    OAUTH_TOKEN_TYPE_BEARER: ClassVar[str] = 'Bearer'
    OAUTH_DEFAULT_FORCE_REFRESH: ClassVar[bool] = False
    OAUTH_DEFAULT_TOKEN_EXPIRATION: ClassVar[int] = 3600
    _OAUTH_TOKEN_EXPIRY_BUFFER_SECONDS: ClassVar[int] = 30
    _OAUTH_ASSERTION_LIFETIME_SECONDS: ClassVar[int] = 300

    # JSON Web Algorithm (JWA) Property Values (RFC 7518)
    JWA_EC: ClassVar[str] = 'EC'       # DSS
    JWA_RSA: ClassVar[str] = 'RSA'     # RFC 3447
    JWA_OCT: ClassVar[str] = 'oct'     # Used to represent symmetric keys


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
    BEARER: ClassVar[str] = 'Bearer {token}'                                                        # Vars: token


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
    Q: ClassVar[str] = ';q={weight}'                                                                # Vars: weight


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
    Q: ClassVar[str] = ';q={weight}'                                                                # Vars: weight


# -------------------------------
# Relevant URLs
# -------------------------------
@dataclass(frozen=True)
class Urls:
    """Common URLs leveraged throughout the package."""
    # Schemes
    HTTP: ClassVar[str] = 'http://'
    HTTPS: ClassVar[str] = 'https://'
    HTTP_SCHEME: ClassVar[str] = 'http'
    HTTPS_SCHEME: ClassVar[str] = 'https'

    # General URLs
    BASE_URL: ClassVar[str] = HTTPS + '{tenant_name}.{api_type}.securid.com'                        # Vars: tenant_name, api_type
    BASE_ADMIN_URL: ClassVar[str] = HTTPS + '{tenant_name}.access.securid.com'                      # Vars: tenant_name
    BASE_AUTH_URL: ClassVar[str] = HTTPS + '{tenant_name}.auth.securid.com'                         # Vars: tenant_name
    OAUTH: ClassVar[str] = '{base_url}/oauth'                                                       # Vars: base_url
    OAUTH_TOKEN: ClassVar[str] = '{issuer_url}/token'                                               # Vars: issuer_url


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
    # Versions
    V1_1: ClassVar[str] = 'v1_1'

    # General REST paths
    ADMIN_BASE: ClassVar[str] = '/AdminInterface/restapi'
    AUTH_BASE: ClassVar[str] = '/mfa/' + V1_1 + '/authn'

    # Users endpoint paths
    # TODO: Add a preceding slash to USERS string after ensuring base URL references end with slash
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
    STATUS_CODE: ClassVar[str] = 'status_code'


# -----------------------------
# Exported namespaces
# -----------------------------
# Common (Public)
ARGUMENT_VALUES: Final[ArgumentValues] = ArgumentValues()
CREDENTIAL_VALUES: Final[CredentialValues] = CredentialValues()
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
OAUTH_SCOPES: Final[OauthScopes] = OauthScopes()
CONTENT_TYPES: Final[ContentTypes] = ContentTypes()
ENCODING_TYPES: Final[EncodingTypes] = EncodingTypes()
HEADERS: Final[Headers] = Headers()
LANGUAGES: Final[Languages] = Languages()
PAYLOAD_VALUES: Final[PayloadValues] = PayloadValues()
QUERY_PARAMS: Final[QueryParams] = QueryParams()
RESPONSE_KEYS: Final[ResponseKeys] = ResponseKeys()
REST_PATHS: Final[RestPaths] = RestPaths()
