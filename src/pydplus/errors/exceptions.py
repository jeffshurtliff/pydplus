# -*- coding: utf-8 -*-
"""
:Module:            pydplus.errors.exceptions
:Synopsis:          Collection of exception classes relating to the pydplus library
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 June 2025
"""

#################
# Base Exception
#################


# Define base exception class
class PyDPlusError(Exception):
    """This is the base class for PyDPlus exceptions."""
    pass


#####################
# General Exceptions
#####################


class CurrentlyUnsupportedError(PyDPlusError):
    """This exception is used when a feature or functionality being used is currently unsupported.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "This feature is currently unsupported at this time."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'message' in kwargs:
            args =(kwargs['message'],)
        else:
            custom_msg = f"The '{args[0]}' {default_msg.split('This ')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class DataMismatchError(PyDPlusError):
    """This exception is used when there is a mismatch between two data sources.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "A data mismatch was found with the data sources."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'data' in kwargs:
            multi_types = [list, tuple, set]
            if isinstance(kwargs['data'], str):
                custom_msg = f"{default_msg.split('the data')[0]}the '{kwargs['data']}'{default_msg.split('with the')[1]}"
                custom_msg = custom_msg.replace('sources', 'source')
                args = (custom_msg,)
            elif type(kwargs['data']) in multi_types and len(kwargs['data']) == 2:
                custom_section = f"'{kwargs['data'][0]}' and '{kwargs['data'][1]}'"
                custom_msg = f"{default_msg.split('data sources')[0]}{custom_section}{default_msg.split('with the')[1]}"
                args = (custom_msg,)
        super().__init__(*args)


class InvalidParameterError(PyDPlusError):
    """This exception is used when an invalid parameter is provided.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The parameter that was provided is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('parameter ')[0]}'{kwargs['val']}'{default_msg.split('The')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class InvalidFieldError(PyDPlusError):
    """This exception is used when an invalid field is provided.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The field that was provided is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('field ')[0]}'{kwargs['val']}'{default_msg.split('The')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class InvalidURLError(PyDPlusError):
    """This exception is used when a provided URL is invalid.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The provided URL is invalid"
        if not (args or kwargs):
            args = (default_msg,)
        elif 'url' in kwargs:
            custom_msg = f"{default_msg.split('is')[0]}'{kwargs['url']}'{default_msg.split('URL')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class MissingRequiredDataError(PyDPlusError):
    """This exception is used when a function or method is missing one or more required arguments.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "Missing one or more required parameters"
        init_msg = "The object failed to initialize as it is missing one or more required arguments."
        param_msg = "The required parameter 'PARAMETER_NAME' is not defined"
        if not (args or kwargs):
            args = (default_msg,)
        elif 'init' in args or 'initialize' in args:
            if 'object' in kwargs:
                custom_msg = f"{init_msg.split('object')[0]}'{kwargs['object']}'{init_msg.split('The')[1]}"
                args = (custom_msg,)
            else:
                args = (init_msg,)
        elif 'param' in kwargs:
            args = (param_msg.replace('PARAMETER_NAME', kwargs['param']),)
        super().__init__(*args)


class UnknownFileTypeError(PyDPlusError):
    """This exception is used when a file type for a given file cannot be identified.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The file type of the given file path cannot be identified."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'file' in kwargs:
            custom_msg = f"{default_msg.split('path')[0]}'{kwargs['file']}'{default_msg.split('path')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


#########################
# Generic API Exceptions
#########################


class APIConnectionError(PyDPlusError):
    """This exception is used when the API query could not be completed due to connection aborts and/or timeouts.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API query could not be completed due to connection aborts and/or timeouts."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class APIMethodError(PyDPlusError):
    """This exception is used when an invalid API call method is used when performing an API call.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "A valid API call method (GET or POST or PATCH or PUT) must be defined."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class APIRequestError(PyDPlusError):
    """This exception is used for generic API request errors when there is not a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class APIResponseConversionError(PyDPlusError):
    """This exception is used for errors when attempting to convert an API response to another data format. (e.g. JSON)

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API response failed to be converted to the specified data format."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class DELETERequestError(PyDPlusError):
    """This exception is used for generic DELETE request errors when there is not a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The DELETE request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class FeatureNotConfiguredError(PyDPlusError):
    """This exception is used when an API request fails because a feature is not configured.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        exc_msg = "The feature is not configured."
        if 'identifier' in kwargs or 'feature' in kwargs:
            if 'identifier' in kwargs:
                exc_msg += f" Identifier: {kwargs['identifier']}"
            if 'feature' in kwargs:
                exc_msg = exc_msg.replace("feature", f"{kwargs['feature']} feature")
            args = (exc_msg,)
        elif not (args or kwargs):
            args = (exc_msg,)
        super().__init__(*args)


class GETRequestError(PyDPlusError):
    """This exception is used for generic GET request errors when there is not a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The GET request did not return a successful response."
        custom_msg = "The GET request failed with the following message:"
        if 'status_code' in kwargs or 'message' in kwargs:
            if 'status_code' in kwargs:
                status_code_msg = f"returned the {kwargs['status_code']} status code"
                custom_msg = custom_msg.replace('failed', status_code_msg)
            if 'message' in kwargs:
                custom_msg = f"{custom_msg} {kwargs['message']}"
            else:
                custom_msg = custom_msg.split(' with the following')[0] + "."
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidEndpointError(PyDPlusError):
    """This exception is used when an invalid API endpoint or service is provided.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied endpoint for the API is not recognized."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidLookupTypeError(PyDPlusError):
    """This exception is used when an invalid API lookup type is provided.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied lookup type for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'id' and 'email')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidPayloadValueError(PyDPlusError):
    """This exception is used when an invalid value is provided for a payload field.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "An invalid payload value was provided."
        custom_msg = "The invalid payload value 'X' was provided for the 'Y' field."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'value' in kwargs:
            if 'field' in kwargs:
                custom_msg = custom_msg.replace('X', kwargs['value']).replace('Y', kwargs['field'])
            else:
                custom_msg = f"{custom_msg.replace('X', kwargs['value']).split(' for the')[0]}."
            args = (custom_msg,)
        super().__init__(*args)


class InvalidRequestTypeError(PyDPlusError):
    """This exception is used when an invalid API request type is provided.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied request type for the API is not recognized. (Examples of valid " + \
                      "request types include 'POST' and 'PUT')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class LookupMismatchError(PyDPlusError):
    """This exception is used when an a lookup value does not match the supplied lookup type.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied lookup type for the API does not match the value that was provided."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class NotFoundResponseError(PyDPlusError):
    """This exception is used when an API query returns a 404 response and there is not a more specific class.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API query returned a 404 response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PayloadMismatchError(PyDPlusError):
    """This exception is used when more than one payload is supplied for an API request.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "More than one payload was provided for the API call when only one is permitted."
        if not (args or kwargs):
            args = (default_msg,)
        elif kwargs['request_type']:
            custom_msg = default_msg.replace("API call", f"{kwargs['request_type'].upper()} request")
            args = (custom_msg,)
        super().__init__(*args)


class POSTRequestError(PyDPlusError):
    """This exception is used for generic POST request errors when there is not a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The POST request did not return a successful response."
        custom_msg = "The POST request failed with the following message:"
        if 'status_code' in kwargs or 'message' in kwargs:
            if 'status_code' in kwargs:
                status_code_msg = f"returned the {kwargs['status_code']} status code"
                custom_msg = custom_msg.replace('failed', status_code_msg)
            if 'message' in kwargs:
                custom_msg = f"{custom_msg} {kwargs['message']}"
            else:
                custom_msg = custom_msg.split(' with the following')[0] + "."
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PUTRequestError(PyDPlusError):
    """This exception is used for generic PUT request errors when there is not a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The PUT request did not return a successful response."
        custom_msg = "The PUT request failed with the following message:"
        if 'status_code' in kwargs or 'message' in kwargs:
            if 'status_code' in kwargs:
                status_code_msg = f"returned the {kwargs['status_code']} status code"
                custom_msg = custom_msg.replace('failed', status_code_msg)
            if 'message' in kwargs:
                custom_msg = f"{custom_msg} {kwargs['message']}"
            else:
                custom_msg = custom_msg.split(' with the following')[0] + "."
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


####################
# Helper Exceptions
####################


class InvalidHelperFileTypeError(PyDPlusError, ValueError):
    """This exception is used when an invalid file type is provided for the helper file.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The helper configuration file can only have the 'yaml' or 'json' file type."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidHelperArgumentsError(PyDPlusError):
    """This exception is used when the helper function was supplied arguments instead of keyword arguments.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The helper configuration file only accepts basic keyword arguments. (e.g. arg_name='arg_value')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class HelperFunctionNotFoundError(PyDPlusError):
    """This exception is used when a function referenced in the helper config file does not exist.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The function referenced in the helper configuration file could not be found."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)
