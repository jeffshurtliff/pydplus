# -*- coding: utf-8 -*-
"""
:Module:            pydplus.utils.core_utils
:Synopsis:          Collection of supporting utilities and functions to complement the primary modules
:Usage:             ``from pydplus.utils import core_utils``
:Example:           ``encoded_string = core_utils.encode_url(decoded_string)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     06 May 2025
"""

import random
import string
import os.path
import warnings
import urllib.parse

import requests

from . import log_utils
from .. import errors

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def url_encode(raw_string):
    """This function encodes a string for use in URLs.

    .. versionadded:: 1.0.0

    :param raw_string: The raw string to be encoded
    :type raw_string: str
    :returns: The encoded string
    """
    return urllib.parse.quote_plus(raw_string)


def url_decode(encoded_string):
    """This function decodes a url-encoded string.

    .. versionadded:: 1.0.0

    :param encoded_string: The url-encoded string
    :type encoded_string: str
    :returns: The unencoded string
    """
    return urllib.parse.unquote_plus(encoded_string)


