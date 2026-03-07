# -*- coding: utf-8 -*-
"""
:Module:            pydplus.utils.core_utils
:Synopsis:          Collection of supporting utilities and functions to complement the primary modules
:Usage:             ``from pydplus.utils import core_utils``
:Example:           ``encoded_string = core_utils.encode_url(decoded_string)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Mar 2026
"""

from __future__ import annotations

import os
import random
import string
import urllib.parse
from typing import Tuple

from . import log_utils
from .. import errors
from .. import constants as const

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def url_encode(raw_string: str) -> str:
    """Encode a string for use in URLs.

    :param raw_string: The raw string to be encoded
    :type raw_string: str
    :returns: The encoded string
    :raises: :py:exc:`TypeError`
    """
    return urllib.parse.quote_plus(raw_string)


def url_decode(encoded_string: str) -> str:
    """Decode a url-encoded string.

    :param encoded_string: The url-encoded string
    :type encoded_string: str
    :returns: The unencoded string
    :raises: :py:exc:`TypeError`
    """
    return urllib.parse.unquote_plus(encoded_string)


def ensure_ending_slash(path: str, path_type: str = const.ARGUMENT_VALUES.URL) -> str:
    """Ensure that a URL ends with a forward slash (``/``) or backslash (``\\``).

    :param path: The path (URL or file path) to check and potentially add an ending slash
    :type path: str
    :param path_type: Indicates that the path is for a ``url`` (default) or a ``file``
    :type path_type: str
    :returns: The URL string with an ending forward slash
    :raises: :py:exc:`pydplus.errors.exceptions.InvalidParameterError`
    """
    valid_path_types = (const.ARGUMENT_VALUES.FILE, const.ARGUMENT_VALUES.URL)
    if not isinstance(path_type, str) or path_type.lower() not in valid_path_types:
        error_msg = "The url_path parameter must be defined as 'url' or 'file'"
        logger.error(error_msg)
        raise errors.exceptions.InvalidParameterError(error_msg)
    if path and path_type.lower() == const.ARGUMENT_VALUES.URL:
        path = f'{path}/' if not path.endswith('/') else path
    elif path and path_type.lower() == const.ARGUMENT_VALUES.FILE:
        path = f'{path}{os.sep}' if not path.endswith(os.sep) else path
    return path


def remove_ending_slash(path: str) -> str:
    """Remove a trailing slash at the end of a URL or endpoint when present.

    :param path: The URL or path
    :type path: str
    :returns: The path string without a trailing slash
    :raises: :py:exc:`TypeError`
    """
    return path[:-1] if path.endswith('/') else path


def file_exists(file_path: str) -> bool:
    """Check to see if a file exists at a given file path.

    :param file_path: The full path to the file
    :type file_path: str
    :returns: Boolean value indicating if the file exists
    :raises: :py:exc:`TypeError`
    """
    return os.path.isfile(file_path)


def get_file_type(file_path: str) -> str:
    """Attempt to identify if a given file path is for a YAML or JSON file.

    :param file_path: The full path to the file
    :type file_path: str
    :returns: The file type in string format (e.g. ``yaml`` or ``json``)
    :raises: :py:exc:`TypeError`,
             :py:exc:`FileNotFoundError`,
             :py:exc:`pydplus.errors.exceptions.UnknownFileTypeError`
    """
    file_type = 'unknown'
    if os.path.isfile(file_path):
        if file_path.endswith(const.FILE_EXTENSIONS.DOT_JSON):
            file_type = const.FILE_EXTENSIONS.JSON
        elif file_path.endswith(const.FILE_EXTENSIONS.DOT_YAML) or file_path.endswith(const.FILE_EXTENSIONS.DOT_YML):
            file_type = const.FILE_EXTENSIONS.YAML
        else:
            warn_msg = f"Unable to recognize the file type of '{file_path}' by its extension."
            logger.warning(warn_msg)
            errors.handlers.display_warning(warn_msg)
            with open(file_path) as cfg_file:
                for line in cfg_file:
                    if line.startswith('#'):
                        continue
                    else:
                        if '{' in line:
                            file_type = const.FILE_EXTENSIONS.JSON
                            break
        if file_type == 'unknown':
            raise errors.exceptions.UnknownFileTypeError(file=file_path)
    else:
        error_msg = const._EXCEPTION_CLASSES._CANNOT_LOCATE_FILE.format(file_path=file_path)
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    return file_type


def split_file_path(full_path: str) -> Tuple[str, str]:
    """Split a full file path into separate variables for file path and file name.

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


def get_base_url(url: str, include_scheme: bool = True) -> str:
    """Parse a URL to return only the base URL with or without the scheme.

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


def get_random_string(length: int = 32, prefix_string: str = '') -> str:
    """Return a random alphanumeric string.

    :param length: The length of the string (``32`` by default)
    :type length: int
    :param prefix_string: A string to which the random string should be appended (optional)
    :type prefix_string: str
    :returns: The randomized alphanumeric string
    """
    return f"{prefix_string}{''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])}"
