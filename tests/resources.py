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


def get_core_object(init_method=None, **kwargs):
    """This function instantiates and returns the core object using a local helper file.

    .. versionadded:: 1.0.0

    :param init_method: The method to use when instantiating the object (e.g. ``helper``, ``param`` (default), ``env``)
    :type init_method: str, None
    :keyword base_url: The base URL to leverage when performing API calls
    :kwtype base_url: str, None
    :keyword connection_info: Dictionary that defines the connection info to use
    :kwtype connection_info: dict, None
    :keyword connection_type:
    :kwtype connection_type: dict, None
    :keyword private_key: The file path to the private key used for API authentication (OAuth or Legacy)
    :kwtype private_key: str, None
    :keyword legacy_access_id: The Access ID associated with the Legacy API connection
    :kwtype legacy_access_id: str, None
    :keyword oauth_client_id: The Client ID associated with the OAuth API connection
    :kwtype oauth_client_id: str, None
    :keyword verify_ssl: Determines if SSL connections should be verified (``True`` by default)
    :kwtype verify_ssl: bool, None
    :keyword auto_connect: Determines if an API connection should be established when the object is instantiated
                           (``True`` by default)
    :kwtype auto_connect: bool
    :returns: The instantiated core object
    """
    pydp_object = None
    set_package_path()
    if init_method and init_method == 'helper':
        if secrets_helper_exists():
            pydp_object = instantiate_with_secrets_helper()
        else:
            if not local_helper_exists():
                pytest.skip('skipping tests where a valid helper file is needed')
            pydp_object = instantiate_with_local_helper()
    elif init_method and init_method == 'env':
        # TODO: Add ability to instantiate the object using environment variables
        pass
    elif init_method and init_method in ('param', 'params', 'parameter', 'parameters'):
        pydp_object = instantiate_with_parameters(**kwargs)
    else:
        pydp_object = instantiate_with_parameters(**kwargs)
    return pydp_object


def instantiate_with_secrets_helper():
    """This function instantiates the PyDPlus object using the unencrypted helper file intended for GitHub Actions.

    .. versionadded:: 1.0.0

    :returns: The instantiated :py:class:`pydplus.core.PyDPlus` object
    :raises: :py:exc:`FileNotFoundError`
    """
    if not secrets_helper_exists():
        raise FileNotFoundError('The unencrypted GitHub Actions helper file cannot be found.')
    file_name = f'{os.environ.get("HOME")}/secrets/{HELPER_FILE_NAME}'
    set_package_path()
    core_module = importlib.import_module('pydplus.core')
    return core_module.PyDPlus(helper=file_name)


def instantiate_with_local_helper():
    """This function instantiates the PyDPlus object using a local helper file for unit testing.

    .. versionadded:: 1.0.0

    :returns: The instantiated :py:class:`pydplus.core.PyDPlus` object
    :raises: :py:exc:`FileNotFoundError`
    """
    if not local_helper_exists():
        raise FileNotFoundError('The local helper file cannot be found.')
    set_package_path()
    core_module = importlib.import_module('pydplus.core')
    return core_module.PyDPlus(helper=f"local/{HELPER_FILE_NAME}")


def instantiate_with_parameters(**kwargs):
    # Import the core module
    set_package_path()
    core_module = importlib.import_module('pydplus.core')

    # Define default parameters (excluding env_variables and helper)
    parameters = {
        'base_url': None,
        'connection_info': None,
        'connection_type': None,
        'private_key': None,
        'legacy_access_id': None,
        'oauth_client_id': None,
        'verify_ssl': None,
        'auto_connect': True,
    }

    # Define parameters based on keyword arguments
    for param in parameters.keys():
        if param in kwargs:
            parameters[param] = kwargs.get(param, None)

    # Attempt to instantiate and return the core object
    return core_module.PyDPlus(
        connection_info=kwargs.get('connection_info', None),
        connection_type=kwargs.get('connection_type', None),
        base_url=kwargs.get('base_url', None),
        private_key=kwargs.get('private_key', None),
        legacy_access_id=kwargs.get('legacy_access_id', None),
        oauth_client_id=kwargs.get('oauth_client_id', None),
        verify_ssl=kwargs.get('verify_ssl', None),
        auto_connect=kwargs.get('auto_connect', None)
    )
