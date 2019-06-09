import json
from unittest.mock import Mock

import pytest
from django.forms import ValidationError
from requests.exceptions import Timeout

from ...conf.test import override_dynamic_settings
from ..validators import validate_with_sfs

cleaned_data = {"email": "test@test.com"}


@pytest.fixture
def request_mock(dynamic_settings):
    return Mock(settings=dynamic_settings, user_ip="127.0.0.1")


@pytest.fixture
def api_mock(mocker):
    return mocker.patch(
        "misago.users.validators.requests",
        get=Mock(
            return_value=Mock(
                content=json.dumps(
                    {"email": {"confidence": 55}, "ip": {"confidence": 45}}
                )
            )
        ),
    )


@override_dynamic_settings(enable_stop_forum_spam=False)
def test_api_is_not_called_if_sfs_is_disabled(api_mock, request_mock):
    validate_with_sfs(request_mock, cleaned_data, None)
    api_mock.get.assert_not_called()


@override_dynamic_settings(enable_stop_forum_spam=True)
def test_api_is_not_called_if_email_is_not_available(api_mock, request_mock):
    validate_with_sfs(request_mock, {}, None)
    api_mock.get.assert_not_called()


@override_dynamic_settings(enable_stop_forum_spam=True, stop_forum_spam_confidence=90)
def test_api_is_called_if_sfs_is_enabled_and_email_is_provided(api_mock, request_mock):
    validate_with_sfs(request_mock, cleaned_data, None)
    api_mock.get.assert_called_once()


@override_dynamic_settings(enable_stop_forum_spam=True, stop_forum_spam_confidence=50)
def test_validator_raises_error_if_ip_score_is_greater_than_confidence(
    api_mock, request_mock
):
    with pytest.raises(ValidationError):
        validate_with_sfs(request_mock, cleaned_data, None)


@override_dynamic_settings(enable_stop_forum_spam=True, stop_forum_spam_confidence=52)
def test_validator_raises_error_if_email_score_is_greater_than_confidence(
    api_mock, request_mock
):
    with pytest.raises(ValidationError):
        validate_with_sfs(request_mock, cleaned_data, None)


@override_dynamic_settings(enable_stop_forum_spam=True)
def test_validator_handles_api_error(mocker, request_mock):
    failing_api_mock = mocker.patch(
        "misago.users.validators.requests",
        get=Mock(return_value=Mock(raise_for_status=Mock(side_effect=Timeout()))),
    )

    validate_with_sfs(request_mock, cleaned_data, None)
    failing_api_mock.get.assert_called_once()


@override_dynamic_settings(enable_stop_forum_spam=True)
def test_validator_logs_api_error(mocker, request_mock):
    failing_api_mock = mocker.patch(
        "misago.users.validators.requests",
        get=Mock(return_value=Mock(raise_for_status=Mock(side_effect=Timeout()))),
    )
    logger_mock = mocker.patch("misago.users.validators.logger", exception=Mock())

    validate_with_sfs(request_mock, cleaned_data, None)
    failing_api_mock.get.assert_called_once()
    logger_mock.exception.assert_called_once()


@override_dynamic_settings(enable_stop_forum_spam=True)
def test_validator_handles_malformed_api_response(mocker, request_mock):
    failing_api_mock = mocker.patch(
        "misago.users.validators.requests", get=Mock(return_value=Mock(content="{}"))
    )

    validate_with_sfs(request_mock, cleaned_data, None)
    failing_api_mock.get.assert_called_once()
