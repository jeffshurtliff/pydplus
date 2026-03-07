# -*- coding: utf-8 -*-
"""
:Module:            pydplus.core
:Synopsis:          This module performs the core operations of the package
:Usage:             ``from pydplus import PyDPlus``
:Example:           ``pydp = PyDPlus()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Mar 2026
"""

from __future__ import annotations

import os
from typing import Any, Optional, Union, Tuple
from collections.abc import Mapping

from . import auth, api, errors
from . import constants as const
from . import users as users_module
from .utils import core_utils, log_utils
from .utils.helper import get_helper_settings

# Initialize logging
logger = log_utils.initialize_logging(__name__)


class PyDPlus(object):
    """Class for the core client object.

    :param connection_info: Dictionary that defines the connection info to use
    :type connection_info: dict, None
    :param connection_type: Determines whether to leverage a(n) ``oauth`` (default) or ``legacy`` connection
    :type connection_type: str, None
    :param base_url: The base URL to leverage when performing API calls
    :type base_url: str, None
    :param private_key: The file path to the private key used for API authentication (OAuth or Legacy)
    :type private_key: str, None
    :param legacy_access_id: The Access ID associated with the Legacy API connection
    :type legacy_access_id: str, None
    :param oauth_client_id: The Client ID associated with the OAuth API connection
    :type oauth_client_id: str, None
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
    :raises: :py:exc:`TypeError`
    """
    # Define the function that initializes the object instance (i.e. instantiates the object)
    def __init__(
            self,
            connection_info: Optional[dict] = None,
            connection_type: Optional[str] = None,
            base_url: Optional[str] = None,
            private_key: Optional[str] = None,
            legacy_access_id: Optional[str] = None,
            oauth_client_id: Optional[str] = None,
            verify_ssl: Optional[bool] = None,
            auto_connect: bool = True,
            strict_mode: Optional[bool] = None,
            env_variables: Optional[dict] = None,
            helper: Union[Optional[str], Optional[tuple], Optional[list], Optional[set], Optional[dict]] = None,
    ):
        """Instantiate the core client object."""
        # Define the initial settings
        self._helper_settings = {}
        self._env_variables = {}
        self.base_headers = {}
        self.connected = False
        self.strict_mode = None

        # Check for a supplied helper file
        if helper:
            # Parse the helper file contents
            if any((isinstance(helper, tuple), isinstance(helper, list), isinstance(helper, set))):
                helper_file_path, helper_file_type = helper
            elif isinstance(helper, str):
                helper_file_path, helper_file_type = (helper, const.HELPER_SETTINGS.DEFAULT_HELPER_FILE_TYPE)
            elif isinstance(helper, dict):
                helper_file_path, helper_file_type = helper.values()
            else:
                error_msg = "The 'helper' argument can only be supplied as string, tuple, list, set or dict."
                logger.error(error_msg)
                raise TypeError(error_msg)
            self.helper_path = helper_file_path
            self._helper_settings = get_helper_settings(helper_file_path, helper_file_type)
        else:
            self._helper_settings = {}

        # Check for custom environment variable names
        if env_variables:
            if not isinstance(env_variables, dict):
                logger.error("The 'env_variables' parameter must be a dictionary and will be ignored.")
            else:
                self._env_variable_names = self._get_env_variable_names(env_variables)
        elif const.HELPER_SETTINGS.ENV_VARIABLES in self._helper_settings:
            self._env_variable_names = self._get_env_variable_names(
                self._helper_settings.get(const.HELPER_SETTINGS.ENV_VARIABLES, {})
            )
        else:
            self._env_variable_names = self._get_env_variable_names()

        # Check for any defined environment variables
        self._env_variables = self._get_env_variables()

        # Determine if strict mode is enabled or disabled
        if strict_mode is not None:
            if not isinstance(strict_mode, bool):
                error_msg = 'The value of the strict_mode parameter must be Boolean.'
                logger.error(error_msg)
                raise TypeError(error_msg)
            self.strict_mode = strict_mode
        elif (self._helper_settings and const.HELPER_SETTINGS.STRICT_MODE in self._helper_settings
                and isinstance(self._helper_settings[const.HELPER_SETTINGS.STRICT_MODE], bool)
                and self._helper_settings[const.HELPER_SETTINGS.STRICT_MODE] is not None):
            self.strict_mode = self._helper_settings.get(const.HELPER_SETTINGS.STRICT_MODE)
        elif (const.HELPER_SETTINGS.STRICT_MODE in self._env_variables
              and isinstance(self._env_variables[const.HELPER_SETTINGS.STRICT_MODE], bool)
              and self._env_variables[const.HELPER_SETTINGS.STRICT_MODE] is not None):
            self.strict_mode = self._env_variables.get(const.HELPER_SETTINGS.STRICT_MODE)
        else:
            self.strict_mode = const.DEFAULT_STRICT_MODE

        # Define the connection type to use
        if connection_type in const.CONNECTION_INFO.VALID_CONNECTION_TYPES:
            self.connection_type = connection_type
        elif (self._helper_settings and const.HELPER_SETTINGS.CONNECTION_TYPE in self._helper_settings
                and self._helper_settings[const.HELPER_SETTINGS.CONNECTION_TYPE] is not None):
            if self._helper_settings.get(const.HELPER_SETTINGS.CONNECTION_TYPE) in const.CONNECTION_INFO.VALID_CONNECTION_TYPES:
                self.connection_type = self._helper_settings.get(const.HELPER_SETTINGS.CONNECTION_TYPE)
            else:
                error_msg = 'The connection_type value in the helper settings in invalid and will be ignored.'
                expected_types = ','.join(const.CONNECTION_INFO.VALID_CONNECTION_TYPES)
                error_msg += (f"(Expected: {expected_types}; "
                              f"Provided: {self._helper_settings.get(const.HELPER_SETTINGS.CONNECTION_TYPE)})")
                logger.error(error_msg)
                self.connection_type = const.CONNECTION_INFO.DEFAULT_CONNECTION_TYPE
        elif (const.HELPER_SETTINGS.CONNECTION_TYPE in self._env_variables
              and self._env_variables[const.HELPER_SETTINGS.CONNECTION_TYPE] is not None):
            if self._env_variables.get(const.HELPER_SETTINGS.CONNECTION_TYPE) in const.CONNECTION_INFO.VALID_CONNECTION_TYPES:
                self.connection_type = self._env_variables.get(const.HELPER_SETTINGS.CONNECTION_TYPE)
            else:
                error_msg = 'The connection_type environment variable in invalid and the default connection type will be used.'
                logger.error(error_msg)
                self.connection_type = const.CONNECTION_INFO.DEFAULT_CONNECTION_TYPE
        else:
            self.connection_type = const.CONNECTION_INFO.DEFAULT_CONNECTION_TYPE

        # Define the verify_ssl value
        if verify_ssl is not None and isinstance(verify_ssl, bool):
            self.verify_ssl = verify_ssl
        elif self._helper_settings and const.HELPER_SETTINGS.VERIFY_SSL in self._helper_settings:
            self.verify_ssl = self._helper_settings.get(const.HELPER_SETTINGS.VERIFY_SSL, True)
        elif self._env_variables and const.HELPER_SETTINGS.VERIFY_SSL in self._env_variables:
            self.verify_ssl = self._env_variables.get(const.HELPER_SETTINGS.VERIFY_SSL, True)
        else:
            self.verify_ssl = True

        # Attempt to define the base URL value
        if base_url:
            self.base_url = core_utils.get_base_url(base_url)
        elif (self._helper_settings and const.HELPER_SETTINGS.BASE_URL in self._helper_settings
                and self._helper_settings.get(const.HELPER_SETTINGS.BASE_URL) is not None):
            self.base_url = core_utils.get_base_url(self._helper_settings.get(const.HELPER_SETTINGS.BASE_URL))
        elif (const.HELPER_SETTINGS.BASE_URL in self._env_variables
              and self._env_variables.get(const.HELPER_SETTINGS.BASE_URL) is not None):
            self.base_url = core_utils.get_base_url(self._env_variables.get(const.HELPER_SETTINGS.BASE_URL))
        else:
            self.base_url = None

        # Raise an exception if a base URL could not be defined
        if not self.base_url:
            error_msg = 'A base URL must be defined in order to instantiate the PyDPlus object.'
            logger.error(error_msg)
            raise errors.exceptions.MissingRequiredDataError(error_msg)

        # Define the Admin API base URL to use in API calls
        # TODO: Ensure the ending slash (or lack thereof) is consistent and use const.URLS for URL paths
        self.admin_base_url = f'{core_utils.ensure_ending_slash(self.base_url)}AdminInterface/restapi'

        # Define the Authentication API base URL to use in API calls
        # Refer to https://community.securid.com/s/article/RSA-SecurID-Authentication-API-Developer-s-Guide pg 15
        # TODO: Ensure the ending slash (or lack thereof) is consistent and use const.URLS for URL paths
        self.auth_base_url = f'{core_utils.ensure_ending_slash(self.base_url)}mfa/v1_1/authn'

        # Check for provided connection info and define the class object attribute
        if not connection_info:
            # Check for individual parameters defined in object instantiation
            connection_info = compile_connection_info(
                base_url=base_url,
                private_key=private_key,
                legacy_access_id=legacy_access_id,
                oauth_client_id=oauth_client_id,
            )

            # Check for defined helper settings
            if self._helper_settings:
                helper_connection_info = self._parse_helper_connection_info()
                connection_info = self._merge_connection_variables(connection_info, helper_connection_info)

            # Check for defined environment variables
            if self._env_variables:
                env_connection_info = self._parse_env_connection_info()
                connection_info = self._merge_connection_variables(connection_info, env_connection_info)

            # Add missing field values where possible and when needed
            connection_info = self._populate_missing_connection_details(connection_info)
        self.connection_info = connection_info

        # Connect to the tenant (if auto-connect is enabled) and retrieve the base API headers
        if auto_connect:
            self.connected, self.base_headers = self.connect()
            # TODO: Figure out how to connect after instantiation and update self.connected and self.base_headers

        # Import inner object classes so their methods can be called from the primary object
        self.users = self._import_user_class()

    def _import_user_class(self):
        """Allow the :py:class:`pydplus.core.PyDPlus.User` class to be utilized within the core object."""
        return PyDPlus.User(self)

    @staticmethod
    def _get_env_variable_names(_custom_dict: Optional[Mapping[str, str]] = None) -> dict:
        """Return the environment variable names to use when checking the OS for environment variables."""
        # Define the dictionary with the default environment variable names
        _env_variable_names = dict(const.HELPER_SETTINGS.ENV_VARIABLE_DEFAULT_MAPPING)

        # Update the dictionary to use any defined custom names instead of the default names
        _custom_dict = {} if _custom_dict is None else _custom_dict
        if not isinstance(_custom_dict, Mapping):
            _error_msg = 'Unable to parse custom environment variable names because variable is not a dictionary.'
            logger.error(_error_msg)
            raise TypeError(_error_msg)
        if _custom_dict:
            for _name_key, _name_value in _custom_dict.items():
                if _name_key in _env_variable_names:
                    _env_variable_names[_name_key] = _name_value

        # Return the finalized dictionary with the mapped environment variable names
        return _env_variable_names

    def _get_env_variables(self):
        """Retrieve any defined environment variables to use with the instantiated core object."""
        _env_variables = {}
        for _config_name, _var_name in self._env_variable_names.items():
            _var_value = os.getenv(_var_name)                               # Returns None if not found
            _env_variables.update({_config_name: _var_value})
        return _env_variables

    def _parse_helper_connection_info(self) -> dict[str, dict[str, Any]]:
        """Parse the helper content to populate the connection info."""
        _helper_connection = self._helper_settings.get(const.HELPER_SETTINGS.CONNECTION, {})
        _helper_connection_info: dict[str, dict[str, Any]] = {}
        for _section, _key_list in const.CONNECTION_INFO.CONNECTION_FIELDS.items():
            _section_data = _helper_connection.get(_section, {})
            _helper_connection_info[_section] = {
                _key: _section_data.get(_key)
                for _key in _key_list
            }
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

    def _populate_missing_connection_details(self, _partial_connection_info):
        """Add missing field values the connection info dictionary as needed."""
        # Define variables for the dictionary keys/fields
        issuer_url_key = const.CONNECTION_INFO.OAUTH_ISSUER_URL
        oauth_key = const.CONNECTION_INFO.OAUTH
        grant_type_key = const.CONNECTION_INFO.OAUTH_GRANT_TYPE
        client_auth_key = const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION

        # Populate the Issuer URL value for OAuth connections if not defined
        if ((issuer_url_key not in _partial_connection_info[oauth_key]
             or not _partial_connection_info[oauth_key][issuer_url_key])
                and self.base_url is not None):
            _partial_connection_info[oauth_key][issuer_url_key] = const.URLS.OAUTH.format(base_url=self.base_url)

        # Populate the Grant Type value for OAuth connections if not defined
        if (grant_type_key not in _partial_connection_info[oauth_key]
                or not _partial_connection_info[oauth_key][grant_type_key]):
            _partial_connection_info[oauth_key][grant_type_key] = const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE

        # Populate the Client Authentication value for OAuth connections if not defined
        if (client_auth_key not in _partial_connection_info[oauth_key][client_auth_key]
                or not _partial_connection_info[oauth_key][client_auth_key]):
            _partial_connection_info[oauth_key][client_auth_key] = const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH

        # Return the updated connection info dictionary
        return _partial_connection_info

    def _check_if_connected(self):
        """Check to see if the object is connected to the tenant and raises an exception if not."""
        if not self.connected:
            error_msg = 'Must be connected to the tenant before performing an API call. Call the connect() method.'
            logger.error(error_msg)
            raise errors.exceptions.APIConnectionError(error_msg)

    def connect(self) -> Tuple[bool, dict[str, str]]:
        """Connect to the RSA ID Plus tenant using the Legacy API or OAuth method.

        :returns: Boolean value indicating if connection was established and dictionary with base API headers
        :raises: :py:exc:`errors.exceptions.APIConnectionError`,
                 :py:exc:`errors.exceptions.FeatureNotConfiguredError`
        """
        base_headers = None
        connected = self.connected
        if connected:
            logger.debug('The client is already connected to the RSA ID Plus tenant.')
        else:
            if self.connection_type == const.CLIENT_SETTINGS.CONNECTION_TYPE_LEGACY:
                # Connect to the tenant using the legacy API method
                try:
                    base_headers = auth.get_legacy_headers(
                        base_url=self.base_url,
                        connection_info=self.connection_info
                    )
                    connected = True
                except Exception as exc:
                    exc_type = type(exc).__name__
                    error_msg = f'Failed to connect using Legacy API due to the following {exc_type} exception: {exc}'
                    logger.error(error_msg)
                    raise errors.exceptions.APIConnectionError(error_msg)
            elif self.connection_type == const.CLIENT_SETTINGS.CONNECTION_TYPE_OAUTH:
                # Connect to the tenant using the OAuth method
                # TODO: Define the base headers using OAuth and establish connection instead of raising an exception
                raise errors.exceptions.FeatureNotConfiguredError('OAuth connections are not currently supported')
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
        return api.get(self, endpoint=endpoint, params=params, headers=headers, api_type=api_type, timeout=timeout,
                       show_full_error=show_full_error, return_json=return_json,
                       allow_failed_response=allow_failed_response)

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
        return api.patch(self, endpoint=endpoint, payload=payload, params=params, headers=headers, api_type=api_type,
                         timeout=timeout, show_full_error=show_full_error, return_json=return_json,
                         allow_failed_response=allow_failed_response)

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
        return api.post(self, endpoint=endpoint, payload=payload, params=params, headers=headers, api_type=api_type,
                        timeout=timeout, show_full_error=show_full_error, return_json=return_json,
                        allow_failed_response=allow_failed_response)

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
        return api.put(self, endpoint=endpoint, payload=payload, params=params, headers=headers, api_type=api_type,
                       timeout=timeout, show_full_error=show_full_error, return_json=return_json,
                       allow_failed_response=allow_failed_response)
    
    class User(object):
        """Class containing user-related methods."""
        def __init__(self, pydp_object):
            """Initialize the :py:class:`pydplus.core.PyDPlus.User` inner class object.

            :param pydp_object: The core :py:class:`pydplus.PyDPlus` object
            :type pydp_object: class[pydplus.PyDPlus]
            """
            self.pydp_object = pydp_object

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
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`
            """
            # TODO: Check to ensure connection to the tenant has already been established
            return users_module.get_user_details(self.pydp_object, email=email, search_unsynced=search_unsynced,
                                                 timeout=timeout, show_full_error=show_full_error,
                                                 return_json=return_json, allow_failed_response=allow_failed_response)

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
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            # TODO: Check to ensure connection to the tenant has already been established
            return users_module.get_user_id(self.pydp_object, email=email, user_details=user_details,
                                            search_unsynced=search_unsynced, timeout=timeout,
                                            show_full_error=show_full_error)

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
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            # TODO: Check to ensure connection to the tenant has already been established
            return users_module.enable_user(self.pydp_object, user_id=user_id, timeout=timeout,
                                            show_full_error=show_full_error, return_json=return_json,
                                            allow_failed_response=allow_failed_response)

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
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            # TODO: Check to ensure connection to the tenant has already been established
            return users_module.disable_user(self.pydp_object, user_id=user_id, timeout=timeout,
                                             show_full_error=show_full_error, return_json=return_json,
                                             allow_failed_response=allow_failed_response)

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
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            # TODO: Check to ensure connection to the tenant has already been established
            return users_module.synchronize_user(self.pydp_object, user_id=user_id, timeout=timeout,
                                                 show_full_error=show_full_error, return_json=return_json,
                                                 allow_failed_response=allow_failed_response)

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
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            # TODO: Check to ensure connection to the tenant has already been established
            return users_module.mark_deleted(self.pydp_object, user_id=user_id, timeout=timeout,
                                             show_full_error=show_full_error, return_json=return_json,
                                             allow_failed_response=allow_failed_response)

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
                     :py:exc:`errors.exceptions.APIMethodError`,
                     :py:exc:`errors.exceptions.APIRequestError`,
                     :py:exc:`errors.exceptions.APIResponseConversionError`,
                     :py:exc:`errors.exceptions.InvalidFieldError`,
                     :py:exc:`errors.exceptions.MissingRequiredDataError`
            """
            # TODO: Check to ensure connection to the tenant has already been established
            return users_module.unmark_deleted(self.pydp_object, user_id=user_id, timeout=timeout,
                                               show_full_error=show_full_error, return_json=return_json,
                                               allow_failed_response=allow_failed_response)


def compile_connection_info(
        base_url: Optional[str],
        private_key: Optional[str],
        legacy_access_id: Optional[str],
        oauth_client_id: Optional[str],
) -> dict:
    """Compile the connection_info dictionary to use when authenticating to the API.

    :param base_url: The base URL to leverage when performing API calls
    :type base_url: str, None
    :param private_key: The file path to the private key used for API authentication (OAuth or Legacy)
    :type private_key: str, None
    :param legacy_access_id: The Access ID associated with the Legacy API connection
    :type legacy_access_id: str, None
    :param oauth_client_id: The Client ID associated with the OAuth API connection
    :type oauth_client_id: str, None
    :returns: The compiled connection_info dictionary
    :raises: :py:exc:`TypeError`
    """
    private_key_path, private_key_file = None, None
    if private_key and isinstance(private_key, str):
        private_key_path, private_key_file = core_utils.split_file_path(private_key)
    base_url = core_utils.get_base_url(base_url) if base_url else base_url
    issuer_url = const.URLS.OAUTH.format(base_url=base_url) if base_url else None
    connection_info = {
        const.CONNECTION_INFO.LEGACY: {
            const.CONNECTION_INFO.LEGACY_ACCESS_ID: legacy_access_id,
            const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_PATH: private_key_path,
            const.CONNECTION_INFO.LEGACY_PRIVATE_KEY_FILE: private_key_file,
        },
        const.CONNECTION_INFO.OAUTH: {
            const.CONNECTION_INFO.OAUTH_ISSUER_URL: issuer_url,
            const.CONNECTION_INFO.OAUTH_CLIENT_ID: oauth_client_id,
            const.CONNECTION_INFO.OAUTH_GRANT_TYPE: const.CONNECTION_INFO.OAUTH_DEFAULT_GRANT_TYPE,
            const.CONNECTION_INFO.OAUTH_CLIENT_AUTHENTICATION: const.CONNECTION_INFO.OAUTH_DEFAULT_CLIENT_AUTH,
        }
    }
    return connection_info
