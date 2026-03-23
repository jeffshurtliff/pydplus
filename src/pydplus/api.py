# -*- coding: utf-8 -*-
"""
:Module:            pydplus.api
:Synopsis:          Defines the basic functions associated with the RSA ID Plus API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     21 Mar 2026
"""

from __future__ import annotations

import logging
from typing import Optional, Union

import requests

from . import errors
from . import constants as const

logger = logging.getLogger(__name__)


def get(
        pydp_object,
        endpoint: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_type: str = const.DEFAULT_API_TYPE,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Perform a GET request against the ID Plus tenant.

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
    :type timeout: int
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (If not explicitly defined then ``True`` if Strict Mode is disabled)
    :type allow_failed_response: bool, None
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

    # Examine the result
    allow_failed_response = _should_allow_failed_responses(pydp_object, allow_failed_response)
    if response.status_code >= 300 and not allow_failed_response:
        _raise_status_code_exception(response, const.API_REQUEST_TYPES.GET, show_full_error)
    if return_json:
        response = _convert_response_to_json(response, allow_failed_response)
    return response


def api_call_with_payload(
        pydp_object,
        method: str,
        endpoint: str,
        payload: Union[Optional[dict], Optional[str]] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_type: str = const.DEFAULT_API_TYPE,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Perform an API call with payload against the ID Plus tenant.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param method: The API method (``post``, ``put``, or ``patch``)
    :type method: str
    :param endpoint: The API endpoint to query
    :type endpoint: str
    :param payload: The payload to leverage in the API call
    :type payload: dict, str, None
    :param params: The query parameters (where applicable)
    :type params: dict, None
    :param headers: Specific API headers to use when performing the API call (beyond the base headers)
    :type headers: dict, None
    :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
    :type api_type: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (If not explicitly defined then ``True`` if Strict Mode is disabled)
    :type allow_failed_response: bool, None
    :returns: The API response in JSON format or as a ``requests`` object
    :raises: :py:exc:`TypeError`,
             :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`
    """
    def _raise_exception_for_payload():
        """Raise a :py:exc:`TypeError` exception when the payload is an invalid data type."""
        _error_msg = f'The API payload must be a dictionary or string (provided: {type(payload)})'
        logger.error(_error_msg)
        raise TypeError(_error_msg)

    # Define the parameters as an empty dictionary if none are provided
    params = {} if params is None else params

    # Define the headers
    headers = {} if headers is None else headers
    headers = _get_headers(pydp_object.base_headers, headers)

    # Perform the API call
    response = None
    full_api_url = _get_full_api_url(pydp_object, endpoint, api_type)
    if isinstance(method, str) and method.upper() == const.API_REQUEST_TYPES.POST:
        if isinstance(payload, dict):
            response = requests.post(full_api_url, json=payload, headers=headers, params=params, timeout=timeout,
                                     verify=pydp_object.verify_ssl)
        elif isinstance(payload, str):
            response = requests.post(full_api_url, data=payload, headers=headers, params=params, timeout=timeout,
                                     verify=pydp_object.verify_ssl)
        else:
            _raise_exception_for_payload()
    elif isinstance(method, str) and method.upper() == const.API_REQUEST_TYPES.PATCH:
        if isinstance(payload, dict):
            response = requests.patch(full_api_url, json=payload, headers=headers, params=params, timeout=timeout,
                                      verify=pydp_object.verify_ssl)
        elif isinstance(payload, str):
            response = requests.patch(full_api_url, data=payload, headers=headers, params=params, timeout=timeout,
                                      verify=pydp_object.verify_ssl)
        else:
            _raise_exception_for_payload()
    elif isinstance(method, str) and method.upper() == const.API_REQUEST_TYPES.PUT:
        if isinstance(payload, dict):
            response = requests.put(full_api_url, json=payload, headers=headers, params=params, timeout=timeout,
                                    verify=pydp_object.verify_ssl)
        elif isinstance(payload, str):
            response = requests.put(full_api_url, data=payload, headers=headers, params=params, timeout=timeout,
                                    verify=pydp_object.verify_ssl)
        else:
            _raise_exception_for_payload()
    else:
        if isinstance(method, str) and method.upper() == const.API_REQUEST_TYPES.GET:
            error_msg = "The 'GET' API call method is not valid when a payload has been provided."
        else:
            error_msg = 'A valid API call method (POST or PATCH or PUT) must be defined.'
        logger.error(error_msg)
        raise errors.exceptions.APIMethodError(error_msg)

    # Examine the result
    allow_failed_response = _should_allow_failed_responses(pydp_object, allow_failed_response)
    if response and response.status_code >= 300 and not allow_failed_response:
        _raise_status_code_exception(response, method, show_full_error)
    if response and return_json:
        response = _convert_response_to_json(response, allow_failed_response)
    return response


def post(
        pydp_object,
        endpoint: str,
        payload: Union[Optional[dict], Optional[str]] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_type: str = const.DEFAULT_API_TYPE,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Perform a POST call with payload against the ID Plus tenant.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param endpoint: The API endpoint to query
    :type endpoint: str
    :param payload: The payload to leverage in the API call
    :type payload: dict, str, None
    :param params: The query parameters (where applicable)
    :type params: dict, None
    :param headers: Specific API headers to use when performing the API call (beyond the base headers)
    :type headers: dict, None
    :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
    :type api_type: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (If not explicitly defined then ``True`` if Strict Mode is disabled)
    :type allow_failed_response: bool, None
    :returns: The API response in JSON format or as a ``requests`` object
    :raises: :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`
    """
    return api_call_with_payload(pydp_object=pydp_object, method=const.API_REQUEST_TYPES.POST, endpoint=endpoint,
                                 payload=payload, params=params, headers=headers, api_type=api_type, timeout=timeout,
                                 show_full_error=show_full_error, return_json=return_json,
                                 allow_failed_response=allow_failed_response)


def patch(
        pydp_object,
        endpoint: str,
        payload: Union[Optional[dict], Optional[str]] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_type: str = const.DEFAULT_API_TYPE,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Perform a PATCH call with payload against the ID Plus tenant.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param endpoint: The API endpoint to query
    :type endpoint: str
    :param payload: The payload to leverage in the API call
    :type payload: dict, str, None
    :param params: The query parameters (where applicable)
    :type params: dict, None
    :param headers: Specific API headers to use when performing the API call (beyond the base headers)
    :type headers: dict, None
    :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
    :type api_type: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (If not explicitly defined then ``True`` if Strict Mode is disabled)
    :type allow_failed_response: bool, None
    :returns: The API response in JSON format or as a ``requests`` object
    :raises: :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`
    """
    return api_call_with_payload(pydp_object=pydp_object, method=const.API_REQUEST_TYPES.PATCH, endpoint=endpoint,
                                 payload=payload, params=params, headers=headers, api_type=api_type, timeout=timeout,
                                 show_full_error=show_full_error, return_json=return_json,
                                 allow_failed_response=allow_failed_response)


def put(
        pydp_object,
        endpoint: str,
        payload: Union[Optional[dict], Optional[str]] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_type: str = const.DEFAULT_API_TYPE,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Perform a PUT call with payload against the ID Plus tenant.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param endpoint: The API endpoint to query
    :type endpoint: str
    :param payload: The payload to leverage in the API call
    :type payload: dict, str, None
    :param params: The query parameters (where applicable)
    :type params: dict, None
    :param headers: Specific API headers to use when performing the API call (beyond the base headers)
    :type headers: dict, None
    :param api_type: Indicates if the ``admin`` (default) or ``auth`` API will be leveraged.
    :type api_type: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (If not explicitly defined then ``True`` if Strict Mode is disabled)
    :type allow_failed_response: bool, None
    :returns: The API response in JSON format or as a ``requests`` object
    :raises: :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`
    """
    return api_call_with_payload(pydp_object=pydp_object, method=const.API_REQUEST_TYPES.PUT, endpoint=endpoint,
                                 payload=payload, params=params, headers=headers, api_type=api_type, timeout=timeout,
                                 show_full_error=show_full_error, return_json=return_json,
                                 allow_failed_response=allow_failed_response)


def _should_allow_failed_responses(_pydp_object, _allow_failed_response: Optional[bool]) -> bool:
    """Determine if failed responses are allowed based on the defined value or strict mode setting."""
    # Only define the value if not already defined
    if not isinstance(_allow_failed_response, bool) or _allow_failed_response is None:
        try:
            # Define the value based on the strict mode define in the instantiated object
            _allow_failed_response = False if _pydp_object.strict_mode is True else True
        except Exception as _exc:
            # Use the default strict mode value to define the value if an exception is raised
            _allow_failed_response = False if const.DEFAULT_STRICT_MODE is True else True
            _exc_type = errors.handlers.get_exception_type(_exc)
            _error_msg = f'Using default strict mode due to the following {_exc_type} exception: {_exc}'
            logger.error(_error_msg)
    return _allow_failed_response


def _get_headers(
        _headers: dict,
        _additional_headers: Optional[dict] = None,
        _header_type: str = const.DEFAULT_HEADER_TYPE,
) -> dict:
    """Return the appropriate HTTP headers to use for different types of API calls."""
    _additional_headers = {} if _additional_headers is None else _additional_headers
    # TODO: Define additional headers as needed based on header type
    _headers.update(_additional_headers)
    return _headers


def _get_full_api_url(_pydp_object, _endpoint: str, _api_type: str = const.DEFAULT_API_TYPE) -> str:
    """Construct the full API URL to use in an API call based on the API type.

    :param _pydp_object: The instantiated pydplus object
    :type _pydp_object: class[pydplus.PyDPlus]
    :param _endpoint: The API endpoint to be called
    :type _endpoint: str
    :param _api_type: Indicates which API to leverage: ``admin`` (default) or ``auth``
    :type _api_type: str
    :returns: The full API URL path including the base URL as a string
    :raises: :py:exc:`pydplus.errors.exceptions.InvalidFieldError`
    """
    # Define the base URL to leverage based on the API type or raise an exception if API type is invalid
    if _api_type.lower() == const.ADMIN_API_TYPE:
        _base_url = _pydp_object.admin_base_rest_url
    elif _api_type.lower() == const.AUTH_API_TYPE:
        _base_url = _pydp_object.auth_base_rest_url
    else:
        if not isinstance(_api_type, str):
            _error_msg = f'The API Type value must be a string. (provided: {type(_api_type)})'
        else:
            _error_msg = f"The value '{_api_type}' is not a valid API type. "
            _error_msg += f"(expected: '{const.ADMIN_API_TYPE}' or '{const.AUTH_API_TYPE}')"
        logger.error(_error_msg)
        raise errors.exceptions.InvalidFieldError(_error_msg)

    # Make sure the endpoint begins with a slash
    _endpoint = f'/{_endpoint}' if not _endpoint.startswith('/') else _endpoint

    # Return the crafted full API URL
    return f'{_base_url}{_endpoint}'


def _raise_status_code_exception(_response, _method: str, _show_full_error: bool = True) -> None:
    """Raise an exception when a non-OK status code is returned for an API call.

    :param _response: The API response
    :param _method: The API request type (``GET``, ``POST``, ``PATCH``, ``PUT``, or ``DELETE``)
    :type _method: str
    :param _show_full_error: Determine if the full error message should be reported (``True`` by default)
    :type _show_full_error: bool
    :returns: None
    :raises: :py:exc:`pydplus.errors.exceptions.APIRequestError`
    """
    _exc_msg = f'The {_method.upper()} request failed with a {_response.status_code} status code.'
    if _show_full_error:
        _exc_msg += f'\n{_response.text}'
    logger.error(_exc_msg)
    raise errors.exceptions.APIRequestError(_exc_msg)


def _convert_response_to_json(_response, _allow_failed_response: bool = False):
    """Attempt to convert an API response to JSON format and raises an exception if unsuccessful.

    :param _response: The API response
    :param _allow_failed_response: Determines if failed responses are accepted (``False`` by default) or if an
                                  exception should be raised if the conversion fails
    :type _allow_failed_response: bool
    :returns: The API response converted to a JSON dictionary (or returned unchanged if the conversion failed and
              no exception was raised)
    :raises: :py:exc:`pydplus.errors.exceptions.APIResponseConversionError`
    """
    try:
        _response = _response.json()
    except Exception as _exc:
        _exc_type = errors.handlers.get_exception_type(_exc)
        _error_msg = (f'Failed to convert the API response to JSON format due to the following {_exc_type} '
                      f'exception: {_exc}')
        logger.error(_error_msg)
        if not _allow_failed_response:
            raise errors.exceptions.APIResponseConversionError(_error_msg)
    return _response
