# -*- coding: utf-8 -*-
"""
:Module:            pydplus.core
:Synopsis:          This module performs the core operations of the package
:Usage:             ``from pydplus import PyDPlus``
:Example:           ``prod = PyDPlus()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 May 2025
"""

from . import errors
from .utils import core_utils, log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


class PyDPlus(object):
    """This is the class for the core object leveraged in this module."""
    # Define the function that initializes the object instance (i.e. instantiates the object)
    def __init__(self, connection_type='oauth', private_key=None, helper=None):
        """This method instantiates the core Salesforce object.

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


