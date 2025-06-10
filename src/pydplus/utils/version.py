# -*- coding: utf-8 -*-
"""
:Module:            pydplus.utils.version
:Synopsis:          This module contains the package version information
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Jun 2025
"""

from . import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)

# Define special and global variables
__version__ = '1.0.0b1'


def get_full_version():
    """This function returns the current full version of the ``pydplus`` package."""
    return __version__


def get_major_minor_version():
    """This function returns the current major.minor (i.e. X.Y) version of the ``pydplus`` package."""
    return ".".join(__version__.split(".")[:2])
