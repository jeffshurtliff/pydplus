# -*- coding: utf-8 -*-
"""
:Module:            pydplus.utils.helper
:Synopsis:          Module that allows the pydplus library to leverage a helper configuration file
:Usage:             ``from pydplus.utils import helper``
:Example:           ``helper_settings = helper.get_settings('/tmp/helper.yml', 'yaml')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 May 2025
"""

import json

import yaml

from .. import errors
from . import log_utils
from .core_utils import get_file_type

# Define constants
DEFAULT_HELPER_FILE_TYPE = 'json'

# Initialize logging within the module
logger = log_utils.initialize_logging(__name__)


def import_helper_file(file_path, file_type):
    """This function imports a YAML (.yml) or JSON (.json) helper config file.

    .. versionadded:: 1.0.0

    :param file_path: The file path to the YAML or JSON file
    :type file_path: str
    :param file_type: Defines the file type as either ``yaml`` or ``json``
    :type file_type: str
    :returns: The parsed configuration data
    :raises: :py:exc:`FileNotFoundError`,
             :py:exc:`pydplus.errors.exceptions.InvalidHelperFileTypeError`
    """
    with open(file_path, 'r') as cfg_file:
        if file_type.lower() == 'yaml':
            helper_cfg = yaml.safe_load(cfg_file)
        elif file_type.lower() == 'json':
            helper_cfg = json.load(cfg_file)
        else:
            raise errors.exceptions.InvalidHelperFileTypeError()
    logger.info(f'The helper file {file_path} was imported successfully.')
    return helper_cfg


def _convert_yaml_to_bool(_yaml_bool_value):
    """This function converts the 'yes' and 'no' YAML values to traditional Boolean values.

    .. versionadded:: 1.0.0
    """
    _true_values = ['yes', 'true']
    if _yaml_bool_value.lower() in _true_values:
        _bool_value = True
    else:
        _bool_value = False
    return _bool_value


def _get_connection_info(_helper_cfg):
    """This function parses any connection information found in the helper file.

    .. versionadded:: 1.0.0
    """
    _connection_info = {'legacy': {}, 'oauth': {}}
    _legacy_keys = ['access_id', 'private_key_path', 'private_key_file']
    _oauth_keys = ['issuer_url', 'client_id', 'grant_type', 'client_authentication']
    for _section, _key_list in {'legacy': _legacy_keys, 'oauth': _oauth_keys}.items():
        for _key in _key_list:
            if _key in _helper_cfg['connection'][_section]:
                _connection_info[_section][_key] = _helper_cfg['connection'][_section][_key]
    return _connection_info


def _collect_values(_top_level_keys, _helper_cfg, _helper_dict=None, _ignore_missing=False):
    """This function loops through a list of top-level keys to collect their corresponding values.

    .. versionadded:: 1.0.0

    :param _top_level_keys: One or more top-level keys that might be found in the helper config file
    :type _top_level_keys: list, tuple, set, str
    :param _helper_cfg: The configuration parsed from the helper configuration file
    :type _helper_cfg: dict
    :param _helper_dict: A predefined dictionary to which the key value pairs should be added
    :type _helper_dict: dict, None
    :param _ignore_missing: Indicates whether fields with null values should be ignored (``False`` by default)
    :type _ignore_missing: bool
    :returns: A dictionary with the identified key value pairs
    """
    _helper_dict = {} if not _helper_dict else _helper_dict
    _top_level_keys = (_top_level_keys, ) if isinstance(_top_level_keys, str) else _top_level_keys
    for _key in _top_level_keys:
        if _key in _helper_cfg:
            _key_val = _helper_cfg[_key]
            if isinstance(_key_val, str) and _key_val in HelperParsing.yaml_boolean_values:
                _key_val = HelperParsing.yaml_boolean_values.get(_key_val)
            _helper_dict[_key] = _key_val
        elif _key == 'ssl_verify':
            # Verify SSL certificates by default unless explicitly set to false
            _helper_dict[_key] = True
        else:
            if not _ignore_missing:
                _helper_dict[_key] = None
    return _helper_dict


def get_helper_settings(file_path, file_type='json', defined_settings=None):
    """This function returns a dictionary of the defined helper settings.

    .. versionadded:: 1.0.0

    :param file_path: The file path to the helper configuration file
    :type file_path: str
    :param file_type: Defines the helper configuration file as a ``json`` file (default) or a ``yaml`` file
    :type file_type: str
    :param defined_settings: Core object settings (if any) defined via the ``defined_settings`` parameter
    :type defined_settings: dict, None
    :returns: Dictionary of helper variables
    :raises: :py:exc:`pydplus.errors.exceptions.InvalidHelperFileTypeError`
    """
    # Initialize the helper_settings dictionary
    helper_settings = {}

    # Convert the defined_settings parameter to an empty dictionary if null
    defined_settings = {} if not defined_settings else defined_settings

    if file_type != 'yaml' and file_type != 'json':
        file_type = get_file_type(file_path)

    # Import the helper configuration file
    helper_cfg = import_helper_file(file_path, file_type)

    # Populate the top-level fields that do not require further validation
    top_level_values = ['base_url', 'connection_type', 'ssl_verify']
    helper_settings = _collect_values(top_level_values, helper_cfg, defined_settings)

    # Populate the connection information in the helper dictionary
    if 'connection' in helper_cfg and 'connection' not in defined_settings:
        helper_settings['connection'] = _get_connection_info(helper_cfg)

    # Populate the environment variables information in the helper dictionary
    if 'env_variables' in helper_cfg and 'env_variables' not in defined_settings:
        helper_settings.update(_collect_values('env_variables', helper_cfg))

    # Return the helper_settings dictionary
    return helper_settings


class HelperParsing:
    """This class is used to help parse values imported from a YAML configuration file."""
    # Define dictionary to map YAML Boolean to Python Boolean
    yaml_boolean_values = {
        True: True,
        False: False,
        'yes': True,
        'no': False
    }
