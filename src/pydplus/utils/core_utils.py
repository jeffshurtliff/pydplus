# -*- coding: utf-8 -*-
"""
:Module:            pydplus.utils.core_utils
:Synopsis:          Collection of supporting utilities and functions to complement the primary modules
:Usage:             ``from pydplus.utils import core_utils``
:Example:           ``encoded_string = core_utils.encode_url(decoded_string)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     29 May 2025
"""

import os
import random
import string
import warnings
import urllib.parse

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
    :raises: :py:exc:`TypeError`
    """
    return urllib.parse.quote_plus(raw_string)


def url_decode(encoded_string):
    """This function decodes a url-encoded string.

    .. versionadded:: 1.0.0

    :param encoded_string: The url-encoded string
    :type encoded_string: str
    :returns: The unencoded string
    :raises: :py:exc:`TypeError`
    """
    return urllib.parse.unquote_plus(encoded_string)


def ensure_ending_slash(path, path_type='url'):
    """This function ensures that a URL ends with a forward slash (``/``) or backslash (``\\``).

    .. versionadded:: 1.0.0

    :param path: The path (URL or file path) to check and potentially add an ending slash
    :type path: str
    :param path_type: Indicates that the path is for a ``url`` (default) or a ``file``
    :type path_type: str
    :returns: The URL string with an ending forward slash
    :raises: :py:exc:`TypeError`
    """
    if not isinstance(path_type, str) or path_type not in ('url', 'file'):
        raise TypeError("The url_path parameter must be defined as 'url' or 'file'")
    if path and path_type.lower() == 'url':
        path = f'{path}/' if not path.endswith('/') else path
    elif path and path_type.lower() == 'file':
        path = f'{path}{os.sep}' if not path.endswith(os.sep) else path
    return path


def display_warning(warn_msg):
    """This function displays a :py:exc:`UserWarning` message via the :py:mod:`warnings` module.

    .. versionadded:: 1.0.0

    :param warn_msg: The message to be displayed
    :type warn_msg: str
    :raises: :py:exc:`TypeError`
    """
    warnings.warn(warn_msg, UserWarning)


def file_exists(file_path):
    """This function checks to see if a file exists at a given file path.

    .. versionadded:: 1.0.0

    :param file_path: The full path to the file
    :type file_path: str
    :returns: Boolean value indicating if the file exists
    :raises: :py:exc:`TypeError`
    """
    return os.path.isfile(file_path)


def get_file_type(file_path):
    """This function attempts to identify if a given file path is for a YAML or JSON file.

    .. versionadded:: 1.0.0

    :param file_path: The full path to the file
    :type file_path: str
    :returns: The file type in string format (e.g. ``yaml`` or ``json``)
    :raises: :py:exc:`TypeError`,
             :py:exc:`FileNotFoundError`,
             :py:exc:`pydplus.errors.exceptions.UnknownFileTypeError`
    """
    file_type = 'unknown'
    if os.path.isfile(file_path):
        if file_path.endswith('.json'):
            file_type = 'json'
        elif file_path.endswith('.yml') or file_path.endswith('.yaml'):
            file_type = 'yaml'
        else:
            display_warning(f"Unable to recognize the file type of '{file_path}' by its extension.")
            with open(file_path) as cfg_file:
                for line in cfg_file:
                    if line.startswith('#'):
                        continue
                    else:
                        if '{' in line:
                            file_type = 'json'
                            break
        if file_type == 'unknown':
            raise errors.exceptions.UnknownFileTypeError(file=file_path)
    else:
        raise FileNotFoundError(f'Unable to locate the following file: {file_path}')
    return file_type


def split_file_path(full_path):
    """This function splits a full file path into separate variables for file path and file name.

    .. versionadded:: 1.0.0

    :param full_path: The full path to the file including the file name
    :type full_path: str
    :returns: The file path and file name strings as separate variables
    :raises: :py:exc:`TypeError`
    """
    file_path = os.path.dirname(full_path)
    if file_path and not file_path.endswith(os.sep):
        file_path = f'{file_path}{os.sep}'
    file_name = os.path.basename(full_path)
    return file_path, file_name


def get_base_url(url, include_scheme=True):
    """This function parses a URL to return only the base URL with or without the scheme.

    .. versionadded:: 1.0.0

    :param url: The URL to parse
    :type url: str
    :param include_scheme: Determines if the scheme (e.g. ``https://``) should be included (``True`` by default)
    :type include_scheme: bool
    :returns: The base URL as a string
    :raises: :py:exc:`TypeError`
    """
    parsed_url = urllib.parse.urlparse(url)
    base_url = parsed_url.netloc
    base_url = f'{parsed_url.scheme}://{base_url}' if include_scheme else base_url
    return base_url


def get_random_string(length=32, prefix_string=''):
    """This function returns a random alphanumeric string.

    .. versionadded:: 1.0.0

    :param length: The length of the string (``32`` by default)
    :type length: int
    :param prefix_string: A string to which the random string should be appended (optional)
    :type prefix_string: str
    :returns: The alphanumeric string
    """
    return f"{prefix_string}{''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])}"
