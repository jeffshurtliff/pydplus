# -*- coding: utf-8 -*-
"""
:Module:            pydplus.tests.resources
:Synopsis:          Frequently used resources for performing unit testing
:Usage:             ``from pydplus.tests import resources``
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Jun 2025
"""

import os
import sys
import importlib

import pytest

# Define constants
SKIP_LOCAL_TEST_MSG = 'skipping local-only tests'
HELPER_FILE_NAME = 'helper_dev.yml'


class MockResponse:
    """This class simulates an API response for testing purposes.

    .. versionadded:: 1.0.0
    """
    def __init__(self, json_body, status_code=200):
        self.json_body = json_body
        self.status_code = status_code

    def json(self):
        return self.json_body


def mock_success_response(*args, **kwargs):
    """This function works with the `MockedResponse` class to simulate a successful API response.

    .. versionadded:: 1.0.0
    """
    return MockResponse({
        'id': '54082ac6-4713-6368-2251-df813c41159f',
    })


def mock_error_response(*args, **kwargs):
    """This function works with the `MockedResponse` class to simulate a failed API response.

    .. versionadded:: 1.0.0
    """
    return MockResponse({
        'code': '404 NOT_FOUND',
        'description': 'User john.doe@example.com not found',
    })


def set_package_path():
    """This function adds the high-level pydplus directory to the sys.path list.

    .. versionadded:: 1.0.0
    """
    sys.path.insert(0, os.path.abspath('../..'))


def import_modules(*modules):
    """This function imports and returns one or more modules to utilize in a unit test.

    .. versionadded:: 1.0.0

    :param modules: One or more module paths (absolute) in string format
    :returns: The imported module(s) as an individual object or a tuple of objects
    """
    imported_modules = []
    for module in modules:
        imported_modules.append(importlib.import_module(module))
    tuple(imported_modules)
    return imported_modules if len(imported_modules) > 1 else imported_modules[0]


def secrets_helper_exists():
    """This function checks to see if the unencrypted helper file exists for GitHub Actions.

    .. versionadded:: 1.0.0
    """
    helper_path = f'{os.environ.get("HOME")}/secrets/{HELPER_FILE_NAME}'
    return os.path.isfile(helper_path)


def local_helper_exists():
    """This function checks to see if a helper file is present in the ``local/`` directory.

    .. versionadded:: 1.0.0
    """
    return os.path.exists(f'local/{HELPER_FILE_NAME}')


# TODO: Add functions to instantiate core object with secrets or local helper
