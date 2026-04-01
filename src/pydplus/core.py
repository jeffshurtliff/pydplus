# -*- coding: utf-8 -*-
"""
:Module:            pydplus.core
:Synopsis:          This module performs the core operations of the package
:Usage:             ``from pydplus import PyDPlus``
:Example:           ``pydp = PyDPlus()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     01 Apr 2026
"""

from __future__ import annotations

import logging
import os
import urllib.parse
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, Optional, Tuple, Union

from . import api, auth, errors
from . import constants as const
from . import users as users_module
from .credentials import IDPlusLegacyKeyMaterial
from .utils import core_utils
from .utils.helper import get_helper_settings

logger = logging.getLogger(__name__)


class PyDPlus:
    """Class for the core client object.

    :param connection_info: Dictionary that defines the connection info to use
    :type connection_info: dict, None
    :param connection_type: Determines whether to leverage a(n) ``oauth`` (default) or ``legacy`` connection
    :type connection_type: str, None
    :param base_url: The base URL to leverage when performing Administration API calls

                     .. note::
                        This parameter is for backwards compatibility only and will eventually be fully deprecated.
                        The ``base_admin_url`` should be leveraged instead as a best practice.

    :type base_url: str, None
    :param base_admin_url: The base URL to leverage when performing Administration API calls
    :type base_admin_url: str, None
    :param base_auth_url: The base URL to leverage when performing Authentication API calls
    :type base_auth_url: str, None
    :param tenant_name: Specify the tenant name for the RSA ID Plus tenant (e.g. ``example-corporation``)

                        .. note::
                           Specifying the tenant name will allow the base URLs to be defined if not already
                           defined via argument, helper setting, or environment variable.

    :type tenant_name: str, None
    :param env: Optionally specify the environment as ``PROD``, ``DEV``, or a custom name. (e.g. ``STAGING``)

                .. note::
                   This parameter will impact which environment variables are referenced when the client object
                   is instantiated. (e.g. ``PYDPLUS_PROD_BASE_URL`` rather than ``PYDPLUS_BASE_URL``)

    :type env: str, None
    :param private_key: The file path to the private key used for legacy API authentication
    :type private_key: str, None
    :param legacy_access_id: The Access ID associated with the Legacy API connection
    :type legacy_access_id: str, None
    :param legacy_key_material: Legacy key material as a ``.key`` file path or parsed object
    :type legacy_key_material: str, pathlib.Path, pydplus.credentials.IDPlusLegacyKeyMaterial, None
    :param oauth_client_id: The Client ID associated with the OAuth API connection
    :type oauth_client_id: str, None
    :param oauth_issuer_url: The explicit OAuth issuer URL to use for token requests (e.g. ``https://<tenant>.auth.securid.com/oauth``)
    :type oauth_issuer_url: str, None
    :param oauth_private_key: The file path to the OAuth private-key JWK file used for Private Key JWT authentication
    :type oauth_private_key: str, None
    :param oauth_private_key_jwk: The OAuth private-key JWK payload used for Private Key JWT authentication
    :type oauth_private_key_jwk: dict, str, None
    :param oauth_scope: One or more OAuth scopes to request in token requests
                        (``+``-delimited string or iterable of scope strings)
    :type oauth_scope: str, tuple, list, set, frozenset, None
    :param oauth_scope_preset: One or more scope preset names to merge with explicit OAuth scopes

                               .. note::
                                  Presets can also be provided through helper settings or environment variables.
                                  (e.g. ``all``, ``user_read_only``, etc.)

    :type oauth_scope_preset: str, tuple, list, set, frozenset, None
    :param oauth_api_type: Defines which API base URL should be used when inferring the OAuth issuer URL
                           (``auth`` by default; ``admin`` supported when configured)
    :type oauth_api_type: str, None
    :param verify_ssl: Determines if SSL connections should be verified (``True`` by default)
    :type verify_ssl: bool, None
    :param auto_connect: Determines if an API connection should be established when the object is instantiated
                         (``True`` by default)
    :type auto_connect: bool
    :param strict_mode: Determines if failed API responses should result in an exception being raised
                        (``False`` by default)
    :type strict_mode: bool, None
    :param env_variables: Optionally define custom environment variable names to use instead of the default names
    :type env_variables: dict, None
    :param helper: Optionally provide the file path for a helper file used to define the object configuration
    :type helper: str, tuple, list, set, dict, None
    :returns: The instantiated PyDPlus object
    :raises: :py:exc:`TypeError`,
             :py:exc:`ValueError`,
             :py:exc:`pydplus.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`pydplus.errors.exceptions.APIConnectionError`
    """

    def __init__(
        self,
        connection_info: Optional[dict] = None,
        connection_type: Optional[str] = None,
        tenant_name: Optional[str] = None,
        base_url: Optional[str] = None,
        base_admin_url: Optional[str] = None,
        base_auth_url: Optional[str] = None,
        env: Optional[str] = None,
        private_key: Optional[str] = None,
        legacy_access_id: Optional[str] = None,
        legacy_key_material: Union[Optional[str], Optional[Path], Optional[IDPlusLegacyKeyMaterial]] = None,
        oauth_client_id: Optional[str] = None,
        oauth_private_key: Optional[str] = None,
        oauth_private_key_jwk: Union[Optional[dict], Optional[str]] = None,
        oauth_scope: Union[Optional[str], Optional[tuple], Optional[list], Optional[set], Optional[frozenset]] = None,
        oauth_scope_preset: Union[Optional[str], Optional[tuple], Optional[list], Optional[set], Optional[frozenset]] = None,
        verify_ssl: Optional[bool] = None,
        auto_connect: bool = const.CLIENT_SETTINGS.DEFAULT_AUTO_CONNECT_VALUE,
        strict_mode: Optional[bool] = None,
        env_variables: Optional[dict] = None,
        helper: Union[Optional[str], Optional[tuple], Optional[list], Optional[set], Optional[dict]] = None,
        oauth_api_type: Optional[str] = None,
        oauth_issuer_url: Optional[str] = None,
    ):
        """Instantiate the core client object."""
        # Define the initial properties and settings
        self._helper_settings = {}
        self._env_variables = {}
        self.base_headers = {}
        self.auto_connect = auto_connect
        self.connected = False
        self.connection_type = None
        self.env = None
        self._oauth_token_data = None
        self.oauth_api_type = const.AUTH_API_TYPE
        self.strict_mode = strict_mode
        self.tenant_name = tenant_name

        # Check for a supplied helper file and extract the configuration settings if found
        self._get_helper_settings(helper)

        # Define the environment if explicitly defined as an argument, helper setting, or environment variable
        self._get_env_name(env)

        # Define the environment variable names to retrieve when defined
        self._define_env_variable_names(env_variables)

        # Check for any defined environment variables using the environment variable names defined above
        self._get_env_variables()

        # Define the strict_mode setting using a passed argument, helper setting, or environment variable
        self._define_strict_mode(strict_mode)  # Defines self.strict_mode

        # Define the verify_ssl value either from a user-defined setting or using the default value
        self._get_verify_ssl_setting(verify_ssl)  # Defines self.verify_ssl

        # Define the legacy key material when applicable
        self.legacy_key_material = self._parse_legacy_key_material(legacy_key_material, connection_info)

        # Use parsed key material as a base URL fallback when no explicit values were provided
        if self.legacy_key_material:
            if not base_url:
                base_url = self.legacy_key_material.admin_rest_api_url  # Base URL will be parsed below
            if not base_admin_url:
                base_admin_url = self.legacy_key_material.admin_rest_api_url  # Base Admin URL will be parsed below

        # Define the base_url value or raise an exception if it cannot be defined
        self._define_base_url(base_url)  # Defines self.base_url

        # Define the admin_base_url (required) and auth_base_url (optional) values
        self._define_base_urls(base_admin_url, base_auth_url)  # Defines self.admin_base_url, self.auth_base_url

        # Define the Administration API base REST URL to use in API calls
        self.admin_base_rest_url = self.admin_base_url + const.REST_PATHS.ADMIN_BASE

        # Define the Authentication API base URL to use in API calls
        self.auth_base_rest_url = self.auth_base_url + const.REST_PATHS.AUTH_BASE if self.auth_base_url else None

        # Define which API type should be used when inferring OAuth issuer URL values
        self._define_oauth_api_type(oauth_api_type)  # Defines self.oauth_api_type

        # Check for provided connection info and define the class object attribute
        self._validate_connection_info(
            connection_info,
            private_key,
            legacy_access_id,
            oauth_client_id,
            oauth_issuer_url,
            oauth_private_key,
            oauth_private_key_jwk,
            oauth_scope,
            oauth_scope_preset,
            self.legacy_key_material,
        )

        # Define the connection type that should be used to authenticate
        self._get_connection_type(connection_type)  # Defines self.connection_type

        # Connect to the tenant (if auto-connect is enabled) and retrieve the base API headers
        if self.auto_connect:
            self.connected, self.base_headers = self.connect()
            # TODO: Figure out how to connect after instantiation and update self.connected and self.base_headers

        # Import inner object classes so their methods can be called from the primary object
        self.users: PyDPlus.User = self._import_user_class()

    def _import_user_class(self):
        """Allow the :py:class:`pydplus.core.PyDPlus.User` class to be utilized within the core object."""
        return PyDPlus.User(self)

    def _get_helper_settings(self, _helper):
        """Retrieve the settings from a helper configuration file if passed as an argument."""
        if _helper:
            # Parse the helper file contents
            if any((isinstance(_helper, tuple), isinstance(_helper, list), isinstance(_helper, set))):
                _helper_file_path, _helper_file_type = _helper
            elif isinstance(_helper, str):
                _helper_file_path, _helper_file_type = (_helper, const.HELPER_SETTINGS.DEFAULT_HELPER_FILE_TYPE)
            elif isinstance(_helper, dict):
                _helper_file_path, _helper_file_type = _helper.values()
            else:
                _error_msg = "The 'helper' argument can only be supplied as string, tuple, list, set or dict"
                logger.error(_error_msg)
                raise TypeError(_error_msg)
            self.helper_path = _helper_file_path
            self._helper_settings = get_helper_settings(_helper_file_path, _helper_file_type)
            logger.info('The helper configuration settings have been loaded successfully')
        else:
            logger.debug('No helper configuration settings were found and therefore none have been configured')
            self._helper_settings = {}

    def _define_legacy_key_material_path(self, _connection_info: Optional[dict] = None) -> str:
        """Defines the path to the legacy API key material file if the file name and/or path has been configured."""
        # Initially define variables
        _key_material_path = ''
        _legacy_key = const.CONNECTION_INFO.LEGACY
        _material_file_key = const.CONNECTION_INFO.LEGACY_KEY_MATERIAL_FILE
        _material_path_key = const.CONNECTION_INFO.LEGACY_KEY_MATERIAL_PATH
        _helper_conn_key = const.HELPER_SETTINGS.CONNECTION
        _env_material_file_key = const.ENV_VARIABLES.LEGACY_KEY_MATERIAL_FILE_FIELD
        _env_material_path_key = const.ENV_VARIABLES.LEGACY_KEY_MATERIAL_PATH_FIELD

        # Attempt to define the full path using the connection_info dictionary if defined
        if (
            _connection_info
            and isinstance(_connection_info.get(_legacy_key), dict)
            and isinstance(_connection_info[_legacy_key].get(_material_file_key), str)
            and _connection_info[_legacy_key][_material_file_key]
        ):
            _key_material_path = _connection_info[_legacy_key][_material_file_key]

            # Check if a path is also defined as part of the connection_info dictionary
            if (
                isinstance(_connection_info[_legacy_key].get(_material_path_key), str)
                and _connection_info[_legacy_key][_material_path_key]
            ):
                _path_to_material_file = core_utils.ensure_ending_slash(_connection_info[_legacy_key][_material_path_key])
                _key_material_path = _path_to_material_file + _key_material_path
            logger.debug(f"Defined '{_key_material_path}' as the path to the key material file via connection_info")

        # Attempt to define the full path using the helper settings if defined
        elif (
            self._helper_settings
            and _helper_conn_key in self._helper_settings
            and isinstance(self._helper_settings[_helper_conn_key].get(_legacy_key), dict)
            and isinstance(self._helper_settings[_helper_conn_key][_legacy_key].get(_material_file_key), str)
            and self._helper_settings[_helper_conn_key][_legacy_key][_material_file_key]
        ):
            _key_material_path = self._helper_settings[_helper_conn_key][_legacy_key][_material_file_key]

            # Check if a path is also defined as part of the helper settings
            if (
                isinstance(self._helper_settings[_helper_conn_key][_legacy_key].get(_material_path_key), str)
                and self._helper_settings[_helper_conn_key][_legacy_key][_material_path_key]
            ):
                _path_to_material_file = core_utils.ensure_ending_slash(
                    self._helper_settings[_helper_conn_key][_legacy_key][_material_path_key]
                )
                _key_material_path = _path_to_material_file + _key_material_path
            logger.debug(f"Defined '{_key_material_path}' as the path to the key material file via helper settings")

        # Attempt to define the full path using environment variables if defined
        elif (
            self._env_variables
            and isinstance(self._env_variables.get(_env_material_file_key), str)
            and self._env_variables[_env_material_file_key]
        ):
            _key_material_path = self._env_variables[_env_material_file_key]

            # Check if a path is also defined as an environment variable
            if isinstance(self._env_variables.get(_env_material_path_key), str) and self._env_variables[_env_material_path_key]:
                _path_to_material_file = core_utils.ensure_ending_slash(self._env_variables[_env_material_path_key])
                _key_material_path = _path_to_material_file + _key_material_path
            logger.debug(f"Defined '{_key_material_path}' as the path to the key material file via environment variables")

        # Returned the defined (or empty) path to the key material file
        if not _key_material_path:
            logger.debug('The key material file path could not be defined and will not be used for authentication')
        return _key_material_path

    def _parse_legacy_key_material(
        self,
        _legacy_key_material: Union[Optional[str], Optional[Path], Optional[IDPlusLegacyKeyMaterial]] = None,
        _connection_info: Optional[dict] = None,
    ) -> Optional[IDPlusLegacyKeyMaterial]:
        """Parse and validate the legacy key material if provided."""
        # Attempt to define the legacy key material file path if not defined via argument
        if _legacy_key_material is None:
            _legacy_key_material = self._define_legacy_key_material_path(_connection_info)
            if not _legacy_key_material:
                return None

        if isinstance(_legacy_key_material, IDPlusLegacyKeyMaterial):
            _legacy_key_material.validate()
            return _legacy_key_material
        if isinstance(_legacy_key_material, (str, Path)):
            return IDPlusLegacyKeyMaterial.from_file(_legacy_key_material)
        _error_msg = (
            "The 'legacy_key_material' parameter must be a string path, pathlib.Path value, or IDPlusLegacyKeyMaterial object"
        )
        logger.error(_error_msg)
        raise TypeError(_error_msg)

    def _get_env_name(self, _env: Optional[str] = None) -> None:
        """Identify the environment name if defined with an argument or environment variable."""
        setting = 'environment name'
        methods = const.ARGUMENT_VALUES.PROVIDED_METHODS  # arg, helper, or env
        debug_msg = const._LOG_MESSAGES._CLIENT_SETTING_CONFIGURED

        # Attempt to define the environment name using a passed argument
        if _env:
            if not isinstance(_env, str):
                _error_msg = f"The 'env' argument is an invalid data type (Expected: str, Provided: {type(_env)})"
                logger.error(_error_msg)
                raise TypeError(_error_msg)
            self.env = _env.upper()
            logger.debug(debug_msg.format(setting=setting, value=self.env, method=methods[0]))

        # Attempt to define the environment name using helper settings if configured
        if (
            not self.env
            and self._helper_settings
            and isinstance(self._helper_settings.get(const.HELPER_SETTINGS.ENV_NAME), str)
            and self._helper_settings[const.HELPER_SETTINGS.ENV_NAME]
        ):
            self.env = self._helper_settings[const.HELPER_SETTINGS.ENV_NAME].upper()
            logger.debug(debug_msg.format(setting=setting, value=self.env, method=methods[1]))

        # Define the environment name (or lack thereof) using the environment variable
        if not self.env:
            _env = os.getenv(const.ENV_VARIABLES.ENV_NAME)  # Returns None if not found
            self.env = _env.upper() if _env else None
            if self.env:
                logger.debug(debug_msg.format(setting=setting, value=self.env, method=methods[2]))
            else:
                logger.debug('The environment name could not be defined as it was not specified anywhere')

    def _define_env_variable_names(self, _env_variables_from_arg: Optional[dict]) -> None:
        """Define the environment variable names to use based on an explicit argument or helper settings."""
        # Check for custom environment variable names passed as an argument (or environment-specific)
        if _env_variables_from_arg:
            if not isinstance(_env_variables_from_arg, dict):
                logger.error("The 'env_variables' parameter must be a dictionary and will be ignored")
            else:
                self._get_env_variable_names(_env_variables_from_arg)

        # Check for custom environment variable names provided within the helper settings (or environment-specific)
        elif const.HELPER_SETTINGS.ENV_VARIABLES in self._helper_settings:
            self._get_env_variable_names(self._helper_settings.get(const.HELPER_SETTINGS.ENV_VARIABLES, {}))

        # Check for environment-specific variable names or use the default
        else:
            self._get_env_variable_names()

    def _get_env_variable_names(self, _custom_dict: Optional[Mapping[str, str]] = None) -> None:
        """Return the environment variable names to use when checking the OS for environment variables."""
        # Define the dictionary with the default environment variable names
        _env_variable_names = dict(const.HELPER_SETTINGS.ENV_VARIABLE_DEFAULT_MAPPING)

        # Update the environment variables to be specific to an environment is one has been defined
        if self.env:
            _env_specific_names = {}
            for _name_key, _name_value in _env_variable_names.items():
                try:
                    _env_specific_value = core_utils.get_env_variable_name_by_environment(_name_key, self.env)
                    _env_specific_names[_name_key] = _env_specific_value
                except Exception as _exc:
                    _exc_type = core_utils.get_exception_type(_exc)
                    _error_msg = (
                        f"Failed to retrieve the '{_name_key}' environment variable name specific to the "
                        f'{self.env} environment due to {_exc_type} exception: {_exc}'
                    )
                    logger.exception(_error_msg)
                    logger.warning(f"Defaulting to the environment variable {_name_value} for '{_name_key}'")
                    _env_specific_names[_name_key] = _name_value
            _env_variable_names.update(_env_specific_names)

        # Update the dictionary to use any defined custom names instead of the default (or env-specific) names
        if _custom_dict and not isinstance(_custom_dict, Mapping):
            _error_msg = 'Unable to parse custom environment variable names because variable is not a dictionary'
            logger.error(_error_msg)
            raise TypeError(_error_msg)
        if _custom_dict:
            for _name_key, _name_value in _custom_dict.items():
                if _name_key in _env_variable_names:
                    _env_variable_names[_name_key] = _name_value
                else:
                    _warn_msg = f"'{_name_key}' is not a recognized environment variable identifier and will be ignored"
                    logger.warning(_warn_msg)

        # Return the finalized dictionary with the mapped environment variable names
        self._env_variable_names = _env_variable_names

    def _get_env_variables(self):
        """Retrieve any defined environment variables to use with the instantiated core object."""
        _env_variables = {}
        for _config_name, _var_name in self._env_variable_names.items():
            _var_value = os.getenv(_var_name)  # Returns None if not found
            _env_variables.update({_config_name: _var_value})
        self._env_variables = _env_variables

    def _define_strict_mode(self, _strict_mode_from_arg: Optional[bool]) -> None:
        """Define the strict_mode setting using a passed argument, helper setting, or environment variable."""
        setting = const.CLIENT_SETTINGS.STRICT_MODE
        methods = const.ARGUMENT_VALUES.PROVIDED_METHODS  # arg, helper, or env
        debug_msg = const._LOG_MESSAGES._CLIENT_SETTING_CONFIGURED
        default_debug_msg = const._LOG_MESSAGES._WILL_USE_DEFAULT_VALUE

        # Check if the strict_mode value was passed as an argument
        if _strict_mode_from_arg is not None:
            if not isinstance(_strict_mode_from_arg, bool):
                _error_msg = const._LOG_MESSAGES._MUST_BE_DATA_TYPE_ERROR.format(param=setting, data_type='bool')
                logger.error(_error_msg)
                raise TypeError(_error_msg)
            self.strict_mode = _strict_mode_from_arg
            logger.debug(debug_msg.format(setting=setting, value=self.strict_mode, method=methods[0]))

        # Check the helper settings to see if strict mode was defined
        elif (
            self._helper_settings
            and const.HELPER_SETTINGS.STRICT_MODE in self._helper_settings
            and isinstance(self._helper_settings[const.HELPER_SETTINGS.STRICT_MODE], bool)
            and self._helper_settings[const.HELPER_SETTINGS.STRICT_MODE] is not None
        ):
            self.strict_mode = self._helper_settings.get(const.HELPER_SETTINGS.STRICT_MODE)
            logger.debug(debug_msg.format(setting=setting, value=self.strict_mode, method=methods[1]))

        # Check the environment variables to see if strict mode was defined
        elif (
            const.ENV_VARIABLES.STRICT_MODE_FIELD in self._env_variables
            and isinstance(self._env_variables[const.ENV_VARIABLES.STRICT_MODE_FIELD], bool)
            and self._env_variables[const.ENV_VARIABLES.STRICT_MODE_FIELD] is not None
        ):
            self.strict_mode = self._env_variables.get(const.ENV_VARIABLES.STRICT_MODE_FIELD)
            logger.debug(debug_msg.format(setting=setting, value=self.strict_mode, method=methods[2]))

        # Use the default value (True) if not strict mode was not explicitly defined
        else:
            self.strict_mode = const.DEFAULT_STRICT_MODE
            logger.debug(default_debug_msg.format(setting=setting, value=self.strict_mode))

    def _check_for_connection_type_mismatch(self):
        if self.legacy_key_material and self.connection_type == const.CONNECTION_INFO.OAUTH:
            _warn_msg = (
                'Legacy key material was provided but will be ignored as the connection_type was explicitly defined as OAuth'
            )
            # TODO: Call method for displaying warnings when a related setting is enabled
            logger.warning(_warn_msg)

    def _has_complete_legacy_connection_info(self) -> bool:
        """Return whether current connection info has the required legacy credentials."""
        _legacy_info = self.connection_info.get(const.CONNECTION_INFO.LEGACY, {})
        if not isinstance(_legacy_info, dict):
            return False
        _has_access_id = bool(_legacy_info.get(const.CONNECTION_INFO.LEGACY_ACCESS_ID))
        _has_private_key = bool(
            _legacy_info.get(const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE)
            or _legacy_info.get(const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PEM)
        )
        return _has_access_id and _has_private_key

    def _has_complete_oauth_connection_info(self) -> bool:
        """Return whether current connection info has the required OAuth credentials."""
        _oauth_info = self.connection_info.get(const.CONNECTION_INFO.OAUTH, {})
        if not isinstance(_oauth_info, dict):
            return False
        _has_issuer_url = bool(_oauth_info.get(const.CONNECTION_INFO.OAUTH_ISSUER_URL))
        _has_client_id = bool(_oauth_info.get(const.CONNECTION_INFO.OAUTH_CLIENT_ID))
        _has_scope = bool(_oauth_info.get(const.CONNECTION_INFO.OAUTH_SCOPE))
        _has_private_key = bool(
            _oauth_info.get(const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_FILE)
            or _oauth_info.get(const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK)
        )
        return _has_issuer_url and _has_client_id and _has_scope and _has_private_key

    def _get_connection_type(self, _connection_type_from_arg: Optional[str]) -> None:
        """Define the connection type that should be used to authenticate to the RSA ID Plus tenant."""
        self.connection_type = None
        setting = const.CLIENT_SETTINGS.CONNECTION_TYPE
        methods = const.ARGUMENT_VALUES.PROVIDED_METHODS  # arg, helper, or env
        debug_msg = const._LOG_MESSAGES._CLIENT_SETTING_CONFIGURED

        # Check if the connection type was passed as an argument and leverage it if valid
        if _connection_type_from_arg is not None:
            if _connection_type_from_arg in const.CONNECTION_INFO.VALID_CONNECTION_TYPES:
                self.connection_type = _connection_type_from_arg
                logger.debug(debug_msg.format(setting=setting, value=self.connection_type, method=methods[0]))
            else:
                _error_msg = const._LOG_MESSAGES._INVALID_ARG_IGNORE.format(arg=setting)
                _expected_types = ','.join(const.CONNECTION_INFO.VALID_CONNECTION_TYPES)
                _error_msg += f' (Expected: {_expected_types}; Provided: {_connection_type_from_arg})'
                logger.error(_error_msg)

        # Attempt to retrieve the connection type via helper settings if present and populated
        if (
            not self.connection_type
            and self._helper_settings
            and const.HELPER_SETTINGS.CONNECTION_TYPE in self._helper_settings
            and self._helper_settings[const.HELPER_SETTINGS.CONNECTION_TYPE] is not None
        ):
            _helper_connection_type = self._helper_settings.get(const.HELPER_SETTINGS.CONNECTION_TYPE)
            if _helper_connection_type in const.CONNECTION_INFO.VALID_CONNECTION_TYPES:
                self.connection_type = _helper_connection_type
                logger.debug(debug_msg.format(setting=setting, value=self.connection_type, method=methods[1]))
            else:
                _error_msg = 'The connection_type value in the helper settings is invalid and will be ignored'
                _expected_types = ','.join(const.CONNECTION_INFO.VALID_CONNECTION_TYPES)
                _error_msg += f' (Expected: {_expected_types}; Provided: {_helper_connection_type})'
                logger.error(_error_msg)

        # Attempt to retrieve the connection type via environment variable if defined
        if (
            not self.connection_type
            and self._env_variables
            and const.ENV_VARIABLES.CONNECTION_TYPE_FIELD in self._env_variables
            and self._env_variables[const.ENV_VARIABLES.CONNECTION_TYPE_FIELD] is not None
        ):
            _env_connection_type = self._env_variables[const.ENV_VARIABLES.CONNECTION_TYPE_FIELD]
            if _env_connection_type in const.CONNECTION_INFO.VALID_CONNECTION_TYPES:
                self.connection_type = _env_connection_type
                logger.debug(debug_msg.format(setting=setting, value=self.connection_type, method=methods[2]))
            else:
                _error_msg = 'The connection_type environment variable is invalid and will be ignored'
                _expected_types = ','.join(const.CONNECTION_INFO.VALID_CONNECTION_TYPES)
                _error_msg += f' (Expected: {_expected_types}; Provided: {_env_connection_type})'
                logger.error(_error_msg)

        # Explicit/declared connection type wins over auto-detection
        if self.connection_type:
            self._check_for_connection_type_mismatch()
            return

        # Auto-detect connection type based on complete credential sets
        if self._has_complete_oauth_connection_info():
            self.connection_type = const.CONNECTION_INFO.OAUTH
            logger.info("The 'oauth' connection_type was selected automatically based on provided OAuth credentials")
            return
        if self._has_complete_legacy_connection_info():
            self.connection_type = const.CONNECTION_INFO.LEGACY
            logger.info("The 'legacy' connection_type was selected automatically based on provided legacy credentials")
            return

        # Fallback to default when no complete credential set is detected.
        self.connection_type = const.CONNECTION_INFO.DEFAULT_CONNECTION_TYPE
        logger.info(
            f"The default connection_type '{const.CONNECTION_INFO.DEFAULT_CONNECTION_TYPE}' will be used "
            'as a complete credential set could not be auto-detected'
        )

    def _get_verify_ssl_setting(self, _verify_ssl_from_arg: Optional[bool]) -> None:
        """Determine the ``verify_ssl`` value from a passed argument, helper setting, or environment variable."""
        setting = const.CLIENT_SETTINGS.VERIFY_SSL
        methods = const.ARGUMENT_VALUES.PROVIDED_METHODS  # arg, helper, or env
        debug_msg = const._LOG_MESSAGES._CLIENT_SETTING_CONFIGURED
        default_debug_msg = const._LOG_MESSAGES._WILL_USE_DEFAULT_VALUE

        # Define the verify_ssl value using the argument if defined
        if _verify_ssl_from_arg is not None and isinstance(_verify_ssl_from_arg, bool):
            self.verify_ssl = _verify_ssl_from_arg
            logger.debug(debug_msg.format(setting=setting, value=self.verify_ssl, method=methods[0]))

        # Attempt to define the verify_ssl value using Helper Settings if present and populated
        elif (
            self._helper_settings
            and const.HELPER_SETTINGS.VERIFY_SSL in self._helper_settings
            and self._helper_settings[const.HELPER_SETTINGS.VERIFY_SSL] is not None
        ):
            self.verify_ssl = self._helper_settings.get(
                const.HELPER_SETTINGS.VERIFY_SSL,
                const.CLIENT_SETTINGS.DEFAULT_VERIFY_SSL_VALUE,  # Fallback value
            )
            logger.debug(debug_msg.format(setting=setting, value=self.verify_ssl, method=methods[1]))

        # Attempt to define the verify_ssl value using an environment variable if defined
        elif (
            self._env_variables
            and const.ENV_VARIABLES.VERIFY_SSL_FIELD in self._env_variables
            and self._env_variables[const.ENV_VARIABLES.VERIFY_SSL_FIELD] is not None
        ):
            self.verify_ssl = self._env_variables.get(
                const.ENV_VARIABLES.VERIFY_SSL_FIELD,
                const.CLIENT_SETTINGS.DEFAULT_VERIFY_SSL_VALUE,  # Fallback value
            )
            logger.debug(debug_msg.format(setting=setting, value=self.verify_ssl, method=methods[2]))

        # Use the default value (True) if not defined elsewhere
        else:
            self.verify_ssl = const.CLIENT_SETTINGS.DEFAULT_VERIFY_SSL_VALUE
            logger.debug(default_debug_msg.format(setting=setting, value=self.verify_ssl))

    def _define_oauth_api_type(self, _oauth_api_type_from_arg: Optional[str]) -> None:
        """Define which API type should be used for OAuth issuer URL inference."""
        setting = const.CLIENT_SETTINGS.OAUTH_API_TYPE
        methods = const.ARGUMENT_VALUES.PROVIDED_METHODS  # arg, helper, or env
        debug_msg = const._LOG_MESSAGES._CLIENT_SETTING_CONFIGURED
        default_debug_msg = const._LOG_MESSAGES._WILL_USE_DEFAULT_VALUE

        if _oauth_api_type_from_arg is not None:
            if not isinstance(_oauth_api_type_from_arg, str):
                _error_msg = (
                    f"The '{setting}' argument is an invalid data type "
                    f'(Expected: str, Provided: {type(_oauth_api_type_from_arg)})'
                )
                logger.error(_error_msg)
                raise TypeError(_error_msg)
            _oauth_api_type = _oauth_api_type_from_arg.strip().lower()
            if _oauth_api_type not in const.VALID_API_TYPES:
                _valid_values = ','.join(sorted(const.VALID_API_TYPES))
                _error_msg = f"The '{setting}' value '{_oauth_api_type_from_arg}' is invalid (Expected one of: {_valid_values})"
                logger.error(_error_msg)
                raise ValueError(_error_msg)
            self.oauth_api_type = _oauth_api_type
            logger.debug(debug_msg.format(setting=setting, value=self.oauth_api_type, method=methods[0]))
            return

        self.oauth_api_type = const.AUTH_API_TYPE
        logger.debug(default_debug_msg.format(setting=setting, value=self.oauth_api_type))

    def _construct_base_url_with_tenant_name(self, _api_type: str, _tenant_name: Optional[str] = None) -> str:
        """Construct the base URL for a given API type using a tenant name."""
        # Ensure the tenant name is defined
        if not _tenant_name:
            if self.tenant_name:
                _tenant_name = self.tenant_name
            else:
                _error_msg = 'A tenant name must be defined or specified to construct a base URL'
                logger.error(_error_msg)
                raise errors.exceptions.MissingRequiredDataError(_error_msg)

        # Construct the appropriate URL based on the provided API type
        if _api_type == const.ADMIN_API_TYPE:
            _base_url = const.URLS.BASE_ADMIN_URL.format(tenant_name=_tenant_name)
        elif _api_type == const.AUTH_API_TYPE:
            _base_url = const.URLS.BASE_AUTH_URL.format(tenant_name=_tenant_name)
        else:
            _error_msg = f"'{_api_type}' is not a valid API type"
            logger.error(_error_msg)
            raise ValueError(_error_msg)

        # Return the constructed base URL
        return _base_url

    def _define_base_url(self, _base_url_from_arg: Optional[str]) -> None:
        """Define the base_url value from user-defined setting or raise an exception if it cannot be defined."""
        # Attempt to define the base URL value for the Administration API by first checking if defined via argument
        setting = const.CLIENT_SETTINGS.BASE_URL
        methods = const.ARGUMENT_VALUES.PROVIDED_METHODS  # arg, helper, or env
        debug_msg = const._LOG_MESSAGES._CLIENT_SETTING_CONFIGURED

        if _base_url_from_arg:
            self.base_url = core_utils.get_base_url(_base_url_from_arg)
            logger.debug(debug_msg.format(setting=setting, value=self.base_url, method=methods[0]))

        # Attempt to define the base URL using the helper settings if defined and populated
        elif (
            self._helper_settings
            and const.HELPER_SETTINGS.BASE_URL in self._helper_settings
            and self._helper_settings[const.HELPER_SETTINGS.BASE_URL]
        ):
            self.base_url = core_utils.get_base_url(self._helper_settings.get(const.HELPER_SETTINGS.BASE_URL))
            logger.debug(debug_msg.format(setting=setting, value=self.base_url, method=methods[1]))

        # Attempt to define the base URL using an environment variable if defined
        elif (
            const.ENV_VARIABLES.BASE_URL_FIELD in self._env_variables and self._env_variables[const.ENV_VARIABLES.BASE_URL_FIELD]
        ):
            self.base_url = core_utils.get_base_url(self._env_variables.get(const.ENV_VARIABLES.BASE_URL_FIELD))
            logger.debug(debug_msg.format(setting=setting, value=self.base_url, method=methods[2]))

        # Set the value to None if the base URL could not be found
        else:
            self.base_url = None

    def _identify_base_url(
        self,
        _api_type: str,
        _base_url_arg: Optional[str] = None,
    ) -> str:
        """Identify the base URL for a specific API type and return the value."""
        # Define the lookup field for the applicable base URL
        _lookup_field = const.HELPER_SETTINGS.API_BASE_URL.format(type=_api_type)

        # Leverage the base URL passed as an argument if defined
        if _base_url_arg:
            _base_url = core_utils.get_base_url(_base_url_arg)

        # Attempt to define the base URL using the helper settings if defined and populated
        elif self._helper_settings and _lookup_field in self._helper_settings and self._helper_settings[_lookup_field]:
            _base_url = core_utils.get_base_url(self._helper_settings.get(_lookup_field))

        # Attempt to define the base URL using an environment variable if defined
        elif _lookup_field in self._env_variables and self._env_variables[_lookup_field]:
            _base_url = core_utils.get_base_url(self._env_variables.get(_lookup_field))

        # Set the value to None if the base URL could not be found
        else:
            _base_url = None

        # Return the base URL value
        return _base_url

    def _define_base_urls(
        self,
        _base_admin_url_arg: Optional[str],
        _base_auth_url_arg: Optional[str],
    ) -> None:
        """Define the base URLs for the Administration API (required)and the Authentication API (optional)."""
        # Attempt to define the admin_base_url value (required)
        self.admin_base_url = self._identify_base_url(const.ADMIN_API_TYPE, _base_admin_url_arg)

        # Leverage the standard base_url value for the admin base URL if the previous attempt returned no result
        if not self.admin_base_url:
            self.admin_base_url = self.base_url

            # Attempt to construct the base URL using the tenant name if the value is still undefined
            if not self.admin_base_url and self.tenant_name:
                self.admin_base_url = self._construct_base_url_with_tenant_name(const.ADMIN_API_TYPE)

            # Raise an exception if a base URL could not be defined
            if not self.admin_base_url:
                _error_msg = (
                    'A base URL for the Administration API must be defined in order to fully '
                    'instantiate the PyDPlus client object'
                )
                logger.error(_error_msg)
                raise errors.exceptions.MissingRequiredDataError(_error_msg)

        # Ensure there is no ending slash at the end of the admin_base_url value
        self.admin_base_url = core_utils.remove_ending_slash(self.admin_base_url)

        # Attempt to define the auth_base_url value (optional)
        self.auth_base_url = self._identify_base_url(const.AUTH_API_TYPE, _base_auth_url_arg)

        # Attempt to construct the base URL using the tenant name if the value is still undefined
        if not self.auth_base_url and self.tenant_name:
            self.auth_base_url = self._construct_base_url_with_tenant_name(const.AUTH_API_TYPE)

        # Attempt to infer the auth base URL from a known admin base URL pattern if still undefined
        if not self.auth_base_url and self.admin_base_url:
            _inferred_auth_base_url = _infer_auth_base_url_from_admin_base_url(self.admin_base_url)
            if _inferred_auth_base_url:
                self.auth_base_url = _inferred_auth_base_url
                logger.debug('The auth_base_url value was inferred from the admin_base_url setting')

        # Log a warning if the Authentication API base URL could not be defined but do not raise an exception
        if not self.auth_base_url:
            _warn_msg = 'The base URL for the Authentication API could not be defined and calls to that API will fail.'
            logger.warning(_warn_msg)
        else:
            # Ensure there is no ending slash at the end of the admin_base_url value
            self.auth_base_url = core_utils.remove_ending_slash(self.auth_base_url)

    def _validate_connection_info(
        self,
        _connection_info: Optional[dict] = None,
        _private_key: Optional[str] = None,
        _legacy_access_id: Optional[str] = None,
        _oauth_client_id: Optional[str] = None,
        _oauth_issuer_url: Optional[str] = None,
        _oauth_private_key: Optional[str] = None,
        _oauth_private_key_jwk: Union[Optional[dict], Optional[str]] = None,
        _oauth_scope: Union[Optional[str], Optional[tuple], Optional[list], Optional[set], Optional[frozenset]] = None,
        _oauth_scope_preset: Union[Optional[str], Optional[tuple[str]], Optional[list[str]], Optional[set[str]]] = None,
        _legacy_key_material: Optional[IDPlusLegacyKeyMaterial] = None,
    ) -> None:
        """Check for provided connection info and define the class object attribute."""
        if _legacy_key_material and not _legacy_access_id:
            _legacy_access_id = _legacy_key_material.access_id

        if not _connection_info:
            # Check for individual parameters defined in object instantiation
            _connection_info = compile_connection_info(
                base_url=self.base_url,
                admin_base_url=self.admin_base_url,
                auth_base_url=self.auth_base_url,
                oauth_api_type=self.oauth_api_type,
                private_key=_private_key,
                legacy_access_id=_legacy_access_id,
                oauth_client_id=_oauth_client_id,
                oauth_issuer_url=_oauth_issuer_url,
                oauth_private_key=_oauth_private_key,
                oauth_private_key_jwk=_oauth_private_key_jwk,
                oauth_scope_preset=_oauth_scope_preset,
                oauth_scope=_oauth_scope,
            )

            # Check for defined helper settings
            if self._helper_settings:
                _helper_connection_info = self._parse_helper_connection_info()
                _connection_info = self._merge_connection_variables(_connection_info, _helper_connection_info)

            # Check for defined environment variables
            if self._env_variables:
                _env_connection_info = self._parse_env_connection_info()
                _connection_info = self._merge_connection_variables(_connection_info, _env_connection_info)

            _connection_info = self._define_oauth_scope_from_presets(
                _connection_info=_connection_info,
                _oauth_scope_preset_from_arg=_oauth_scope_preset,
            )

            # Add missing field values where possible and when needed
            _connection_info = self._populate_missing_connection_details(_connection_info)

        # Merge parsed legacy key material into connection info when available
        if _legacy_key_material:
            _connection_info = self._merge_legacy_key_material(_connection_info, _legacy_key_material)
        self.connection_info = _connection_info

    @staticmethod
    def _merge_legacy_key_material(
        _connection_info: Optional[dict],
        _legacy_key_material: IDPlusLegacyKeyMaterial,
    ) -> dict:
        """Merge legacy key material into connection info without overriding explicit file-path values."""
        if not _connection_info:
            _connection_info = dict(const.CONNECTION_INFO.EMPTY_CONNECTION_INFO)

        _legacy_section = dict(_connection_info.get(const.CONNECTION_INFO.LEGACY, {}))
        if not _legacy_section.get(const.CONNECTION_INFO.LEGACY_ACCESS_ID):
            _legacy_section[const.CONNECTION_INFO.LEGACY_ACCESS_ID] = _legacy_key_material.access_id

        _has_explicit_key_file = bool(_legacy_section.get(const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE))
        if not _has_explicit_key_file:
            _legacy_section[const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PEM] = _legacy_key_material.access_key_pem

        _connection_info[const.CONNECTION_INFO.LEGACY] = _legacy_section
        return _connection_info

    def _parse_helper_connection_info(self) -> dict[str, dict[str, Any]]:
        """Parse the helper content to populate the connection info."""
        _helper_connection = self._helper_settings.get(const.HELPER_SETTINGS.CONNECTION, {})
        _helper_connection_info: dict[str, dict[str, Any]] = {}
        for _section, _key_list in const.CONNECTION_INFO.CONNECTION_FIELDS.items():
            _section_data = _helper_connection.get(_section, {})
            _helper_connection_info[_section] = {_key: _section_data.get(_key) for _key in _key_list}
        return _helper_connection_info

    def _parse_env_connection_info(self) -> dict[str, dict[str, Any]]:
        """Parse environment variable definitions into the connection info dictionary."""
        _env_connection_info: dict[str, dict[str, Any]] = {}

        for _section, _field_mapping in (
            (const.CONNECTION_INFO.LEGACY, const.HELPER_SETTINGS.ENV_LEGACY_CONNECTION_MAPPING),
            (const.CONNECTION_INFO.OAUTH, const.HELPER_SETTINGS.ENV_OAUTH_CONNECTION_MAPPING),
        ):
            _env_connection_info[_section] = {
                _connection_field: self._env_variables.get(_env_variable_field)
                for _connection_field, _env_variable_field in _field_mapping.items()
            }

        return _env_connection_info

    @staticmethod
    def _parse_oauth_scope_preset_values(
        _oauth_scope_preset: Union[Optional[str], Optional[tuple[str]], Optional[list[str]], Optional[set[str]]],
    ) -> list[str]:
        """Parse OAuth scope preset values into a normalized list."""
        if _oauth_scope_preset is None:
            return []

        _parsed_preset_values: list[str] = []
        if isinstance(_oauth_scope_preset, str):
            _parsed_preset_values.extend(_oauth_scope_preset.replace('+', ' ').replace(',', ' ').split())
            return _parsed_preset_values

        if isinstance(_oauth_scope_preset, Iterable):
            for _scope_preset_value in _oauth_scope_preset:
                if not isinstance(_scope_preset_value, str):
                    _error_msg = (
                        f"The 'oauth_scope_preset' values must be strings (provided element type: {type(_scope_preset_value)})"
                    )
                    logger.error(_error_msg)
                    raise TypeError(_error_msg)
                _parsed_preset_values.extend(_scope_preset_value.replace('+', ' ').replace(',', ' ').split())
            return _parsed_preset_values

        _error_msg = (
            "The 'oauth_scope_preset' value must be supplied as a string or iterable of strings "
            f'(provided: {type(_oauth_scope_preset)})'
        )
        logger.error(_error_msg)
        raise TypeError(_error_msg)

    def _define_oauth_scope_from_presets(
        self,
        _connection_info: dict[str, dict[str, Any]],
        _oauth_scope_preset_from_arg: Union[Optional[str], Optional[tuple[str]], Optional[list[str]], Optional[set[str]]],
    ) -> dict[str, dict[str, Any]]:
        """Define OAuth scopes by merging explicit scopes with any presets from all supported sources."""
        _combined_scope_presets: list[str] = []
        _seen_scope_presets: set[str] = set()
        _helper_scope_preset = None
        if (
            const.HELPER_SETTINGS.CONNECTION in self._helper_settings
            and isinstance(self._helper_settings[const.HELPER_SETTINGS.CONNECTION], dict)
            and const.CONNECTION_INFO.OAUTH in self._helper_settings[const.HELPER_SETTINGS.CONNECTION]
            and isinstance(self._helper_settings[const.HELPER_SETTINGS.CONNECTION][const.CONNECTION_INFO.OAUTH], dict)
        ):
            _helper_oauth = self._helper_settings[const.HELPER_SETTINGS.CONNECTION][const.CONNECTION_INFO.OAUTH]
            _helper_scope_preset = _helper_oauth.get(const.HELPER_SETTINGS.OAUTH_SCOPE_PRESET)
            if _helper_scope_preset is None:
                _helper_scope_preset = _helper_oauth.get(const.HELPER_SETTINGS.LEGACY_OAUTH_SCOPE_PRESET)

        # Fallback for any helper settings parsed with older root-level field names.
        if _helper_scope_preset is None:
            _helper_scope_preset = self._helper_settings.get(const.HELPER_SETTINGS.LEGACY_OAUTH_SCOPE_PRESET)

        for _scope_preset_values in (
            _oauth_scope_preset_from_arg,
            _helper_scope_preset,
            self._env_variables.get(const.ENV_VARIABLES.OAUTH_SCOPE_PRESET_FIELD),
        ):
            for _scope_preset_value in self._parse_oauth_scope_preset_values(_scope_preset_values):
                _normalized_scope_preset_value = _scope_preset_value.strip().lower()
                if _normalized_scope_preset_value and _normalized_scope_preset_value not in _seen_scope_presets:
                    _combined_scope_presets.append(_normalized_scope_preset_value)
                    _seen_scope_presets.add(_normalized_scope_preset_value)

        if not _combined_scope_presets:
            return _connection_info

        _oauth_section = _connection_info.get(const.CONNECTION_INFO.OAUTH, {})
        _existing_scope = _oauth_section.get(const.CONNECTION_INFO.OAUTH_SCOPE)
        _merged_oauth_scope = auth._get_scope_from_preset(_combined_scope_presets, _existing_scope)
        _oauth_section[const.CONNECTION_INFO.OAUTH_SCOPE] = core_utils.normalize_oauth_scope(_merged_oauth_scope)
        _connection_info[const.CONNECTION_INFO.OAUTH] = _oauth_section
        return _connection_info

    @staticmethod
    def _merge_connection_variables(
        _defined_info: Optional[Mapping[str, Mapping[str, Any]]] = None,
        _supplemental_info: Optional[Mapping[str, Mapping[str, Any]]] = None,
    ) -> dict[str, dict[str, Any]]:
        """Merge explicit connection values with supplemental helper or environment values."""
        _merged_connection_info: dict[str, dict[str, Any]] = {}

        for _section, _key_list in const.CONNECTION_INFO.CONNECTION_FIELDS.items():
            _defined_section = _defined_info.get(_section, {}) if _defined_info else {}
            _supplemental_section = _supplemental_info.get(_section, {}) if _supplemental_info else {}

            _merged_connection_info[_section] = {
                _key: (
                    _defined_section[_key]
                    if _key in _defined_section and _defined_section[_key] is not None
                    else _supplemental_section.get(_key)
                )
                for _key in _key_list
            }

        return _merged_connection_info

    def _populate_missing_connection_details(self, _partial_connection_info: dict) -> dict:
        """Add missing field values the connection info dictionary as needed."""
        # Define variables for the dictionary keys/fields
        _issuer_url_key = const.CONNECTION_INFO.OAUTH_ISSUER_URL
        _oauth_key = const.CONNECTION_INFO.OAUTH
        _grant_type_key = const.CONNECTION_INFO.OAUTH_GRANT_TYPE
        _client_auth_key = const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION
        if self.oauth_api_type == const.AUTH_API_TYPE:
            _issuer_base_url = self.auth_base_url if self.auth_base_url else self.admin_base_url
        else:
            _issuer_base_url = self.admin_base_url if self.admin_base_url else self.auth_base_url
        if not _issuer_base_url:
            _issuer_base_url = self.base_url

        # Populate the Issuer URL value for OAuth connections if not defined
        if (
            _issuer_url_key not in _partial_connection_info[_oauth_key]
            or not _partial_connection_info[_oauth_key][_issuer_url_key]
        ) and _issuer_base_url is not None:
            _partial_connection_info[_oauth_key][_issuer_url_key] = const.URLS.OAUTH.format(base_url=_issuer_base_url)

        # Populate the Grant Type value for OAuth connections if not defined
        if (
            _grant_type_key not in _partial_connection_info[_oauth_key]
            or not _partial_connection_info[_oauth_key][_grant_type_key]
        ):
            _partial_connection_info[_oauth_key][_grant_type_key] = const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE

        # Populate the Client Authentication value for OAuth connections if not defined
        if (
            _client_auth_key not in _partial_connection_info[_oauth_key]
            or not _partial_connection_info[_oauth_key][_client_auth_key]
        ):
            _partial_connection_info[_oauth_key][_client_auth_key] = const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH

        # Return the updated connection info dictionary
        return _partial_connection_info

    def _ensure_oauth_headers(self, force_refresh: bool = False) -> dict[str, str]:
        """Ensure valid OAuth headers are available for Administration API calls."""
        if self.connection_type != const.CONNECTION_INFO.OAUTH:
            return self.base_headers
        base_headers, self._oauth_token_data = auth.get_oauth_headers(
            connection_info=self.connection_info,
            verify_ssl=self.verify_ssl,
            token_data=self._oauth_token_data,
            force_refresh=force_refresh,
        )
        self.base_headers = base_headers
        return base_headers

    def refresh_oauth_token(self) -> dict[str, str]:
        """Force refresh the OAuth access token and return updated base headers."""
        return self._ensure_oauth_headers(force_refresh=True)

    def _check_if_connected(self) -> None:
        """Check to see if the object is connected to the tenant and raises an exception if not."""
        if not self.connected:
            _error_msg = 'Must be connected to the tenant before performing an API call. Call the connect() method.'
            logger.error(_error_msg)
            raise errors.exceptions.APIConnectionError(_error_msg)

    def connect(self) -> Tuple[bool, dict[str, str]]:
        """Connect to the RSA ID Plus tenant using the Legacy API or OAuth method.

        :returns: Boolean value indicating if connection was established and dictionary with base API headers
        :raises: :py:exc:`errors.exceptions.APIConnectionError`,
                 :py:exc:`errors.exceptions.FeatureNotConfiguredError`
        """
        base_headers = self.base_headers
        connected = self.connected
        if connected and self.connection_type != const.CLIENT_SETTINGS.CONNECTION_TYPE_OAUTH:
            logger.debug('The client is already connected to the RSA ID Plus tenant')
            return connected, base_headers

        if self.connection_type == const.CLIENT_SETTINGS.CONNECTION_TYPE_LEGACY:
            # Connect to the tenant using the legacy API method
            try:
                base_headers = auth.get_legacy_headers(base_url=self.base_url, connection_info=self.connection_info)
                self._oauth_token_data = None
                connected = True
            except Exception as exc:
                exc_type = type(exc).__name__
                error_msg = f'Failed to connect using Legacy API due to the following {exc_type} exception: {exc}'
                logger.error(error_msg)
                raise errors.exceptions.APIConnectionError(error_msg)
        elif self.connection_type == const.CLIENT_SETTINGS.CONNECTION_TYPE_OAUTH:
            # Connect to the tenant using the OAuth method
            try:
                base_headers = self._ensure_oauth_headers(force_refresh=connected)
                connected = True
            except Exception as exc:
                exc_type = type(exc).__name__
                error_msg = f'Failed to connect using OAuth due to the following {exc_type} exception: {exc}'
                logger.error(error_msg)
                raise errors.exceptions.APIConnectionError(error_msg)
        else:
            error_msg = f"Unsupported connection_type '{self.connection_type}'"
            logger.error(error_msg)
            raise errors.exceptions.APIConnectionError(error_msg)
        return connected, base_headers

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_type: str = const.ADMIN_API_TYPE,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
    ):
        """Perform a GET request against the ID Plus tenant.

        :param endpoint: The API endpoint to query
        :type endpoint: str
        :param params: The query parameters (where applicable)
        :type params: dict, None
        :param headers: Specific API headers to use when performing the API call (beyond the base headers)
        :type headers: dict, None
        :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
        :type api_type: str
        :param timeout: The timeout period in seconds (defaults to ``30``)
        :type timeout: int
        :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
        :type show_full_error: bool
        :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
        :type return_json: bool
        :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                      (If not explicitly defined then ``True`` if Strict Mode is disabled)
        :type allow_failed_response: bool, None
        :returns: The API response in JSON format or as a ``requests`` object
        :raises: :py:exc:`errors.exceptions.APIConnectionError`,
                 :py:exc:`errors.exceptions.APIRequestError`,
                 :py:exc:`errors.exceptions.APIResponseConversionError`,
                 :py:exc:`errors.exceptions.InvalidFieldError`
        """
        self._check_if_connected()
        return api.get(
            self,
            endpoint=endpoint,
            params=params,
            headers=headers,
            api_type=api_type,
            timeout=timeout,
            show_full_error=show_full_error,
            return_json=return_json,
            allow_failed_response=allow_failed_response,
        )

    def patch(
        self,
        endpoint: str,
        payload: dict,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_type: str = const.ADMIN_API_TYPE,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
    ):
        """Perform a PATCH call with payload against the ID Plus tenant.

        :param endpoint: The API endpoint to query
        :type endpoint: str
        :param payload: The payload to leverage in the API call
        :type payload: dict
        :param params: The query parameters (where applicable)
        :type params: dict, None
        :param headers: Specific API headers to use when performing the API call (beyond the base headers)
        :type headers: dict, None
        :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
        :type api_type: str
        :param timeout: The timeout period in seconds (defaults to ``30``)
        :type timeout: int
        :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
        :type show_full_error: bool
        :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
        :type return_json: bool
        :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                      (If not explicitly defined then ``True`` if Strict Mode is disabled)
        :type allow_failed_response: bool, None
        :returns: The API response in JSON format or as a ``requests`` object
        :raises: :py:exc:`errors.exceptions.APIConnectionError`,
                 :py:exc:`errors.exceptions.APIMethodError`,
                 :py:exc:`errors.exceptions.APIRequestError`,
                 :py:exc:`errors.exceptions.APIResponseConversionError`,
                 :py:exc:`errors.exceptions.InvalidFieldError`
        """
        self._check_if_connected()
        return api.patch(
            self,
            endpoint=endpoint,
            payload=payload,
            params=params,
            headers=headers,
            api_type=api_type,
            timeout=timeout,
            show_full_error=show_full_error,
            return_json=return_json,
            allow_failed_response=allow_failed_response,
        )

    def post(
        self,
        endpoint: str,
        payload: dict,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_type: str = const.ADMIN_API_TYPE,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
    ):
        """Perform a POST call with payload against the ID Plus tenant.

        :param endpoint: The API endpoint to query
        :type endpoint: str
        :param payload: The payload to leverage in the API call
        :type payload: dict
        :param params: The query parameters (where applicable)
        :type params: dict, None
        :param headers: Specific API headers to use when performing the API call (beyond the base headers)
        :type headers: dict, None
        :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
        :type api_type: str
        :param timeout: The timeout period in seconds (defaults to ``30``)
        :type timeout: int
        :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
        :type show_full_error: bool
        :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
        :type return_json: bool
        :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                      (If not explicitly defined then ``True`` if Strict Mode is disabled)
        :type allow_failed_response: bool, None
        :returns: The API response in JSON format or as a ``requests`` object
        :raises: :py:exc:`errors.exceptions.APIConnectionError`,
                 :py:exc:`errors.exceptions.APIMethodError`,
                 :py:exc:`errors.exceptions.APIRequestError`,
                 :py:exc:`errors.exceptions.APIResponseConversionError`,
                 :py:exc:`errors.exceptions.InvalidFieldError`
        """
        self._check_if_connected()
        return api.post(
            self,
            endpoint=endpoint,
            payload=payload,
            params=params,
            headers=headers,
            api_type=api_type,
            timeout=timeout,
            show_full_error=show_full_error,
            return_json=return_json,
            allow_failed_response=allow_failed_response,
        )

    def put(
        self,
        endpoint: str,
        payload: dict,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_type: str = const.ADMIN_API_TYPE,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
    ):
        """Perform a PUT call with payload against the ID Plus tenant.

        :param endpoint: The API endpoint to query
        :type endpoint: str
        :param payload: The payload to leverage in the API call
        :type payload: dict
        :param params: The query parameters (where applicable)
        :type params: dict, None
        :param headers: Specific API headers to use when performing the API call (beyond the base headers)
        :type headers: dict, None
        :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
        :type api_type: str
        :param timeout: The timeout period in seconds (defaults to ``30``)
        :type timeout: int
        :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
        :type show_full_error: bool
        :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
        :type return_json: bool
        :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                      (If not explicitly defined then ``True`` if Strict Mode is disabled)
        :type allow_failed_response: bool, None
        :returns: The API response in JSON format or as a ``requests`` object
        :raises: :py:exc:`errors.exceptions.APIConnectionError`,
                 :py:exc:`errors.exceptions.APIMethodError`,
                 :py:exc:`errors.exceptions.APIRequestError`,
                 :py:exc:`errors.exceptions.APIResponseConversionError`,
                 :py:exc:`errors.exceptions.InvalidFieldError`
        """
        self._check_if_connected()
        return api.put(
            self,
            endpoint=endpoint,
            payload=payload,
            params=params,
            headers=headers,
            api_type=api_type,
            timeout=timeout,
            show_full_error=show_full_error,
            return_json=return_json,
            allow_failed_response=allow_failed_response,
        )

    class User:
        """Class containing user-related methods."""

        def __init__(self, pydp_object) -> None:
            """Initialize the :py:class:`pydplus.core.PyDPlus.User` inner class object.

            :param pydp_object: The core :py:class:`pydplus.PyDPlus` object
            :type pydp_object: class[pydplus.PyDPlus]
            :returns: None
            """
            self.pydp_object: PyDPlus = pydp_object

        def get_user_details(
            self,
            email: str,
            search_unsynced: Optional[bool] = None,
            timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
            show_full_error: bool = True,
            return_json: bool = True,
            allow_failed_response: Optional[bool] = None,
        ):
            """Retrieve the details for a specific user based on their email address.

            :param email: The email address of the user for whom to retrieve details
            :type email: str
            :param search_unsynced: Indicates if the user search should include unsynchronized users (optional)
            :type search_unsynced: bool, None
            :param timeout: The timeout period in seconds (defaults to ``30``)
            :type timeout: int
            :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
            :type show_full_error: bool
            :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
            :type return_json: bool
            :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                          (If not explicitly defined then ``True`` if Strict Mode is disabled)
            :type allow_failed_response: bool, None
            :returns: The user details in JSON format or the API response as a ``requests`` object
            :raises: :py:exc:`TypeError`,
                     :py:exc:`errors.exceptions.APIConnectionError`,
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`
            """
            self.pydp_object._check_if_connected()
            return users_module.get_user_details(
                self.pydp_object,
                email=email,
                search_unsynced=search_unsynced,
                timeout=timeout,
                show_full_error=show_full_error,
                return_json=return_json,
                allow_failed_response=allow_failed_response,
            )

        def get_user_id(
            self,
            email: Optional[str] = None,
            user_details: Optional[dict] = None,
            search_unsynced: Optional[bool] = None,
            timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
            show_full_error: bool = True,
        ) -> str:
            """Retrieve the User ID associated with a specific user.

            :param email: The email address of the user for whom to retrieve details
            :type email: str, None
            :param user_details: The user details data from the :py:func:`pydplus.users.get_user_details` function
            :type user_details: dict, None
            :param search_unsynced: Indicates if the user search should include unsynchronized users (optional)
            :type search_unsynced: bool, None
            :param timeout: The timeout period in seconds (defaults to ``30``)
            :type timeout: int, str, None
            :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
            :type show_full_error: bool
            :returns: The User ID for the given user as a string (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
                      or an empty string if the User ID could not be retrieved successfully
            :raises: :py:exc:`TypeError`,
                     :py:exc:`errors.exceptions.APIConnectionError`,
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            self.pydp_object._check_if_connected()
            return users_module.get_user_id(
                self.pydp_object,
                email=email,
                user_details=user_details,
                search_unsynced=search_unsynced,
                timeout=timeout,
                show_full_error=show_full_error,
            )

        def enable_user(
            self,
            user_id: str,
            timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
            show_full_error: bool = True,
            return_json: bool = True,
            allow_failed_response: Optional[bool] = None,
        ):
            """Enable a user that is currently disabled.

            :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
            :type user_id: str
            :param timeout: The timeout period in seconds (defaults to ``30``)
            :type timeout: int
            :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
            :type show_full_error: bool
            :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
            :type return_json: bool
            :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                          (If not explicitly defined then ``True`` if Strict Mode is disabled)
            :type allow_failed_response: bool, None
            :returns: The API response in JSON format or as a ``requests`` object
            :raises: :py:exc:`TypeError`,
                     :py:exc:`errors.exceptions.APIConnectionError`,
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            self.pydp_object._check_if_connected()
            return users_module.enable_user(
                self.pydp_object,
                user_id=user_id,
                timeout=timeout,
                show_full_error=show_full_error,
                return_json=return_json,
                allow_failed_response=allow_failed_response,
            )

        def disable_user(
            self,
            user_id: str,
            timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
            show_full_error: bool = True,
            return_json: bool = True,
            allow_failed_response: Optional[bool] = None,
        ):
            """Disable a user that is currently enabled.

            :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
            :type user_id: str
            :param timeout: The timeout period in seconds (defaults to ``30``)
            :type timeout: int
            :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
            :type show_full_error: bool
            :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
            :type return_json: bool
            :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                          (If not explicitly defined then ``True`` if Strict Mode is disabled)
            :type allow_failed_response: bool, None
            :returns: The API response in JSON format or as a ``requests`` object
            :raises: :py:exc:`TypeError`,
                     :py:exc:`errors.exceptions.APIConnectionError`,
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            self.pydp_object._check_if_connected()
            return users_module.disable_user(
                self.pydp_object,
                user_id=user_id,
                timeout=timeout,
                show_full_error=show_full_error,
                return_json=return_json,
                allow_failed_response=allow_failed_response,
            )

        def synchronize_user(
            self,
            user_id: str,
            timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
            show_full_error: bool = True,
            return_json: bool = True,
            allow_failed_response: Optional[bool] = None,
        ):
            """Synchronize the details of a user between an identity source and the Cloud Access Service.

            :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
            :type user_id: str
            :param timeout: The timeout period in seconds (defaults to ``30``)
            :type timeout: int
            :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
            :type show_full_error: bool
            :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
            :type return_json: bool
            :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                          (If not explicitly defined then ``True`` if Strict Mode is disabled)
            :type allow_failed_response: bool, None
            :returns: The API response in JSON format or as a ``requests`` object
            :raises: :py:exc:`TypeError`,
                     :py:exc:`errors.exceptions.APIConnectionError`,
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            self.pydp_object._check_if_connected()
            return users_module.synchronize_user(
                self.pydp_object,
                user_id=user_id,
                timeout=timeout,
                show_full_error=show_full_error,
                return_json=return_json,
                allow_failed_response=allow_failed_response,
            )

        def mark_deleted(
            self,
            user_id: str,
            timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
            show_full_error: bool = True,
            return_json: bool = True,
            allow_failed_response: Optional[bool] = None,
        ):
            """Mark a specific user to be deleted during the next automated bulk deletion process.

            :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
            :type user_id: str
            :param timeout: The timeout period in seconds (defaults to ``30``)
            :type timeout: int
            :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
            :type show_full_error: bool
            :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
            :type return_json: bool
            :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                          (If not explicitly defined then ``True`` if Strict Mode is disabled)
            :type allow_failed_response: bool, None
            :returns: The API response in JSON format or as a ``requests`` object
            :raises: :py:exc:`TypeError`,
                     :py:exc:`errors.exceptions.APIConnectionError`,
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            self.pydp_object._check_if_connected()
            return users_module.mark_deleted(
                self.pydp_object,
                user_id=user_id,
                timeout=timeout,
                show_full_error=show_full_error,
                return_json=return_json,
                allow_failed_response=allow_failed_response,
            )

        def unmark_deleted(
            self,
            user_id: str,
            timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
            show_full_error: bool = True,
            return_json: bool = True,
            allow_failed_response: Optional[bool] = None,
        ):
            """Unmark a specific user that was flagged to be deleted.

            :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
            :type user_id: str
            :param timeout: The timeout period in seconds (defaults to ``30``)
            :type timeout: int, str, None
            :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
            :type show_full_error: bool
            :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
            :type return_json: bool
            :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                          (If not explicitly defined then ``True`` if Strict Mode is disabled)
            :type allow_failed_response: bool, None
            :returns: The API response in JSON format or as a ``requests`` object
            :raises: :py:exc:`TypeError`,
                     :py:exc:`errors.exceptions.APIConnectionError`,
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            self.pydp_object._check_if_connected()
            return users_module.unmark_deleted(
                self.pydp_object,
                user_id=user_id,
                timeout=timeout,
                show_full_error=show_full_error,
                return_json=return_json,
                allow_failed_response=allow_failed_response,
            )


def compile_connection_info(
    base_url: Optional[str] = None,
    admin_base_url: Optional[str] = None,
    private_key: Optional[str] = None,
    legacy_access_id: Optional[str] = None,
    oauth_client_id: Optional[str] = None,
    oauth_private_key: Optional[str] = None,
    oauth_private_key_jwk: Union[Optional[dict], Optional[str]] = None,
    oauth_scope: Union[Optional[str], Optional[tuple], Optional[list], Optional[set], Optional[frozenset]] = None,
    oauth_scope_preset: Union[Optional[str], Optional[tuple[str]], Optional[list[str]], Optional[set[str]]] = None,
    auth_base_url: Optional[str] = None,
    oauth_api_type: Optional[str] = None,
    oauth_issuer_url: Optional[str] = None,
) -> dict:
    """Compile the connection_info dictionary to use when authenticating to the API.

    :param base_url: The base URL to leverage when performing API calls (deprecated and kept for backwards compatibility)
    :type base_url: str, None
    :param admin_base_url: The base URL for the Administration API
    :type admin_base_url: str, None
    :param private_key: The file path to the private key used for legacy API authentication
    :type private_key: str, None
    :param legacy_access_id: The Access ID associated with the Legacy API connection
    :type legacy_access_id: str, None
    :param oauth_client_id: The Client ID associated with the OAuth API connection
    :type oauth_client_id: str, None
    :param oauth_private_key: The file path to the OAuth private-key JWK used for Private Key JWT authentication
    :type oauth_private_key: str, None
    :param oauth_private_key_jwk: The OAuth private-key JWK payload used for Private Key JWT authentication
    :type oauth_private_key_jwk: dict, str, None
    :param oauth_scope: One or more OAuth scopes to request in token requests
                        (``+``-delimited string or iterable of scope strings)
    :type oauth_scope: str, tuple, list, set, frozenset, None
    :param oauth_scope_preset: One or more presets representing groupings of OAuth scopes and permissions
    :type oauth_scope_preset: str, tuple, list, set, None
    :param auth_base_url: The base URL for the Authentication API
    :type auth_base_url: str, None
    :param oauth_api_type: The API type to use when inferring OAuth issuer URL values (``auth`` by default)
    :type oauth_api_type: str, None
    :param oauth_issuer_url: The explicit OAuth issuer URL to use for token requests
    :type oauth_issuer_url: str, None
    :returns: The compiled connection_info dictionary
    :raises: :py:exc:`TypeError`,
             :py:exc:`ValueError`
    """
    # Define the two private key variables if defined
    if private_key and isinstance(private_key, str):
        private_key_path, private_key_file = core_utils.split_file_path(private_key)
    else:
        private_key_path, private_key_file = None, None

    # Define OAuth private-key file path variables if defined
    if oauth_private_key and isinstance(oauth_private_key, str):
        oauth_private_key_path, oauth_private_key_file = core_utils.split_file_path(oauth_private_key)
    else:
        oauth_private_key_path, oauth_private_key_file = None, None

    # Validate the OAuth private key JWK payload when provided
    if oauth_private_key_jwk is not None and not isinstance(oauth_private_key_jwk, (dict, str)):
        _error_msg = (
            "The 'oauth_private_key_jwk' parameter must be supplied as a dictionary or string "
            f'(provided: {type(oauth_private_key_jwk)})'
        )
        logger.error(_error_msg)
        raise TypeError(_error_msg)

    # Define and normalize the OAuth scope
    # TODO: Check the helper settings and environment variables for scope presets
    oauth_scope = auth._get_scope_from_preset(oauth_scope_preset, oauth_scope)
    oauth_scope = core_utils.normalize_oauth_scope(oauth_scope)

    # Prepare the admin_base_url value in order to construct the issuer_url value
    if base_url and admin_base_url:
        if base_url == admin_base_url:
            logger.debug("The 'base_url' argument is not needed if 'admin_base_url' is defined")
        else:
            logger.warning("The 'base_url' and 'admin_base_url' values do not match and the latter will be used")
        admin_base_url = core_utils.get_base_url(admin_base_url)
    elif base_url and not admin_base_url:
        admin_base_url = core_utils.get_base_url(base_url)
    elif admin_base_url:
        admin_base_url = core_utils.get_base_url(admin_base_url)

    # Normalize the auth_base_url value for OAuth issuer inference if defined
    if auth_base_url:
        auth_base_url = core_utils.get_base_url(auth_base_url)

    # Normalize and validate oauth_api_type when provided
    if oauth_api_type is None:
        oauth_api_type = const.AUTH_API_TYPE
    if not isinstance(oauth_api_type, str):
        _error_msg = f"The 'oauth_api_type' parameter must be a string (provided: {type(oauth_api_type)})"
        logger.error(_error_msg)
        raise TypeError(_error_msg)
    oauth_api_type = oauth_api_type.strip().lower()
    if oauth_api_type not in const.VALID_API_TYPES:
        _valid_values = ','.join(sorted(const.VALID_API_TYPES))
        _error_msg = f"The 'oauth_api_type' value '{oauth_api_type}' is invalid (Expected one of: {_valid_values})"
        logger.error(_error_msg)
        raise ValueError(_error_msg)

    # Validate and normalize an explicitly provided OAuth issuer URL if defined
    if oauth_issuer_url is not None and not isinstance(oauth_issuer_url, str):
        _error_msg = f"The 'oauth_issuer_url' parameter must be a string (provided: {type(oauth_issuer_url)})"
        logger.error(_error_msg)
        raise TypeError(_error_msg)
    oauth_issuer_url = oauth_issuer_url.strip() if isinstance(oauth_issuer_url, str) else None
    if oauth_issuer_url:
        _parsed_issuer_url = urllib.parse.urlparse(oauth_issuer_url)
        if not _parsed_issuer_url.netloc or not _parsed_issuer_url.scheme:
            _error_msg = f"The provided OAuth issuer URL '{oauth_issuer_url}' is invalid"
            logger.error(_error_msg)
            raise ValueError(_error_msg)
        issuer_url = core_utils.remove_ending_slash(oauth_issuer_url)
    else:
        # Infer an auth base URL from the admin base URL when the auth URL is not explicitly defined
        if not auth_base_url and admin_base_url:
            auth_base_url = _infer_auth_base_url_from_admin_base_url(admin_base_url)

        # Define the issuer URL and compile the connection info
        if oauth_api_type == const.AUTH_API_TYPE:
            issuer_base_url = auth_base_url if auth_base_url else admin_base_url
        else:
            issuer_base_url = admin_base_url if admin_base_url else auth_base_url
        issuer_url = const.URLS.OAUTH.format(base_url=issuer_base_url) if issuer_base_url else None
    connection_info = {
        const.CONNECTION_INFO.LEGACY: {
            const.CONNECTION_INFO.LEGACY_ACCESS_ID: legacy_access_id,
            const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH: private_key_path,
            const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE: private_key_file,
        },
        const.CONNECTION_INFO.OAUTH: {
            const.CONNECTION_INFO.OAUTH_ISSUER_URL: issuer_url,
            const.CONNECTION_INFO.OAUTH_CLIENT_ID: oauth_client_id,
            const.CONNECTION_INFO.OAUTH_SCOPE: oauth_scope,
            const.CONNECTION_INFO.OAUTH_GRANT_TYPE: const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE,
            const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION: const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH,
            const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_PATH: oauth_private_key_path,
            const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_FILE: oauth_private_key_file,
            const.CONNECTION_INFO.OAUTH_PRIVATE_KEY_JWK: oauth_private_key_jwk,
        },
    }
    return connection_info


def _infer_auth_base_url_from_admin_base_url(_admin_base_url: Optional[str]) -> Optional[str]:
    """Infer an Authentication API base URL from a matching Administration API base URL."""
    if not isinstance(_admin_base_url, str) or not _admin_base_url:
        return None
    try:
        _normalized_admin_base_url = core_utils.get_base_url(_admin_base_url)
    except Exception as _exc:
        _exc_type = core_utils.get_exception_type(_exc)
        _error_msg = f'Failed to infer Authentication API base URL from the Administration due to {_exc_type} exception: {_exc}'
        logger.error(_error_msg)
        return None
    if '.access.' not in _normalized_admin_base_url:
        return None
    return _normalized_admin_base_url.replace('.access.', '.auth.', 1)
