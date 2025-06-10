# -*- coding: utf-8 -*-
"""
:Module:            pydplus.api
:Synopsis:          Defines the basic functions associated with the RSA ID Plus API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Jun 2025
"""

import requests

from . import errors
from .utils import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)

# Define constants
DEFAULT_TIMEOUT = 30
DEFAULT_API_TYPE = 'admin'


def get(pydp_object, endpoint, params=None, headers=None, api_type=DEFAULT_API_TYPE, timeout=DEFAULT_TIMEOUT,
        show_full_error=True, return_json=True, allow_failed_response=False):
    """This function performs a GET request against the ID Plus tenant.

    .. versionadded:: 1.0.0

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param endpoint: The API endpoint to query
    :type endpoint: str
    :param params: The query parameters (where applicable)
    :type params: dict, None
    :param headers: Specific API headers to use when performing the API call (beyond the base headers)
    :type headers: dict, None
    :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
    :type api_type: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (``False`` by default)
    :type allow_failed_response: bool
    :returns: The API response in JSON format or as a ``requests`` object
    :raises: :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`
    """
    # Define the parameters as an empty dictionary if none are provided
    params = {} if params is None else params

    # Define the headers
    headers = {} if headers is None else headers
    headers = _get_headers(pydp_object.base_headers, headers)

    # Perform the API call
    full_api_url = _get_full_api_url(pydp_object, endpoint, api_type)
    response = requests.get(
        full_api_url,
        headers=headers,
        params=params,
        timeout=timeout,
        verify=pydp_object.verify_ssl
    )
    if response.status_code >= 300 and not allow_failed_response:
        _raise_status_code_exception(response, 'GET', show_full_error)
    if return_json:
        response = _convert_response_to_json(response, allow_failed_response)
    return response


def api_call_with_payload(pydp_object, method, endpoint, payload, params=None, headers=None, api_type=DEFAULT_API_TYPE,
                          timeout=DEFAULT_TIMEOUT, show_full_error=True, return_json=True, allow_failed_response=False):
    """This function performs an API call with payload against the ID Plus tenant.

    .. versionadded:: 1.0.0

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param method: The API method (``post``, ``put``, or ``patch``)
    :type method: str
    :param endpoint: The API endpoint to query
    :type endpoint: str
    :param payload: The payload to leverage in the API call
    :type payload: dict
    :param params: The query parameters (where applicable)
    :type params: dict, None
    :param headers: Specific API headers to use when performing the API call (beyond the base headers)
    :type headers: dict, None
    :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
    :type api_type: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (``False`` by default)
    :type allow_failed_response: bool
    :returns: The API response in JSON format or as a ``requests`` object
    :raises: :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`
    """
    # Define the parameters as an empty dictionary if none are provided
    params = {} if params is None else params

    # Define the headers
    headers = {} if headers is None else headers
    headers = _get_headers(pydp_object.base_headers, headers)

    # Perform the API call
    full_api_url = _get_full_api_url(pydp_object, endpoint, api_type)
    if isinstance(method, str) and method.lower() == 'post':
        response = requests.post(full_api_url, json=payload, headers=headers, params=params, timeout=timeout,
                                 verify=pydp_object.verify_ssl)
    elif isinstance(method, str) and method.lower() == 'patch':
        response = requests.patch(full_api_url, json=payload, headers=headers, params=params, timeout=timeout,
                                  verify=pydp_object.verify_ssl)
    elif isinstance(method, str) and method.lower() == 'put':
        response = requests.put(full_api_url, json=payload, headers=headers, params=params, timeout=timeout,
                                verify=pydp_object.verify_ssl)
    else:
        error_msg = 'A valid API call method (POST or PATCH or PUT) must be defined.'
        if isinstance(method, str) and method.lower() == 'get':
            error_msg = "The 'GET' API call method is not valid when a payload has been provided."
        logger.error(error_msg)
        raise errors.exceptions.APIMethodError(error_msg)

    # Examine the result
    if response.status_code >= 300 and not allow_failed_response:
        _raise_status_code_exception(response, method, show_full_error)
    if return_json:
        response = _convert_response_to_json(response, allow_failed_response)
    return response


def post(pydp_object, endpoint, payload, params=None, headers=None, api_type=DEFAULT_API_TYPE, timeout=DEFAULT_TIMEOUT,
         show_full_error=True, return_json=True, allow_failed_response=False):
    """This function performs a POST call with payload against the ID Plus tenant.

    .. versionadded:: 1.0.0

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param endpoint: The API endpoint to query
    :type endpoint: str
    :param payload: The payload to leverage in the API call
    :type payload: dict
    :param params: The query parameters (where applicable)
    :type params: dict, None
    :param headers: Specific API headers to use when performing the API call (beyond the base headers)
    :type headers: dict, None
    :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
    :type api_type: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (``False`` by default)
    :type allow_failed_response: bool
    :returns: The API response in JSON format or as a ``requests`` object
    :raises: :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`
    """
    return api_call_with_payload(pydp_object=pydp_object, method='post', endpoint=endpoint, payload=payload,
                                 params=params, headers=headers, api_type=api_type, timeout=timeout,
                                 show_full_error=show_full_error, return_json=return_json,
                                 allow_failed_response=allow_failed_response)


def put(pydp_object, endpoint, payload, params=None, headers=None, api_type=DEFAULT_API_TYPE, timeout=DEFAULT_TIMEOUT,
        show_full_error=True, return_json=True, allow_failed_response=False):
    """This function performs a PUT call with payload against the ID Plus tenant.

    .. versionadded:: 1.0.0

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param endpoint: The API endpoint to query
    :type endpoint: str
    :param payload: The payload to leverage in the API call
    :type payload: dict
    :param params: The query parameters (where applicable)
    :type params: dict, None
    :param headers: Specific API headers to use when performing the API call (beyond the base headers)
    :type headers: dict, None
    :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
    :type api_type: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (``False`` by default)
    :type allow_failed_response: bool
    :returns: The API response in JSON format or as a ``requests`` object
    :raises: :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`
    """
    return api_call_with_payload(pydp_object=pydp_object, method='put', endpoint=endpoint, payload=payload,
                                 params=params, headers=headers, api_type=api_type, timeout=timeout,
                                 show_full_error=show_full_error, return_json=return_json,
                                 allow_failed_response=allow_failed_response)


def _get_headers(_headers, _additional_headers=None, _header_type='default'):
    """This function returns the appropriate HTTP headers to use for different types of API calls.

    .. versionadded:: 1.0.0
    """
    _additional_headers = {} if _additional_headers is None else _additional_headers
    # TODO: Define additional headers as needed based on header type
    _headers.update(_additional_headers)
    return _headers


def _get_full_api_url(_pydp_object, _endpoint, _api_type=DEFAULT_API_TYPE):
    """This function constructs the full API URL to use in an API call based on the API type.

    .. versionadded:: 1.0.0
    """
    # Define the base URL to leverage based on the API type or raise an exception if API type is invalid
    if _api_type.lower() == 'admin':
        _base_url = _pydp_object.admin_base_url
    elif _api_type.lower() == 'auth':
        _base_url = _pydp_object.auth_base_url
    else:
        if not isinstance(_api_type, str):
            _error_msg = 'The API Type value must be a string.'
        else:
            _error_msg = f"The value '{_api_type}' is not a valid API type."
        logger.error(_error_msg)
        raise errors.exceptions.InvalidFieldError(_error_msg)

    # Make sure the endpoint begins with a slash
    _endpoint = f'/{_endpoint}' if not _endpoint.startswith('/') else _endpoint

    # Return the crafted full API URL
    return f'{_base_url}{_endpoint}'


def _raise_status_code_exception(_response, _method, _show_full_error=True):
    """This function raises an APIRequestError when a non-OK status code is returned for an API call.

    .. versionadded:: 1.0.0
    """
    _exc_msg = f'The {_method.upper()} request failed with a {_response.status_code} status code.'
    if _show_full_error:
        _exc_msg += f'\n{_response.text}'
    logger.error(_exc_msg)
    raise errors.exceptions.APIRequestError(_exc_msg)


def _convert_response_to_json(_response, allow_failed_response=False):
    """This function attempts to convert an API response to JSON format and raises an exception if unsuccessful.

    .. versionadded:: 1.0.0
    """
    try:
        _response = _response.json()
    except Exception as _exc:
        _exc_type = type(_exc).__name__
        _error_msg = (f'Failed to convert the API response to JSON format due to the following {_exc_type} '
                      f'exception: {_exc}')
        logger.error(_error_msg)
        if not allow_failed_response:
            raise errors.exceptions.APIResponseConversionError(_error_msg)
    return _response
