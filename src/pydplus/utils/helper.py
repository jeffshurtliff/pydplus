# -*- coding: utf-8 -*-
"""
:Module:            pydplus.utils.helper
:Synopsis:          Module that allows the pydplus library to leverage a helper configuration file
:Usage:             ``from pydplus.utils import helper``
:Example:           ``helper_settings = helper.get_settings('/tmp/helper.yml', 'yaml')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Mar 2026
"""

from __future__ import annotations

import json
from typing import Optional, Union

import yaml

from . import log_utils
from .core_utils import get_file_type
from .. import errors
from .. import constants as const

# Initialize logging within the module
logger = log_utils.initialize_logging(__name__)


def import_helper_file(file_path: str, file_type: str) -> dict:
    """Import a YAML (.yml, .yaml) or JSON (.json) helper config file.

    :param file_path: The file path to the YAML file
    :type file_path: str
    :param file_type: Defines the file type as ``yaml``, ``yml``, or ``json``
    :type file_type: str
    :returns: The parsed configuration data
    :raises: :py:exc:`FileNotFoundError`,
             :py:exc:`salespyforce.errors.exceptions.InvalidHelperFileTypeError`
    """
    with open(file_path, 'r') as cfg_file:
        if file_type.replace('.', '') in (const.FILE_EXTENSIONS.YML, const.FILE_EXTENSIONS.YAML):
            helper_cfg = yaml.safe_load(cfg_file)
        elif file_type.replace('.', '') == const.FILE_EXTENSIONS.JSON:
            helper_cfg = json.load(cfg_file)
        else:
            logger.error(const._EXCEPTION_CLASSES._INVALID_HELPER_DEFAULT_MSG)
            raise errors.exceptions.InvalidHelperFileTypeError()
    logger.info(f'The helper file {file_path} was imported successfully.')
    return helper_cfg


def _convert_yaml_to_bool(_yaml_bool_value: str) -> bool:
    """Convert the 'yes' and 'no' YAML values to traditional Boolean values."""
    if _yaml_bool_value.lower() in const.HELPER_SETTINGS.VALID_YAML_TRUE_VALUES:
        return True
    else:
        return False


def _get_connection_info(_helper_cfg: dict) -> dict[str, dict]:
    """Parse any connection information found in the helper file."""
    _connection_info = {const.CONNECTION_INFO.LEGACY: {}, const.CONNECTION_INFO.OAUTH: {}}
    for _section, _key_list in const.CONNECTION_INFO.CONNECTION_FIELDS.items():
        for _key in _key_list:
            if (const.HELPER_SETTINGS.CONNECTION in _helper_cfg
                    and _section in _helper_cfg[const.HELPER_SETTINGS.CONNECTION]
                    and _key in _helper_cfg[const.HELPER_SETTINGS.CONNECTION][_section]):
                _connection_info[_section][_key] = _helper_cfg[const.HELPER_SETTINGS.CONNECTION][_section][_key]
    return _connection_info


def _collect_values(
        _top_level_keys: Union[list, tuple, set, frozenset, str],
        _helper_cfg: dict,
        _helper_dict: Optional[dict] = None,
        _ignore_missing: bool = False,
) -> dict:
    """Loop through a list of top-level keys to collect their corresponding values.

    :param _top_level_keys: One or more top-level keys that might be found in the helper config file
    :type _top_level_keys: list, tuple, set, frozenset, str
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
            if _key_val in const.YAML_BOOLEAN_MAPPING:
                _key_val = const.YAML_BOOLEAN_MAPPING.get(_key_val)
            _helper_dict[_key] = _key_val
        elif _key == const.HELPER_SETTINGS.VERIFY_SSL:
            # Verify SSL certificates by default unless explicitly set to false
            _helper_dict[_key] = True
        else:
            if not _ignore_missing:
                _helper_dict[_key] = None
    return _helper_dict


def get_helper_settings(
        file_path: str,
        file_type: str = const.FILE_EXTENSIONS.JSON,
        defined_settings: Optional[dict] = None,
) -> dict[str, Union[str, bool, dict]]:
    """Return a dictionary of the defined helper settings.

    :param file_path: The file path to the helper configuration file
    :type file_path: str
    :param file_type: Defines the helper configuration file as a ``json`` file (default) or a ``yaml`` file
    :type file_type: str
    :param defined_settings: Core object settings (if any) defined via the ``defined_settings`` parameter
    :type defined_settings: dict, None
    :returns: Dictionary of helper variables
    :raises: :py:exc:`pydplus.errors.exceptions.InvalidHelperFileTypeError`
    """
    # Convert the defined_settings parameter to an empty dictionary if null
    defined_settings = {} if not defined_settings else defined_settings

    if file_type not in const.HELPER_SETTINGS.VALID_HELPER_FILE_TYPES:
        file_type = get_file_type(file_path)

    # Import the helper configuration file
    helper_cfg = import_helper_file(file_path, file_type)

    # Populate the root-level fields that do not require further validation
    helper_settings = _collect_values(const.HELPER_SETTINGS.ROOT_LEVEL_BASIC_FIELDS, helper_cfg, defined_settings)

    # Populate the connection information in the helper dictionary
    if const.HELPER_SETTINGS.CONNECTION in helper_cfg and const.HELPER_SETTINGS.CONNECTION not in defined_settings:
        helper_settings[const.HELPER_SETTINGS.CONNECTION] = _get_connection_info(helper_cfg)

    # Populate the environment variables information in the helper dictionary
    if const.HELPER_SETTINGS.ENV_VARIABLES in helper_cfg and const.HELPER_SETTINGS.ENV_VARIABLES not in defined_settings:
        helper_settings.update(_collect_values(const.HELPER_SETTINGS.ENV_VARIABLES, helper_cfg))

    # Return the helper_settings dictionary
    return helper_settings
