# -*- coding: utf-8 -*-
"""
:Module:            pydplus.users
:Synopsis:          Defines the user-related functions associated with the RSA ID Plus API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     16 Jun 2025
"""

from . import api, errors
from .utils import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def get_user_details(pydp_object, email, search_unsynced=None, timeout=api.DEFAULT_TIMEOUT, show_full_error=True,
                     return_json=True, allow_failed_response=None):
    """This function retrieves the details for a specific user based on their email address.

    .. versionadded:: 1.0.0

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param email: The email address of the user for whom to retrieve details
    :type email: str
    :param search_unsynced: Indicates if the user search should include unsynchronized users (optional)
    :type search_unsynced: bool, None
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
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
    # Define the API endpoint to call and other API details
    endpoint = 'v1/users/lookup'
    api_type = 'admin'

    # Define the payload
    payload = {
        'email': email,
    }
    if search_unsynced is not None:
        if not isinstance(search_unsynced, bool):
            raise TypeError('The value of the search_unsynced parameter must be Boolean.')
        # noinspection PyTypeChecker
        payload['searchUnsynched'] = search_unsynced

    # Perform the API call and return the response in JSON format
    return api.post(pydp_object=pydp_object, endpoint=endpoint, payload=payload, api_type=api_type, timeout=timeout,
                    show_full_error=show_full_error, return_json=return_json,
                    allow_failed_response=allow_failed_response)


def get_user_id(pydp_object, email=None, user_details=None, search_unsynced=None, timeout=api.DEFAULT_TIMEOUT,
                show_full_error=True):
    """This function retrieves the User ID associated with a specific user.

    .. versionadded:: 1.0.0

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param email: The email address of the user for whom to retrieve details
    :type email: str, None
    :param user_details: The user details data from the :py:func:`pydplus.users.get_user_details` function
    :type user_details: dict, None
    :param search_unsynced: Indicates if the user search should include unsynchronized users (optional)
    :type search_unsynced: bool, None
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
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
    if not isinstance(user_details, dict) or 'id' not in user_details:
        error_msg = 'Failed to retrieve the user ID for the queried user. An empty string will be returned for the ID.'
        logger.error(error_msg)
    return user_details.get('id', '')


def _update_user_status(_pydp_object, _user_id, _action, _timeout=api.DEFAULT_TIMEOUT, _show_full_error=True,
                        _return_json=True, _allow_failed_response=None):
    """This function enables or disables a user by calling the User Status API.

    .. versionadded:: 1.0.0
    """
    # Define the API endpoint to call and other API details
    _endpoint = f'v1/users/{_user_id}/userStatus'
    _api_type = 'admin'

    # Identify the action to perform and define the payload accordingly
    _valid_actions = {'enable', 'disable'}
    if _action.lower() not in _valid_actions:
        error_msg = f"'{_action}' is not a valid action value when enabling or disabling a user."
        logger.error(error_msg)
        raise errors.exceptions.InvalidPayloadValueError(error_msg)
    _action = 'Enabled' if _action.lower() == 'enable' else 'Disabled'
    _payload = {
        'userStatus': _action,
    }

    # Perform the API call and return the response
    return api.put(pydp_object=_pydp_object, endpoint=_endpoint, payload=_payload, timeout=_timeout,
                   show_full_error=_show_full_error, return_json=_return_json,
                   allow_failed_response=_allow_failed_response)


def enable_user(pydp_object, user_id, timeout=api.DEFAULT_TIMEOUT, show_full_error=True, return_json=True,
                allow_failed_response=None):
    """This function enables a user that is currently disabled.

    .. versionadded:: 1.0.0

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
    :type user_id: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
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
    return _update_user_status(_pydp_object=pydp_object, _user_id=user_id, _action='enable', _timeout=timeout,
                               _show_full_error=show_full_error, _return_json=return_json,
                               _allow_failed_response=allow_failed_response)


def disable_user(pydp_object, user_id, timeout=api.DEFAULT_TIMEOUT, show_full_error=True, return_json=True,
                 allow_failed_response=None):
    """This function disables a user that is currently enabled.

    .. versionadded:: 1.0.0

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
    :type user_id: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
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
    return _update_user_status(_pydp_object=pydp_object, _user_id=user_id, _action='disable', _timeout=timeout,
                               _show_full_error=show_full_error, _return_json=return_json,
                               _allow_failed_response=allow_failed_response)


def synchronize_user(pydp_object, user_id, timeout=api.DEFAULT_TIMEOUT, show_full_error=True, return_json=True,
                     allow_failed_response=None):
    """This function synchronizes the details of a user between an identity source and the Cloud Access Service.

    .. versionadded:: 1.0.0

    :param pydp_object: The instantiated pydplus object
    :type pydp_object: class[pydplus.PyDPlus]
    :param user_id: The ID of an existing user (e.g. ``54082ac6-4713-6368-2251-df813c41159f``)
    :type user_id: str
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
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
    endpoint = f'v1/users/{user_id}/sync'
    api_type = 'admin'
    payload = ''
    # TODO: Test to see if Content-Length header must be explicitly defined

    # Perform the API call and return the response
    return api.post(pydp_object=pydp_object, endpoint=endpoint, payload=payload, api_type=api_type, timeout=timeout,
                    show_full_error=show_full_error, return_json=return_json,
                    allow_failed_response=allow_failed_response)


def _update_mark_deleted(_pydp_object, _user_id, _mark_deleted, _timeout=api.DEFAULT_TIMEOUT, _show_full_error=True, _return_json=True,
                    _allow_failed_response=None):
    # TODO: Add docstring for the function
    # Define the API endpoint to call and other API details
    _endpoint = 'v1/users/{user_id}/markDeleted'
    _api_type = 'admin'
    _payload = {'markDeleted': _mark_deleted}
    
    # Perform the API call and return the response
    return api.put(pydp_object=_pydp_object, endpoint=_endpoint, payload=_payload, api_type=_api_type, timeout=_timeout, show_full_error=_show_full_error, return_json=_return_json, allow_failed_response=_allow_failed_response)


def mark_deleted(pydp_object, user_id, timeout=api.DEFAULT_TIMEOUT, show_full_error=True, return_json=True, allow_failed_response=None):
    # TODO: Add docstring for the function
    return _update_mark_deleted(pydp_object, _user_id=user_id, _mark_deleted=True, _timeout=timeout, _show_full_error=show_full_error, _return_json=return_json, _allow_failed_response=allow_failed_response)


def mark_undeleted(pydp_object, user_id, timeout=api.DEFAULT_TIMEOUT, show_full_error=True, return_json=True, allow_failed_response=None):
    # TODO: Add docstring for the function
    return _update_mark_deleted(pydp_object, _user_id=user_id, _mark_deleted=False, _timeout=timeout, _show_full_error=show_full_error, _return_json=return_json, _allow_failed_response=allow_failed_response)

