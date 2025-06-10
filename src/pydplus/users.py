# -*- coding: utf-8 -*-
"""
:Module:            pydplus.users
:Synopsis:          Defines the user-related functions associated with the RSA ID Plus API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Jun 2025
"""

from . import api, errors
from .utils import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def get_user_details(pydp_object, email, search_unsynced=None, timeout=api.DEFAULT_TIMEOUT, show_full_error=True,
                     return_json=True, allow_failed_response=False):
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
                                  (``False`` by default)
    :type allow_failed_response: bool
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
