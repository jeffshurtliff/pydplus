# -*- coding: utf-8 -*-
"""
:Module:            tests.unit.test_exceptions
:Synopsis:          Unit tests for pydplus custom exception classes
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-5.3-codex)
:Modified Date:     30 Mar 2026
"""

from __future__ import annotations

import pytest

from pydplus.errors import exceptions

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ('exception_cls', 'expected_message'),
    [
        (exceptions.CurrentlyUnsupportedError, 'This feature is currently unsupported at this time.'),
        (exceptions.DataMismatchError, 'A data mismatch was found with the data sources.'),
        (exceptions.FeatureNotConfiguredError, 'The feature is not configured.'),
        (exceptions.InvalidParameterError, 'The parameter that was provided is invalid.'),
        (exceptions.InvalidFieldError, 'The field that was provided is invalid.'),
        (exceptions.InvalidURLError, 'The provided URL is invalid'),
        (exceptions.MissingRequiredDataError, 'Missing one or more required parameters'),
        (exceptions.UnknownFileTypeError, 'The file type of the given file path cannot be identified.'),
        (
            exceptions.APIConnectionError,
            'The API query could not be completed due to connection aborts and/or timeouts.',
        ),
        (
            exceptions.APIMethodError,
            'A valid API call method (GET or POST or PATCH or PUT) must be defined.',
        ),
        (exceptions.APIRequestError, 'The API request did not return a successful response.'),
        (
            exceptions.APIResponseConversionError,
            'The API response failed to be converted to the specified data format.',
        ),
        (exceptions.DELETERequestError, 'The DELETE request did not return a successful response.'),
        (exceptions.GETRequestError, 'The GET request did not return a successful response.'),
        (exceptions.InvalidEndpointError, 'The supplied endpoint for the API is not recognized.'),
        (
            exceptions.InvalidLookupTypeError,
            "The supplied lookup type for the API is not recognized. (Examples of valid lookup types include 'id' and 'email')",
        ),
        (exceptions.InvalidPayloadValueError, 'An invalid payload value was provided.'),
        (
            exceptions.InvalidRequestTypeError,
            "The supplied request type for the API is not recognized. (Examples of valid request types include 'POST' and 'PUT')",
        ),
        (
            exceptions.LookupMismatchError,
            'The supplied lookup type for the API does not match the value that was provided.',
        ),
        (exceptions.NotFoundResponseError, 'The API query returned a 404 response.'),
        (exceptions.PATCHRequestError, 'The PATCH request did not return a successful response.'),
        (
            exceptions.PayloadMismatchError,
            'More than one payload was provided for the API call when only one is permitted.',
        ),
        (exceptions.POSTRequestError, 'The POST request did not return a successful response.'),
        (exceptions.PUTRequestError, 'The PUT request did not return a successful response.'),
        (
            exceptions.InvalidHelperFileTypeError,
            "The helper configuration file can only have the 'yml', 'yaml' or 'json' file type.",
        ),
        (
            exceptions.InvalidHelperArgumentsError,
            "The helper configuration file only accepts basic keyword arguments. (e.g. arg_name='arg_value')",
        ),
        (
            exceptions.HelperFunctionNotFoundError,
            'The function referenced in the helper configuration file could not be found.',
        ),
    ],
)
def test_default_exception_messages(exception_cls, expected_message: str) -> None:
    """Ensure each exception class provides its expected default message."""
    assert str(exception_cls()) == expected_message


def test_pydplus_error_is_exception_subclass() -> None:
    """Ensure the base custom error behaves like a normal Python exception."""
    error = exceptions.PyDPlusError('base')
    assert isinstance(error, Exception)
    assert str(error) == 'base'


@pytest.mark.parametrize(
    ('exception_cls', 'custom_message'),
    [
        (exceptions.APIConnectionError, 'network timeout'),
        (exceptions.APIMethodError, 'custom method error'),
        (exceptions.APIRequestError, 'custom api request error'),
        (exceptions.APIResponseConversionError, 'cannot decode'),
        (exceptions.InvalidEndpointError, 'invalid endpoint custom'),
        (exceptions.InvalidLookupTypeError, 'invalid lookup custom'),
        (exceptions.InvalidRequestTypeError, 'invalid request type custom'),
        (exceptions.LookupMismatchError, 'lookup mismatch custom'),
        (exceptions.NotFoundResponseError, 'not found custom'),
        (exceptions.InvalidHelperFileTypeError, 'invalid helper file type custom'),
        (exceptions.InvalidHelperArgumentsError, 'helper args custom'),
        (exceptions.HelperFunctionNotFoundError, 'helper function missing custom'),
    ],
)
def test_custom_message_passthrough_for_exception_classes(exception_cls, custom_message: str) -> None:
    """Ensure explicit positional messages are passed through unchanged."""
    assert str(exception_cls(custom_message)) == custom_message


def test_currently_unsupported_error_uses_argument_context() -> None:
    """Ensure contextual messages are built from the first positional argument."""
    assert str(exceptions.CurrentlyUnsupportedError('feature-flag')) == (
        "The 'feature-flag' feature is currently unsupported at this time."
    )


def test_currently_unsupported_error_uses_message_keyword() -> None:
    """Ensure message keyword bypasses custom formatting."""
    assert str(exceptions.CurrentlyUnsupportedError(message='forced message')) == 'forced message'


def test_data_mismatch_error_custom_messages_for_str_and_pair() -> None:
    """Ensure data mismatch errors support string and two-item collection inputs."""
    assert str(exceptions.DataMismatchError(data='tenant profile')) == (
        "A data mismatch was found with the 'tenant profile' data source."
    )
    assert str(exceptions.DataMismatchError(data=['api', 'database'])) == (
        "A data mismatch was found with the 'api' and 'database' data sources."
    )


def test_data_mismatch_error_with_unsupported_data_type_creates_empty_message() -> None:
    """Ensure unsupported data types preserve current behavior and do not set a default message."""
    assert str(exceptions.DataMismatchError(data=100)) == ''


def test_feature_not_configured_error_supports_feature_and_identifier() -> None:
    """Ensure feature and identifier values are both reflected in the generated message."""
    error = exceptions.FeatureNotConfiguredError(feature='MFA', identifier='abc123')
    assert str(error) == 'The MFA feature is not configured. Identifier: abc123'


def test_invalid_parameter_and_field_errors_support_val_keyword() -> None:
    """Ensure invalid parameter and field classes render val-specific details."""
    assert str(exceptions.InvalidParameterError(val='verify_ssl')) == ("The 'verify_ssl' parameter that was provided is invalid.")
    assert str(exceptions.InvalidFieldError(val='userStatus')) == "The 'userStatus' field that was provided is invalid."


def test_invalid_url_error_url_keyword_raises_index_error() -> None:
    """Ensure current URL keyword branch behavior is covered."""
    with pytest.raises(IndexError):
        exceptions.InvalidURLError(url='https://example.com')


def test_invalid_url_error_url_keyword_builds_message_when_url_constant_matches_case(monkeypatch) -> None:
    """Ensure URL-kwarg branch can build a message when constant casing aligns with split logic."""
    monkeypatch.setattr(type(exceptions._EXCEPTION_CLASSES), '_URL', 'URL')
    assert str(exceptions.InvalidURLError(**{'URL': 'https://example.com'})) == (
        "The provided URL 'https://example.com' is invalid"
    )


def test_missing_required_data_error_covers_init_and_param_paths() -> None:
    """Ensure init and param-specific message branches are exercised."""
    assert str(exceptions.MissingRequiredDataError('init', object='PyDPlus')) == (
        "The 'PyDPlus' object failed to initialize as it is missing one or more required arguments."
    )
    assert str(exceptions.MissingRequiredDataError('initialize')) == (
        'The object failed to initialize as it is missing one or more required arguments.'
    )
    assert str(exceptions.MissingRequiredDataError(param='base_url')) == ("The required parameter 'base_url' is not defined")


def test_unknown_file_type_error_supports_file_keyword() -> None:
    """Ensure unknown-file-type errors can include the problematic file path."""
    assert str(exceptions.UnknownFileTypeError(file='/tmp/config.bin')) == (
        "The file type of the given file '/tmp/config.bin' cannot be identified."
    )


@pytest.mark.parametrize(
    ('exception_cls', 'request_type'),
    [
        (exceptions.DELETERequestError, 'DELETE'),
        (exceptions.GETRequestError, 'GET'),
        (exceptions.PATCHRequestError, 'PATCH'),
        (exceptions.POSTRequestError, 'POST'),
        (exceptions.PUTRequestError, 'PUT'),
    ],
)
def test_api_request_exception_classes_support_custom_status_and_message(exception_cls, request_type: str) -> None:
    """Ensure HTTP-method-specific exceptions can include status code and response details."""
    error = exception_cls(status_code=404, message='Not Found')
    assert str(error) == f'The {request_type} request returned the 404 status code with the following message: Not Found'


def test_invalid_payload_value_error_covers_all_value_paths() -> None:
    """Ensure payload value errors support field-aware and value-only custom messages."""
    with_field = exceptions.InvalidPayloadValueError(value='Disabled', field='userStatus')
    without_field = exceptions.InvalidPayloadValueError(value='Disabled')

    assert str(with_field) == "The invalid payload value 'Disabled' was provided for the 'userStatus' field."
    assert str(without_field) == "The invalid payload value 'Disabled' was provided."


def test_payload_mismatch_error_supports_request_type_and_invalid_keyword_behavior() -> None:
    """Ensure payload mismatch message customization is covered."""
    assert str(exceptions.PayloadMismatchError(request_type='post')) == (
        'More than one payload was provided for the POST request when only one is permitted.'
    )

    with pytest.raises(KeyError):
        exceptions.PayloadMismatchError(other='value')


def test_value_error_mixin_exception_classes_are_instances_of_value_error() -> None:
    """Ensure ValueError mixin exceptions preserve ValueError inheritance."""
    assert isinstance(exceptions.APIMethodError(), ValueError)
    assert isinstance(exceptions.InvalidLookupTypeError(), ValueError)
    assert isinstance(exceptions.InvalidRequestTypeError(), ValueError)
    assert isinstance(exceptions.InvalidHelperFileTypeError(), ValueError)


def test_construct_api_custom_message_helper_covers_all_paths() -> None:
    """Ensure custom API message helper handles all status/message combinations."""
    assert exceptions._construct_api_custom_message('get') == ('The GET request did not return a successful response.')
    assert exceptions._construct_api_custom_message('get', _message='bad request') == (
        'The GET request failed with the following message: bad request'
    )
    assert exceptions._construct_api_custom_message('get', _status_code=401) == ('The GET request returned the 401 status code.')
    assert exceptions._construct_api_custom_message('get', _message='bad request', _status_code=401) == (
        'The GET request returned the 401 status code with the following message: bad request'
    )
