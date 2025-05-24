# -*- coding: utf-8 -*-
"""
:Module:            pydplus.core
:Synopsis:          This module performs the core operations of the package
:Usage:             ``from pydplus import PyDPlus``
:Example:           ``prod = PyDPlus()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     24 May 2025
"""

import os

from . import auth, errors
from .utils import core_utils, log_utils
from .utils.helper import get_helper_settings, DEFAULT_HELPER_FILE_TYPE

# Initialize logging
logger = log_utils.initialize_logging(__name__)


class PyDPlus(object):
    """This is the class for the core object leveraged in this module."""
    # Define the function that initializes the object instance (i.e. instantiates the object)
    def __init__(self, connection_info=None, connection_type=auth.DEFAULT_CONNECTION_TYPE, base_url=None,
                 private_key=None, legacy_access_id=None, oauth_client_id=None, verify_ssl=True, env_variables=None,
                 helper=None):
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
        :type verify_ssl: bool
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
        if connection_type in auth.VALID_CONNECTION_TYPES:
            self.connection_type = connection_type
        else:
            self.connection_type = auth.DEFAULT_CONNECTION_TYPE

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

        # Check for provided connection info
        if connection_info is None:
            # Check for individual parameters defined in object instantiation
            # TODO: Add logic to check for individually defined parameters

            # Check for defined helper settings
            if self._helper_settings:
                connection_info = self._parse_helper_connection_info()

            # Check for defined environment variables
            # TODO: Check for defined environment variables

            # Add missing field values where possible and when needed
            # TODO: Define the OAuth Issuer URL using the base_url


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
            'oauth_grant_type': 'PYDPLUS_OAUTH_GRANT_TYPE'
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
        _connection_info = {'legacy': {}, 'oauth': {}}
        _connection_fields = {'legacy': auth.LEGACY_CONNECTION_FIELDS, 'oauth': auth.OAUTH_CONNECTION_FIELDS}
        for _section, _key_list in _connection_fields.items():
            for _key in _key_list:
                if _key in self._helper_settings['connection'][_section]:
                    _connection_info[_section][_key] = self._helper_settings['connection'][_section][_key]
                else:
                    _connection_info[_section][_key] = None
        return _connection_info


def compile_connection_info(connection_type, base_url, private_key, legacy_access_id, oauth_client_id, verify_ssl):
    private_key_path, private_key_file = core_utils.split_file_path(private_key)
    connection_info = {
        'base_url': base_url,
        'connection_type': connection_type,
        'connection': {
            'legacy': {
                'access_id': legacy_access_id,
                'private_key_path': private_key_path,
                'private_key_file': private_key_file,
            },
            'oauth': {
                # TODO: Use the base_url to get the issuer URL
                'client_id': oauth_client_id,
                'grant_type': auth.OAUTH_GRANT_TYPE,
                'client_authentication': auth.OAUTH_CLIENT_AUTH,
            }
        },
        'verify_ssl': verify_ssl,
    }
    return connection_info
