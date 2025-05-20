# -*- coding: utf-8 -*-
"""
:Module:            pydplus.core
:Synopsis:          This module performs the core operations of the package
:Usage:             ``from pydplus import PyDPlus``
:Example:           ``prod = PyDPlus()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     20 May 2025
"""

import os

from . import errors
from .utils import core_utils, log_utils
from .utils.helper import get_helper_settings, DEFAULT_HELPER_FILE_TYPE

# Initialize logging
logger = log_utils.initialize_logging(__name__)

# Define constants
DEFAULT_CONNECTION_TYPE = 'oauth'
VALID_CONNECTION_TYPES = {'oauth', 'legacy'}
LEGACY_CONNECTION_FIELDS = {'access_id', 'private_key_path', 'private_key_file'}
OAUTH_CONNECTION_FIELDS = {'issuer_url', 'client_id', 'grant_type', 'client_authentication'}


class PyDPlus(object):
    """This is the class for the core object leveraged in this module."""
    # Define the function that initializes the object instance (i.e. instantiates the object)
    def __init__(self, connection_info=None, connection_type=DEFAULT_CONNECTION_TYPE, private_key=None,
                 env_variables=None, helper=None):
        """This method instantiates the core Salesforce object.

        :param connection_info: Dictionary that defines the connection info to use
        :type connection_info: dict, None
        :param connection_type: Defines the connection type to leverage ``oauth`` (default) or ``legacy``
        :type connection_type: str, None
        :param private_key: The file path to the private key used for API authentication
        :type private_key: str, None
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
        self.connection_type = connection_type if connection_type in VALID_CONNECTION_TYPES else DEFAULT_CONNECTION_TYPE

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
            # Check for defined helper settings
            if self._helper_settings:
                connection_info = self._parse_helper_connection_info()


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
        for _section, _key_list in {'legacy': LEGACY_CONNECTION_FIELDS, 'oauth': OAUTH_CONNECTION_FIELDS}.items():
            for _key in _key_list:
                if _key in self._helper_settings['connection'][_section]:
                    _connection_info[_section][_key] = self._helper_settings['connection'][_section][_key]
                else:
                    _connection_info[_section][_key] = None
        return _connection_info
