# -*- coding: utf-8 -*-
"""
:Module:            pydplus.core
:Synopsis:          This module performs the core operations of the package
:Usage:             ``from pydplus import PyDPlus``
:Example:           ``prod = PyDPlus()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Jun 2025
"""

import os
import copy

from . import auth, api, errors
from . import users as users_module
from .utils import core_utils, log_utils
from .utils.helper import get_helper_settings, DEFAULT_HELPER_FILE_TYPE

# Initialize logging
logger = log_utils.initialize_logging(__name__)


class PyDPlus(object):
    """This is the class for the core object leveraged in this module."""
    # Define the function that initializes the object instance (i.e. instantiates the object)
    def __init__(self, connection_info=None, connection_type=None, base_url=None,
                 private_key=None, legacy_access_id=None, oauth_client_id=None, verify_ssl=None, auto_connect=True,
                 env_variables=None, helper=None):
        """This method instantiates the core Salesforce object.

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
        :param env_variables: Optionally define custom environment variable names to use instead of the default names
        :type env_variables: dict, None
        :param helper: The file path of a helper file (when applicable)
        :type helper: str, None
        :returns: The instantiated object
        :raises: :py:exc:`TypeError`
        """
        # Define the default settings
        self._helper_settings = {}
        self._env_variables = {}
        self.base_headers = {}
        self.connected = False

        # Check for a supplied helper file
        if helper:
            # Parse the helper file contents
            if any((isinstance(helper, tuple), isinstance(helper, list), isinstance(helper, set))):
                helper_file_path, helper_file_type = helper
            elif isinstance(helper, str):
                helper_file_path, helper_file_type = (helper, DEFAULT_HELPER_FILE_TYPE)
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
        elif 'env_variables' in self._helper_settings:
            self._env_variable_names = self._get_env_variable_names(self._helper_settings.get('env_variables', {}))
        else:
            self._env_variable_names = self._get_env_variable_names()

        # Check for any defined environment variables
        self._env_variables = self._get_env_variables()

        # Define the connection type to use
        if connection_type in auth.VALID_CONNECTION_TYPES:
            self.connection_type = connection_type
        elif (self._helper_settings and 'connection_type' in self._helper_settings
                and self._helper_settings['connection_type'] is not None):
            if self._helper_settings.get('connection_type') in auth.VALID_CONNECTION_TYPES:
                self.connection_type = self._helper_settings.get('connection_type')
            else:
                logger.error('The connection_type value in the helper settings in invalid and will be ignored.')
                self.connection_type = auth.DEFAULT_CONNECTION_TYPE
        elif 'connection_type' in self._env_variables and self._env_variables['connection_type'] is not None:
            if self._env_variables.get('connection_type') in auth.VALID_CONNECTION_TYPES:
                self.connection_type = self._env_variables.get('connection_type')
            else:
                logger.error('The connection_type environment variable in invalid and will be ignored.')
                self.connection_type = auth.DEFAULT_CONNECTION_TYPE
        else:
            self.connection_type = auth.DEFAULT_CONNECTION_TYPE

        # Define the verify_ssl value
        if verify_ssl is not None and isinstance(verify_ssl, bool):
            self.verify_ssl = verify_ssl
        elif self._helper_settings and 'verify_ssl' in self._helper_settings:
            self.verify_ssl = self._helper_settings.get('verify_ssl', True)
        elif self._env_variables and 'verify_ssl' in self._env_variables:
            self.verify_ssl = self._env_variables.get('verify_ssl', True)
        else:
            self.verify_ssl = True

        # Attempt to define the base URL value
        if base_url:
            self.base_url = core_utils.get_base_url(base_url)
        elif (self._helper_settings and 'base_url' in self._helper_settings
                and self._helper_settings.get('base_url') is not None):
            self.base_url = core_utils.get_base_url(self._helper_settings.get('base_url'))
        elif 'base_url' in self._env_variables and self._env_variables.get('base_url') is not None:
            self.base_url = core_utils.get_base_url(self._env_variables.get('base_url'))
        else:
            self.base_url = None

        # Raise an exception if a base URL could not be defined
        if not self.base_url:
            error_msg = 'A base URL must be defined in order to instantiate the PyDPlus object.'
            logger.error(error_msg)
            raise errors.exceptions.MissingRequiredDataError(error_msg)

        # Define the Admin API base URL to use in API calls
        self.admin_base_url = f'{core_utils.ensure_ending_slash(self.base_url)}AdminInterface/restapi'

        # Define the Authentication API base URL to use in API calls
        # Refer to https://community.securid.com/s/article/RSA-SecurID-Authentication-API-Developer-s-Guide pg 15
        self.auth_base_url = f'{core_utils.ensure_ending_slash(self.base_url)}mfa/v1_1/authn'

        # Check for provided connection info and define the class object attribute
        if not connection_info:
            # Check for individual parameters defined in object instantiation
            connection_info = compile_connection_info(base_url, private_key, legacy_access_id, oauth_client_id)

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
        """This method allows the :py:class:`pydplus.core.PyDPlus.User` class to be utilized in the core object."""
        return PyDPlus.User(self)

    @staticmethod
    def _get_env_variable_names(_custom_dict=None):
        """This function returns the environment variable names to use when checking the OS for environment variables.

        .. versionadded:: 1.0.0
        """
        # Define the dictionary with the default environment variable names
        _env_variable_names = {
            'connection_type': 'PYDPLUS_CONNECTION_TYPE',
            'legacy_access_id': 'PYDPLUS_LEGACY_ACCESS_ID',
            'legacy_key_path': 'PYDPLUS_LEGACY_KEY_PATH',
            'legacy_key_file': 'PYDPLUS_LEGACY_KEY_FILE',
            'oauth_issuer_url': 'PYDPLUS_OAUTH_ISSUER_URL',
            'oauth_client_id': 'PYDPLUS_OAUTH_CLIENT_ID',
            'oauth_grant_type': 'PYDPLUS_OAUTH_GRANT_TYPE',
            'verify_ssl': 'PYDPLUS_VERIFY_SSL',
        }

        # Update the dictionary to use any defined custom names instead of the default names
        _custom_dict = {} if _custom_dict is None else _custom_dict
        if not isinstance(_custom_dict, dict):
            raise TypeError('Unable to parse custom environment variable names because variable is not a dictionary.')
        if _custom_dict:
            for _name_key, _name_value in _custom_dict.items():
                if _name_key in _env_variable_names:
                    _env_variable_names.update({_name_key: _name_value})

        # Return the finalized dictionary with the mapped environment variable names
        return _env_variable_names

    def _get_env_variables(self):
        """This function retrieves any defined environment variables to use with the instantiated core object.

        .. versionadded:: 1.0.0
        """
        _env_variables = {}
        for _config_name, _var_name in self._env_variable_names.items():
            _var_value = os.getenv(_var_name)                               # Returns None if not found
            _env_variables.update({_config_name: _var_value})
        return _env_variables

    def _parse_helper_connection_info(self):
        """This method parses the helper content to populate the connection info.

        .. versionadded:: 1.0.0
        """
        _helper_connection_info = copy.deepcopy(auth.EMPTY_CONNECTION_INFO)
        for _section, _key_list in auth.STRUCTURED_CONNECTION_FIELDS.items():
            for _key in _key_list:
                if _key in self._helper_settings['connection'][_section]:
                    _helper_connection_info[_section][_key] = self._helper_settings['connection'][_section][_key]
                else:
                    _helper_connection_info[_section][_key] = None
        return _helper_connection_info

    def _parse_env_connection_info(self):
        """This function parses the environment variable definitions to populate the connection info dictionary.

        .. versionadded:: 1.0.0
        """
        _env_connection_info = copy.deepcopy(auth.EMPTY_CONNECTION_INFO)
        _legacy_mapping = {
            'access_id': 'legacy_access_id',
            'private_key_path': 'legacy_key_path',
            'private_key_file': 'legacy_key_file',
        }
        _oauth_mapping = {
            'issuer_url': 'oauth_issuer_url',
            'client_id': 'oauth_client_id',
            'grant_type': 'oauth_grant_type',
        }

        # Populate the legacy API connection values where defined
        for _legacy_key in _legacy_mapping:
            _env_connection_info['legacy'][_legacy_key] = self._env_variables.get(_legacy_mapping.get(_legacy_key), None)

        # Populate the OAuth connection values where defined
        for _oauth_key in _oauth_mapping:
            _env_connection_info['oauth'][_oauth_key] = self._env_variables.get(_oauth_mapping.get(_oauth_key), None)

        # Return the populated connection information
        return _env_connection_info

    @staticmethod
    def _merge_connection_variables(_defined_info=None, _supplemental_info=None):
        """This function merges the connection variables explicitly passed as parameters with the values defined
           in the helper settings or environmental variables.

        .. versionadded:: 1.0.0
        """
        _merged_connection_info = copy.deepcopy(auth.EMPTY_CONNECTION_INFO)
        for _section, _key_list in auth.STRUCTURED_CONNECTION_FIELDS.items():
            for _key in _key_list:
                # Leverage the defined value first if it is not None or missing
                if (_defined_info and _section in _defined_info and _key in _defined_info[_section]
                        and _defined_info[_section][_key] is not None):
                    _merged_connection_info[_section][_key] = _defined_info[_section][_key]
                # Leverage the supplemental settings when the key was not explicitly defined in parameters
                elif (_supplemental_info and _section in _supplemental_info and _key in _supplemental_info[_section]
                        and _supplemental_info[_section][_key] is not None):
                    _merged_connection_info[_section][_key] = _supplemental_info[_section][_key]
                # Define the key as None if no defined or helper value exists
                else:
                    _merged_connection_info[_section][_key] = None
        return _merged_connection_info

    def _populate_missing_connection_details(self, _partial_connection_info):
        """This function adds missing field values the connection info dictionary as needed.

        .. versionadded:: 1.0.0
        """
        # Populate the Issuer URL value for OAuth connections if not defined
        if (('issuer_url' not in _partial_connection_info['oauth'] or
                not _partial_connection_info['oauth']['issuer_url']) and self.base_url is not None):
            _partial_connection_info['oauth']['issuer_url'] = f'{self.base_url}/oauth'

        # Populate the Grant Type value for OAuth connections if not defined
        if 'grant_type' not in _partial_connection_info['oauth'] or not _partial_connection_info['oauth']['grant_type']:
            _partial_connection_info['oauth']['grant_type'] = auth.OAUTH_GRANT_TYPE

        # Populate the Client Authentication value for OAuth connections if not defined
        dict_key = 'client_authentication'
        if (dict_key not in _partial_connection_info['oauth'][dict_key] or
                not _partial_connection_info['oauth'][dict_key]):
            _partial_connection_info['oauth'][dict_key] = auth.OAUTH_CLIENT_AUTH

        # Return the updated connection info dictionary
        return _partial_connection_info

    def _check_if_connected(self):
        """This function checks to see if the object is connected to the tenant and raises an exception if not.

        .. versionadded:: 1.0.0
        """
        if not self.connected:
            error_msg = 'Must be connected to the tenant before performing an API call. Call the connect() method.'
            logger.error(error_msg)
            raise errors.exceptions.APIConnectionError(error_msg)

    def connect(self):
        """This function connects to the RSA ID Plus tenant using the Legacy API or OAuth method.

        .. versionadded:: 1.0.0

        :returns: Boolean value indicating if connection was established and dictionary with base API headers
        :raises: :py:exc:`errors.exceptions.APIConnectionError`,
                 :py:exc:`errors.exceptions.FeatureNotConfiguredError`
        """
        base_headers = None
        connected = self.connected
        if not connected:
            if self.connection_type == 'legacy':
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
            elif self.connection_type == 'oauth':
                # Connect to the tenant using the OAuth method
                # TODO: Define the base headers using OAuth instead of raising the exception below
                raise errors.exceptions.FeatureNotConfiguredError('OAuth connections are not currently supported')
        return connected, base_headers

    def get(self, endpoint, params=None, headers=None, api_type='admin', timeout=30, show_full_error=True,
            return_json=True, allow_failed_response=False):
        """This method performs a GET request against the ID Plus tenant.

        .. versionadded:: 1.0.0

        :param endpoint: The API endpoint to query
        :type endpoint: str
        :param params: The query parameters (where applicable)
        :type params: dict, None
        :param headers: Specific API headers to use when performing the API call (beyond the base headers)
        :type headers: dict, None
        :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
        :type api_type: str
        :param timeout: The timeout period in seconds (defaults to ``30``)
        :type timeout: int, str, None
        :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
        :type show_full_error: bool
        :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
        :type return_json: bool
        :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                      (``False`` by default)
        :type allow_failed_response: bool
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

    def post(self, endpoint, payload, params=None, headers=None, api_type='admin', timeout=30,
             show_full_error=True, return_json=True, allow_failed_response=False):
        """This method performs a POST call with payload against the ID Plus tenant.

        .. versionadded:: 1.0.0

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
        :type timeout: int, str, None
        :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
        :type show_full_error: bool
        :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
        :type return_json: bool
        :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                      (``False`` by default)
        :type allow_failed_response: bool
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

    def put(self, endpoint, payload, params=None, headers=None, api_type='admin', timeout=30,
            show_full_error=True, return_json=True, allow_failed_response=False):
        """This method performs a PUT call with payload against the ID Plus tenant.

        .. versionadded:: 1.0.0

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
        :type timeout: int, str, None
        :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
        :type show_full_error: bool
        :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
        :type return_json: bool
        :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                      (``False`` by default)
        :type allow_failed_response: bool
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
        """This class includes user-related methods."""
        def __init__(self, pydp_object):
            """This method initializes the :py:class:`pydplus.core.PyDPlus.User` inner class object.

            :param pydp_object: The core :py:class:`pydplus.PyDPlus` object
            :type pydp_object: class[pydplus.PyDPlus]
            """
            self.pydp_object = pydp_object

        def get_user_details(self, email, search_unsynced=None, timeout=api.DEFAULT_TIMEOUT, show_full_error=True,
                             return_json=True, allow_failed_response=False):
            """This method retrieves the details for a specific user based on their email address.

            .. versionadded:: 1.0.0

            :param email: The email address of the user for whom to retrieve details
            :type email: str
            :param search_unsynced: Indicates if the user search should include unsynchronized users (optional)
            :type search_unsynced: bool, None
            :param timeout: The timeout period in seconds (defaults to ``30``)
            :type timeout: int, str, None
            :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
            :type show_full_error: bool
            :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
            :type return_json: bool
            :param allow_failed_response: Indicates that failed responses should return and should not raise an
                                          exception (``False`` by default)
            :type allow_failed_response: bool
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


def compile_connection_info(base_url, private_key, legacy_access_id, oauth_client_id):
    """This function compiles the connection_info dictionary to use when authenticating to the API.

    .. versionadded:: 1.0.0

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
    issuer_url = f'{base_url}/oauth' if base_url else None
    connection_info = {
        'legacy': {
            'access_id': legacy_access_id,
            'private_key_path': private_key_path,
            'private_key_file': private_key_file,
        },
        'oauth': {
            'issuer_url': issuer_url,
            'client_id': oauth_client_id,
            'grant_type': auth.OAUTH_GRANT_TYPE,
            'client_authentication': auth.OAUTH_CLIENT_AUTH,
        }
    }
    return connection_info
