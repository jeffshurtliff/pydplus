# -*- coding: utf-8 -*-
"""
:Module:            pydplus.constants
:Synopsis:          Constants that are utilized throughout the package
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     05 Mar 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, ClassVar, Mapping, Union


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
    FILE: ClassVar[str] = 'file'
    URL: ClassVar[str] = 'url'


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
    # TODO: Add constants for the client object


# -------------------------------
# Helper Configuration Settings
# -------------------------------
@dataclass(frozen=True)
class HelperSettings:
    """Fields, values, and other constants relating to the helper configuration settings and
       the :py:mod:`pydplus.utils.helper` module.
    """
    # Validation criteria
    VALID_HELPER_FILE_TYPES: ClassVar[frozenset[str]] = frozenset({'json', 'yml', 'yaml'})
    VALID_YAML_TRUE_VALUES: ClassVar[frozenset[str]] = frozenset({'yes', 'true'})

    # Root-level helper fields
    BASE_URL: ClassVar[str] = 'base_url'
    CONNECTION: ClassVar[str] = 'connection'
    CONNECTION_TYPE: ClassVar[str] = 'connection_type'
    SSL_VERIFY: str = 'ssl_verify'
    STRICT_MODE: ClassVar[str] = 'strict_mode'
    ENV_VARIABLES: ClassVar[str] = 'env_variables'
    ROOT_LEVEL_BASIC_FIELDS: ClassVar[frozenset[str]] = frozenset({
        BASE_URL,
        CONNECTION_TYPE,
        STRICT_MODE,
        SSL_VERIFY,
    })

    # Authentication/Connection type parent fields
    LEGACY: ClassVar[str] = 'legacy'
    OAUTH: ClassVar[str] = 'oauth'

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
    CONNECTION_FIELDS: Final[Mapping[str, frozenset[str]]] = MappingProxyType({
        LEGACY: LEGACY_FIELDS,
        OAUTH: OAUTH_FIELDS,
    })

    # Environment variable fields
    ENV_CONNECTION_TYPE: ClassVar[str] = 'connection_type'
    ENV_LEGACY_ACCESS_ID: ClassVar[str] = 'legacy_access_id'
    ENV_LEGACY_KEY_PATH: ClassVar[str] = 'legacy_key_path'
    ENV_LEGACY_KEY_FILE: ClassVar[str] = 'legacy_key_file'
    ENV_OAUTH_ISSUER_URL: ClassVar[str] = 'oauth_issuer_url'
    ENV_OAUTH_CLIENT_ID: ClassVar[str] = 'oauth_client_id'
    ENV_OAUTH_GRANT_TYPE: ClassVar[str] = 'oauth_grant_type'

    # Environment variable default values
    ENV_DEFAULT_CONNECTION_TYPE: ClassVar[str] = 'PYDPLUS_CONNECTION_TYPE'
    ENV_DEFAULT_LEGACY_ACCESS_ID: ClassVar[str] = 'PYDPLUS_LEGACY_ACCESS_ID'
    ENV_DEFAULT_LEGACY_KEY_PATH: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_PATH'
    ENV_DEFAULT_LEGACY_KEY_FILE: ClassVar[str] = 'PYDPLUS_LEGACY_KEY_FILE'
    ENV_DEFAULT_OAUTH_ISSUER_URL: ClassVar[str] = 'PYDPLUS_OAUTH_ISSUER_URL'
    ENV_DEFAULT_OAUTH_CLIENT_ID: ClassVar[str] = 'PYDPLUS_OAUTH_CLIENT_ID'
    ENV_DEFAULT_OAUTH_GRANT_TYPE: ClassVar[str] = 'PYDPLUS_OAUTH_GRANT_TYPE'

    # Environment variable default mapping
    ENV_VARIABLE_DEFAULT_MAPPING: Final[Mapping[str, str]] = MappingProxyType({
        ENV_CONNECTION_TYPE: ENV_DEFAULT_CONNECTION_TYPE,
        ENV_LEGACY_ACCESS_ID: ENV_DEFAULT_LEGACY_ACCESS_ID,
        ENV_LEGACY_KEY_PATH: ENV_DEFAULT_LEGACY_KEY_PATH,
        ENV_LEGACY_KEY_FILE: ENV_DEFAULT_LEGACY_KEY_FILE,
        ENV_OAUTH_ISSUER_URL: ENV_DEFAULT_OAUTH_ISSUER_URL,
        ENV_OAUTH_CLIENT_ID: ENV_DEFAULT_OAUTH_CLIENT_ID,
        ENV_OAUTH_GRANT_TYPE: ENV_DEFAULT_OAUTH_GRANT_TYPE,
    })

    # Other configuration fields
    # TODO: Add constants here (if needed)

    # Other default values
    DEFAULT_SSL_VERIFY_VALUE = True


# -----------------------------
# HTTP / Networking Defaults
# -----------------------------
DEFAULT_API_TIMEOUT_SECONDS: Final[int] = 30
DEFAULT_API_MAX_RETRIES: Final[int] = 3
HEADER_TYPE_DEFAULT: Final[str] = 'default'
VALID_HEADER_TYPES: Final[frozenset[str]] = frozenset({
    HEADER_TYPE_DEFAULT,
})


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
    # TODO: Add constants to this class


# -------------------------------
# Salesforce REST API Endpoints
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
    # TODO: Add constants here


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


# -----------------------------
# REST API Payload Values
# -----------------------------
@dataclass(frozen=True)
class PayloadValues:
    """Standard and common payload values used in RSA ID Plus REST API requests."""
    # TODO: Populate with constants


# -----------------------------
# REST API Response Keys
# -----------------------------
@dataclass(frozen=True)
class ResponseKeys:
    """Standard and common keys / fields for RSA ID Plus REST API responses."""
    # TODO: Add constants here


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

# HTTP / API
API_REQUEST_TYPES: Final[ApiRequestTypes] = ApiRequestTypes()
AUTH_SCHEMES: Final[AuthSchemes] = AuthSchemes()
CONTENT_TYPES: Final[ContentTypes] = ContentTypes()
ENCODING_TYPES: Final[EncodingTypes] = EncodingTypes()
HEADERS: Final[Headers] = Headers()
LANGUAGES: Final[Languages] = Languages()
PAYLOAD_VALUES: Final[PayloadValues] = PayloadValues()
QUERY_PARAMS: Final[QueryParams] = QueryParams()
RESPONSE_KEYS: Final[ResponseKeys] = ResponseKeys()
REST_PATHS: Final[RestPaths] = RestPaths()
