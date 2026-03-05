# -*- coding: utf-8 -*-
"""
:Module:            pydplus.errors.exceptions
:Synopsis:          Collection of exception classes relating to the pydplus library
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     05 Mar 2026
"""

from __future__ import annotations

from typing import Optional, Union

from ..constants import _EXCEPTION_CLASSES, API_REQUEST_TYPES


# -----------------------------
# Base Exception
# -----------------------------


# Define base exception class
class PyDPlusError(Exception):
    """This is the base class for PyDPlus exceptions."""
    pass


# -----------------------------
# General Exceptions
# -----------------------------


class CurrentlyUnsupportedError(PyDPlusError):
    """Exception used when a feature or functionality being used is currently unsupported."""
    def __init__(self, *args, **kwargs):
        default_msg = "This feature is currently unsupported at this time."
        if not (args or kwargs):
            args = (default_msg,)
        elif _EXCEPTION_CLASSES._MESSAGE in kwargs:
            args =(kwargs[_EXCEPTION_CLASSES._MESSAGE],)
        else:
            custom_msg = f"The '{args[0]}' {default_msg.split('This ')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class DataMismatchError(PyDPlusError):
    """Exception used when there is a mismatch between two data sources."""
    def __init__(self, *args, **kwargs):
        default_msg = "A data mismatch was found with the data sources."
        if not (args or kwargs):
            args = (default_msg,)
        elif _EXCEPTION_CLASSES._DATA in kwargs:
            multi_types = [list, tuple, set]
            if isinstance(kwargs[_EXCEPTION_CLASSES._DATA], str):
                custom_msg = (f"{default_msg.split('the data')[0]}the '{kwargs[_EXCEPTION_CLASSES._DATA]}'"
                              f"{default_msg.split('with the')[1]}")
                custom_msg = custom_msg.replace('sources', 'source')
                args = (custom_msg,)
            elif type(kwargs[_EXCEPTION_CLASSES._DATA]) in multi_types and len(kwargs[_EXCEPTION_CLASSES._DATA]) == 2:
                custom_section = f"'{kwargs[_EXCEPTION_CLASSES._DATA][0]}' and '{kwargs[_EXCEPTION_CLASSES._DATA][1]}'"
                custom_msg = f"{default_msg.split('data sources')[0]}{custom_section}{default_msg.split('with the')[1]}"
                args = (custom_msg,)
        super().__init__(*args)


class FeatureNotConfiguredError(PyDPlusError):
    """Exception used when an API request fails because a feature is not configured."""
    def __init__(self, *args, **kwargs):
        exc_msg = "The feature is not configured."
        if _EXCEPTION_CLASSES._IDENTIFIER in kwargs or _EXCEPTION_CLASSES._FEATURE in kwargs:
            if _EXCEPTION_CLASSES._IDENTIFIER in kwargs:
                exc_msg += f" Identifier: {kwargs[_EXCEPTION_CLASSES._IDENTIFIER]}"
            if _EXCEPTION_CLASSES._FEATURE in kwargs:
                exc_msg = exc_msg.replace("feature", f"{kwargs[_EXCEPTION_CLASSES._FEATURE]} feature")
            args = (exc_msg,)
        elif not (args or kwargs):
            args = (exc_msg,)
        super().__init__(*args)


class InvalidParameterError(PyDPlusError):
    """Exception used when an invalid parameter is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The parameter that was provided is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif _EXCEPTION_CLASSES._VAL in kwargs:
            custom_msg = (f"{default_msg.split('parameter ')[0]}'{kwargs[_EXCEPTION_CLASSES._VAL]}'"
                          f"{default_msg.split('The')[1]}")
            args = (custom_msg,)
        super().__init__(*args)


class InvalidFieldError(PyDPlusError):
    """Exception used when an invalid field is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The field that was provided is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif _EXCEPTION_CLASSES._VAL in kwargs:
            custom_msg = f"{default_msg.split('field ')[0]}'{kwargs[_EXCEPTION_CLASSES._VAL]}'{default_msg.split('The')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class InvalidURLError(PyDPlusError):
    """Exception used when a provided URL is invalid."""
    def __init__(self, *args, **kwargs):
        default_msg = "The provided URL is invalid"
        if not (args or kwargs):
            args = (default_msg,)
        elif _EXCEPTION_CLASSES._URL in kwargs:
            custom_msg = (f"{default_msg.split('is')[0]}'{kwargs[_EXCEPTION_CLASSES._URL]}'"
                          f"{default_msg.split(_EXCEPTION_CLASSES._URL)[1]}")
            args = (custom_msg,)
        super().__init__(*args)


class MissingRequiredDataError(PyDPlusError):
    """Exception used when a function or method is missing one or more required arguments."""
    def __init__(self, *args, **kwargs):
        default_msg = "Missing one or more required parameters"
        init_msg = "The object failed to initialize as it is missing one or more required arguments."
        param_msg = "The required parameter 'PARAMETER_NAME' is not defined"
        if not (args or kwargs):
            args = (default_msg,)
        elif _EXCEPTION_CLASSES._INIT in args or _EXCEPTION_CLASSES._INITIALIZE in args:
            if _EXCEPTION_CLASSES._OBJECT in kwargs:
                custom_msg = (f"{init_msg.split(_EXCEPTION_CLASSES._OBJECT)[0]}'{kwargs[_EXCEPTION_CLASSES._OBJECT]}'"
                              f"{init_msg.split('The')[1]}")
                args = (custom_msg,)
            else:
                args = (init_msg,)
        elif _EXCEPTION_CLASSES._PARAM in kwargs:
            args = (param_msg.replace('PARAMETER_NAME', kwargs[_EXCEPTION_CLASSES._PARAM]),)
        super().__init__(*args)


class UnknownFileTypeError(PyDPlusError):
    """Exception used when a file type for a given file cannot be identified."""
    def __init__(self, *args, **kwargs):
        default_msg = "The file type of the given file path cannot be identified."
        if not (args or kwargs):
            args = (default_msg,)
        elif _EXCEPTION_CLASSES._FILE in kwargs:
            custom_msg = (f"{default_msg.split('path')[0]}'{kwargs[_EXCEPTION_CLASSES._FILE]}'"
                          f"{default_msg.split('path')[1]}")
            args = (custom_msg,)
        super().__init__(*args)


# -----------------------------
# Generic API Exceptions
# -----------------------------


class APIConnectionError(PyDPlusError):
    """Exception used when the API query could not be completed due to connection aborts and/or timeouts."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API query could not be completed due to connection aborts and/or timeouts."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class APIMethodError(PyDPlusError, ValueError):
    """Exception used when an invalid API call method is used when performing an API call."""
    def __init__(self, *args, **kwargs):
        default_msg = "A valid API call method (GET or POST or PATCH or PUT) must be defined."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class APIRequestError(PyDPlusError):
    """Exception used for generic API request errors when there is not a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = _EXCEPTION_CLASSES._API_DEFAULT_MSG.format(type='API')
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class APIResponseConversionError(PyDPlusError):
    """Exception used for errors when attempting to convert an API response to another data format. (e.g. JSON)"""
    def __init__(self, *args, **kwargs):
        default_msg = "The API response failed to be converted to the specified data format."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class DELETERequestError(PyDPlusError):
    """Exception used for generic DELETE request errors when there is not a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = _EXCEPTION_CLASSES._API_DEFAULT_MSG.format(type=API_REQUEST_TYPES.DELETE)
        if _EXCEPTION_CLASSES._STATUS_CODE in kwargs or _EXCEPTION_CLASSES._MESSAGE in kwargs:
            custom_msg = _construct_api_custom_message(_request_type=API_REQUEST_TYPES.DELETE,
                                                       _message=kwargs.get(_EXCEPTION_CLASSES._MESSAGE, None),
                                                       _status_code=kwargs.get(_EXCEPTION_CLASSES._STATUS_CODE, None))
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class GETRequestError(PyDPlusError):
    """Exception used for generic GET request errors when there is not a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = _EXCEPTION_CLASSES._API_DEFAULT_MSG.format(type=API_REQUEST_TYPES.GET)
        if _EXCEPTION_CLASSES._STATUS_CODE in kwargs or _EXCEPTION_CLASSES._MESSAGE in kwargs:
            custom_msg = _construct_api_custom_message(_request_type=API_REQUEST_TYPES.GET,
                                                       _message=kwargs.get(_EXCEPTION_CLASSES._MESSAGE, None),
                                                       _status_code=kwargs.get(_EXCEPTION_CLASSES._STATUS_CODE, None))
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidEndpointError(PyDPlusError):
    """Exception used when an invalid API endpoint or service is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied endpoint for the API is not recognized."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidLookupTypeError(PyDPlusError, ValueError):
    """Exception used when an invalid API lookup type is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied lookup type for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'id' and 'email')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidPayloadValueError(PyDPlusError):
    """Exception used when an invalid value is provided for a payload field."""
    def __init__(self, *args, **kwargs):
        default_msg = "An invalid payload value was provided."
        custom_msg = "The invalid payload value 'X' was provided for the 'Y' field."
        if not (args or kwargs):
            args = (default_msg,)
        elif _EXCEPTION_CLASSES._VALUE in kwargs:
            if _EXCEPTION_CLASSES._FIELD in kwargs:
                custom_msg = custom_msg.replace('X', kwargs[_EXCEPTION_CLASSES._VALUE])
                custom_msg = custom_msg.replace('Y', kwargs[_EXCEPTION_CLASSES._FIELD])
            else:
                custom_msg = f"{custom_msg.replace('X', kwargs[_EXCEPTION_CLASSES._VALUE]).split(' for the')[0]}."
            args = (custom_msg,)
        super().__init__(*args)


class InvalidRequestTypeError(PyDPlusError, ValueError):
    """Exception used when an invalid API request type is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied request type for the API is not recognized. (Examples of valid " + \
                      "request types include 'POST' and 'PUT')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class LookupMismatchError(PyDPlusError):
    """Exception used when a lookup value does not match the supplied lookup type."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied lookup type for the API does not match the value that was provided."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class NotFoundResponseError(PyDPlusError):
    """Exception used when an API query returns a 404 response and there is not a more specific class."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API query returned a 404 response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PATCHRequestError(PyDPlusError):
    """This exception is used for generic PATCH request errors when there is not a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = _EXCEPTION_CLASSES._API_DEFAULT_MSG.format(type=API_REQUEST_TYPES.PATCH)
        if _EXCEPTION_CLASSES._STATUS_CODE in kwargs or _EXCEPTION_CLASSES._MESSAGE in kwargs:
            custom_msg = _construct_api_custom_message(_request_type=API_REQUEST_TYPES.PATCH,
                                                       _message=kwargs.get(_EXCEPTION_CLASSES._MESSAGE, None),
                                                       _status_code=kwargs.get(_EXCEPTION_CLASSES._STATUS_CODE, None))
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PayloadMismatchError(PyDPlusError):
    """Exception used when more than one payload is supplied for an API request."""
    def __init__(self, *args, **kwargs):
        default_msg = "More than one payload was provided for the API call when only one is permitted."
        if not (args or kwargs):
            args = (default_msg,)
        elif kwargs[_EXCEPTION_CLASSES._REQUEST_TYPE]:
            custom_msg = default_msg.replace('API call', f'{kwargs[_EXCEPTION_CLASSES._REQUEST_TYPE].upper()} request')
            args = (custom_msg,)
        super().__init__(*args)


class POSTRequestError(PyDPlusError):
    """Exception used for generic POST request errors when there is not a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = _EXCEPTION_CLASSES._API_DEFAULT_MSG.format(type=API_REQUEST_TYPES.POST)
        if _EXCEPTION_CLASSES._STATUS_CODE in kwargs or _EXCEPTION_CLASSES._MESSAGE in kwargs:
            custom_msg = _construct_api_custom_message(_request_type=API_REQUEST_TYPES.POST,
                                                       _message=kwargs.get(_EXCEPTION_CLASSES._MESSAGE, None),
                                                       _status_code=kwargs.get(_EXCEPTION_CLASSES._STATUS_CODE, None))
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PUTRequestError(PyDPlusError):
    """Exception used for generic PUT request errors when there is not a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = _EXCEPTION_CLASSES._API_DEFAULT_MSG.format(type=API_REQUEST_TYPES.PUT)
        if _EXCEPTION_CLASSES._STATUS_CODE in kwargs or _EXCEPTION_CLASSES._MESSAGE in kwargs:
            custom_msg = _construct_api_custom_message(_request_type=API_REQUEST_TYPES.PUT,
                                                       _message=kwargs.get(_EXCEPTION_CLASSES._MESSAGE, None),
                                                       _status_code=kwargs.get(_EXCEPTION_CLASSES._STATUS_CODE, None))
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


# -----------------------------
# Helper Exceptions
# -----------------------------


class InvalidHelperFileTypeError(PyDPlusError, ValueError):
    """Exception used when an invalid file type is provided for the helper file."""
    def __init__(self, *args, **kwargs):
        if not (args or kwargs):
            args = (_EXCEPTION_CLASSES._INVALID_HELPER_DEFAULT_MSG,)
        super().__init__(*args)


class InvalidHelperArgumentsError(PyDPlusError):
    """Exception used when the helper function was called with arguments instead of keyword arguments."""
    def __init__(self, *args, **kwargs):
        default_msg = "The helper configuration file only accepts basic keyword arguments. (e.g. arg_name='arg_value')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class HelperFunctionNotFoundError(PyDPlusError):
    """Exception used when a function referenced in the helper config file does not exist."""
    def __init__(self, *args, **kwargs):
        default_msg = "The function referenced in the helper configuration file could not be found."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


# -----------------------------
# Constructor Functions
# -----------------------------


def _construct_api_custom_message(
        _request_type: str,
        _message: Optional[str] = None,
        _status_code: Union[Optional[str], Optional[int]] = None
) -> str:
    """Constructions the exception message for an API-related exception class.

    :param _request_type: The associated API request type (``GET``, ``PATCH``, ``POST``, ``PUT``, or ``DELETE``)
    :type _request_type: str
    :param _message: A specific message to append to the base message (optional)
    :type _message: str
    :param _status_code: The status code returned from the API request (optional)
    :type _status_code: str, int, None
    :returns: The constructed custom message to use when raising the exception
    """
    # Define the base custom message
    _custom_msg = _EXCEPTION_CLASSES._API_CUSTOM_MSG.format(type=_request_type.upper())

    # Define the status code custom message if a status code was provided
    if _status_code:
        _status_code_msg = f'returned the {_status_code} status code'
        _custom_msg = _custom_msg.replace('failed', _status_code_msg)

    # Construct the standard custom message if a custom message string was provided
    if _message:
        _custom_msg = f'{_custom_msg} {_message}'
    elif _status_code:
        # Adjust the status code message
        _custom_msg = _custom_msg.split(_EXCEPTION_CLASSES._WITH_THE_FOLLOWING_SEGMENT)[0] + "."
    else:
        # Revert back to the default message if a custom message was not provided
        _custom_msg = _EXCEPTION_CLASSES._API_DEFAULT_MSG.format(type=_request_type.upper())

    # Return the constructed message
    return _custom_msg
