# -*- coding: utf-8 -*-
"""
:Module:            pydplus.users
:Synopsis:          Defines the user-related functions associated with the RSA ID Plus API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     25 Mar 2026
"""

from __future__ import annotations

import logging
from typing import Optional, Union

from . import api, errors
from . import constants as const

logger = logging.getLogger(__name__)


def get_user_details(
        pydp_object,
        email: str,
        search_unsynced: Optional[bool] = None,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Retrieve the details for a specific user based on their email address.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param email: The email address of the user for whom to retrieve details
    :type email: str
    :param search_unsynced: Indicates if the user search should include unsynchronized users (optional)
    :type search_unsynced: bool, None
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type return_json: bool
    :param allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (If not explicitly defined then ``True`` if Strict Mode is disabled)
    :type allow_failed_response: bool, None
    :returns: The user details in JSON format or the API response as a ``requests`` object
    :raises: :py:exc:`TypeError`,
             :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`
    """
    # Define the payload
    payload: dict[str, Union[str, bool]] = {
        const.QUERY_PARAMS.EMAIL: email,
    }
    if search_unsynced is not None:
        if not isinstance(search_unsynced, bool):
            error_msg = f'The value of the search_unsynced parameter must be Boolean. (Provided: {type(search_unsynced)})'
            logger.error(error_msg)
            raise TypeError(error_msg)
        payload[const.QUERY_PARAMS.SEARCH_UNSYNCED] = search_unsynced

    # Perform the API call and return the response in JSON format
    return api.post(pydp_object=pydp_object, endpoint=const.REST_PATHS.USERS_LOOKUP, payload=payload,
                    api_type=const.ADMIN_API_TYPE, timeout=timeout, show_full_error=show_full_error,
                    return_json=return_json, allow_failed_response=allow_failed_response)


def get_user_id(
        pydp_object,
        email: str = None,
        user_details: Optional[dict] = None,
        search_unsynced: Optional[bool] = None,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
) -> str:
    """Retrieve the User ID associated with a specific user.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param email: The email address of the user for whom to retrieve details
    :type email: str, None
    :param user_details: The user details data from the :py:func:`pydplus.users.get_user_details` function
    :type user_details: dict, None
    :param search_unsynced: Indicates if the user search should include unsynchronized users (optional)
    :type search_unsynced: bool, None
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int
    :param show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type show_full_error: bool
    :returns: The User ID for the given user as a string (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
              or an empty string if the User ID could not be retrieved successfully
    :raises: :py:exc:`TypeError`,
             :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    # Ensure one of the lookup values was provided
    if not any((email, user_details)):
        error_msg = 'An email address or user details dictionary must be provided to retrieve a user ID.'
        logger.error(error_msg)
        raise errors.exceptions.MissingRequiredDataError(error_msg)

    # Retrieve the user details if not provided
    if not user_details:
        user_details = get_user_details(pydp_object=pydp_object, email=email, search_unsynced=search_unsynced,
                                        timeout=timeout, show_full_error=show_full_error, allow_failed_response=True)

    # Locate and return the user ID if possible
    if not user_details or not isinstance(user_details, dict) or const.RESPONSE_KEYS.ID not in user_details:
        error_msg = 'Failed to retrieve the user ID for the queried user. An empty string will be returned for the ID.'
        logger.error(error_msg)
        return ''
    return user_details.get(const.RESPONSE_KEYS.ID, '')


def _update_user_status(
        _pydp_object,
        _user_id: str,
        _action: str,
        _timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        _show_full_error: bool = True,
        _return_json: bool = True,
        _allow_failed_response: Optional[bool] = None,
):
    """Enable or disable a user by calling the User Status API.

    :param _pydp_object: The instantiated pydplus object
    :type _pydp_object: class[pydplus.PyDPlus]
    :param _user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
    :type _user_id: str
    :param _action: The action to be performed (Accepted values: ``enable``, ``disable``)
    :type _action: str
    :param _timeout: The timeout period in seconds (defaults to ``30``)
    :type _timeout: int
    :param _show_full_error: Determines if the full error message should be displayed (defaults to ``True``)
    :type _show_full_error: bool
    :param _return_json: Determines if the response should be returned in JSON format (defaults to ``True``)
    :type _return_json: bool
    :param _allow_failed_response: Indicates that failed responses should return and should not raise an exception
                                  (If not explicitly defined then ``True`` if Strict Mode is disabled)
    :type _allow_failed_response: bool, None
    :returns: The API response in JSON format or as a ``requests`` object
    :raises: :py:exc:`TypeError`,
             :py:exc:`errors.exceptions.APIMethodError`,
             :py:exc:`errors.exceptions.APIRequestError`,
             :py:exc:`errors.exceptions.APIResponseConversionError`,
             :py:exc:`errors.exceptions.InvalidFieldError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    # Define the API endpoint to call and other API details
    _endpoint = const.REST_PATHS.USER_STATUS.format(user_id=_user_id)

    # Identify the action to perform and define the payload accordingly
    if _action.lower() not in const.ARGUMENT_VALUES.VALID_USER_STATUS_ACTIONS:
        _error_msg = f"'{_action}' is not a valid action value when enabling or disabling a user. "
        _error_msg += f"(Expected: '{const.ARGUMENT_VALUES.ENABLE}', '{const.ARGUMENT_VALUES.DISABLE}')"
        logger.error(_error_msg)
        raise errors.exceptions.InvalidPayloadValueError(_error_msg)
    if _action.lower() == const.ARGUMENT_VALUES.ENABLE:
        _action = const.PAYLOAD_VALUES.ENABLED
    else:
        _action = const.PAYLOAD_VALUES.DISABLED
    _payload = {
        const.QUERY_PARAMS.USER_STATUS: _action,
    }

    # Perform the API call and return the response
    return api.put(pydp_object=_pydp_object, endpoint=_endpoint, payload=_payload, api_type=const.ADMIN_API_TYPE,
                   timeout=_timeout, show_full_error=_show_full_error, return_json=_return_json,
                   allow_failed_response=_allow_failed_response)


def enable_user(
        pydp_object,
        user_id: str,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Enable a user that is currently disabled.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
    :type user_id: str
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
             :py:exc:`errors.exceptions.InvalidFieldError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    return _update_user_status(_pydp_object=pydp_object, _user_id=user_id, _action=const.ARGUMENT_VALUES.ENABLE,
                               _timeout=timeout, _show_full_error=show_full_error, _return_json=return_json,
                               _allow_failed_response=allow_failed_response)


def disable_user(
        pydp_object,
        user_id: str,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Disable a user that is currently enabled.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
    :type user_id: str
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
             :py:exc:`errors.exceptions.InvalidFieldError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    return _update_user_status(_pydp_object=pydp_object, _user_id=user_id, _action=const.ARGUMENT_VALUES.DISABLE,
                               _timeout=timeout, _show_full_error=show_full_error, _return_json=return_json,
                               _allow_failed_response=allow_failed_response)


def synchronize_user(
        pydp_object,
        user_id: str,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Synchronize the details of a user between an identity source and the Cloud Access Service.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
    :type user_id: str
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
             :py:exc:`errors.exceptions.InvalidFieldError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    # Define the API endpoint to call and other API details
    endpoint = const.REST_PATHS.USER_SYNC.format(user_id=user_id)
    payload = ''
    # TODO: Test to see if Content-Length header must be explicitly defined

    # Perform the API call and return the response
    return api.post(pydp_object=pydp_object, endpoint=endpoint, payload=payload, api_type=const.ADMIN_API_TYPE,
                    timeout=timeout, show_full_error=show_full_error, return_json=return_json,
                    allow_failed_response=allow_failed_response)


def _update_mark_deleted(
        _pydp_object,
        _user_id: str,
        _mark_deleted: bool,
        _timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        _show_full_error: bool = True,
        _return_json: bool = True,
        _allow_failed_response: Optional[bool] = None,
):
    """Mark (or unmark) a specific user as deleted."""
    # Define the API endpoint to call and other API details
    _endpoint: str = const.REST_PATHS.USER_MARK_DELETED.format(user_id=_user_id)
    _payload: dict[str, bool] = {const.QUERY_PARAMS.MARK_DELETED: _mark_deleted}
    
    # Perform the API call and return the response
    return api.put(pydp_object=_pydp_object, endpoint=_endpoint, payload=_payload, api_type=const.ADMIN_API_TYPE,
                   timeout=_timeout, show_full_error=_show_full_error, return_json=_return_json,
                   allow_failed_response=_allow_failed_response)


def mark_deleted(
        pydp_object,
        user_id: str,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Mark a specific user to be deleted during the next automated bulk deletion process.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
    :type user_id: str
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
             :py:exc:`errors.exceptions.InvalidFieldError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    return _update_mark_deleted(pydp_object, _user_id=user_id, _mark_deleted=True, _timeout=timeout,
                                _show_full_error=show_full_error, _return_json=return_json,
                                _allow_failed_response=allow_failed_response)


def unmark_deleted(
        pydp_object,
        user_id: str,
        timeout: int = const.DEFAULT_API_TIMEOUT_SECONDS,
        show_full_error: bool = True,
        return_json: bool = True,
        allow_failed_response: Optional[bool] = None,
):
    """Unmark a specific user that was flagged to be deleted.

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
    :type user_id: str
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
             :py:exc:`errors.exceptions.InvalidFieldError`,
             :py:exc:`errors.exceptions.MissingRequiredDataError`
    """
    return _update_mark_deleted(pydp_object, _user_id=user_id, _mark_deleted=False, _timeout=timeout,
                                _show_full_error=show_full_error, _return_json=return_json,
                                _allow_failed_response=allow_failed_response)


# def _add_remove_high_risk_users(_pydp_object, _users_list, _action, _timeout=const.DEFAULT_API_TIMEOUT_SECONDS,
#                                 _show_full_error=True, _return_json=True, _allow_failed_response=None):
#     # TODO: Finish the function
#     pass
