# -*- coding: utf-8 -*-
"""
:Module:            pydplus.core
:Synopsis:          This module performs the core operations of the package
:Usage:             ``from pydplus import PyDPlus``
:Example:           ``prod = PyDPlus()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     19 May 2025
"""

from . import errors
from .utils import core_utils, log_utils
from .utils.helper import get_helper_settings, DEFAULT_HELPER_FILE_TYPE

# Initialize logging
logger = log_utils.initialize_logging(__name__)


class PyDPlus(object):
    """This is the class for the core object leveraged in this module."""
    # Define the function that initializes the object instance (i.e. instantiates the object)
    def __init__(self, connection_info=None, connection_type='oauth', private_key=None, helper=None):
        """This method instantiates the core Salesforce object.

        :param connection_info: Dictionary that defines the connection info to use
        :type connection_info: dict, None
        :param connection_type: Defines the connection type to leverage ``oauth`` (default) or ``legacy``
        :type connection_type: str, None
        :param private_key: The file path to the private key used for API authentication
        :type private_key: str, None
        :param helper: The file path of a helper file (when applicable)
        :type helper: str, None
        :returns: The instantiated object
        :raises: :py:exc:`TypeError`
        """
        # Define the default settings
        self._helper_settings = {}

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

        # Check for provided connection info
        if connection_info is None:
            # Check for defined helper settings
            if self._helper_settings:
                # TODO: Define connection_info using _helper_settings
                pass




