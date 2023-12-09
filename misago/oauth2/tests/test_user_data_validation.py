from unittest.mock import Mock

import pytest

from ..exceptions import OAuth2UserDataValidationError
from ..validation import validate_user_data


def test_new_user_valid_data_is_validated(db, dynamic_settings):
    valid_data = validate_user_data(
        Mock(settings=dynamic_settings),
        None,
        {
            "id": "1234",
            "name": "Test User",
            "email": "user@example.com",
            "avatar": None,
        },
        {},
    )

    assert valid_data == {
        "id": "1234",
        "name": "Test_User",
        "email": "user@example.com",
        "avatar": None,
    }


def test_existing_user_valid_data_is_validated(user, dynamic_settings):
    valid_data = validate_user_data(
        Mock(settings=dynamic_settings),
        user,
        {
            "id": "1234",
            "name": user.username,
            "email": user.email,
            "avatar": None,
        },
        {},
    )

    assert valid_data == {
        "id": "1234",
        "name": user.username,
        "email": user.email,
        "avatar": None,
    }


def test_error_was_raised_for_user_data_with_without_name(
    db, dynamic_settings, disable_user_data_filters
):
    with pytest.raises(OAuth2UserDataValidationError) as excinfo:
        validate_user_data(
            Mock(settings=dynamic_settings),
            None,
            {
                "id": "1234",
                "name": "",
                "email": "user@example.com",
                "avatar": None,
            },
            {},
        )

    assert excinfo.value.error_list == [
        (
            "Username can only contain Latin alphabet letters, digits, "
            "and an underscore sign."
        )
    ]


def test_error_was_raised_for_user_data_with_invalid_name(
    db, dynamic_settings, disable_user_data_filters
):
    with pytest.raises(OAuth2UserDataValidationError) as excinfo:
        validate_user_data(
            Mock(settings=dynamic_settings),
            None,
            {
                "id": "1234",
                "name": "Invalid!",
                "email": "user@example.com",
                "avatar": None,
            },
            {},
        )

    assert excinfo.value.error_list == [
        (
            "Username can only contain Latin alphabet letters, digits, "
            "and an underscore sign."
        )
    ]


def test_error_was_raised_for_user_data_with_too_long_name(db, dynamic_settings):
    with pytest.raises(OAuth2UserDataValidationError) as excinfo:
        validate_user_data(
            Mock(settings=dynamic_settings),
            None,
            {
                "id": "1234",
                "name": "UserName" * 100,
                "email": "user@example.com",
                "avatar": None,
            },
            {},
        )

    assert excinfo.value.error_list == [
        "Username cannot be longer than 200 characters."
    ]


def test_error_was_raised_for_user_data_without_email(db, dynamic_settings):
    with pytest.raises(OAuth2UserDataValidationError) as excinfo:
        validate_user_data(
            Mock(settings=dynamic_settings),
            None,
            {
                "id": "1234",
                "name": "Test User",
                "email": "",
                "avatar": None,
            },
            {},
        )

    assert excinfo.value.error_list == ["Enter a valid e-mail address."]


def test_error_was_raised_for_user_data_with_invalid_email(db, dynamic_settings):
    with pytest.raises(OAuth2UserDataValidationError) as excinfo:
        validate_user_data(
            Mock(settings=dynamic_settings),
            None,
            {
                "id": "1234",
                "name": "Test User",
                "email": "userexample.com",
                "avatar": None,
            },
            {},
        )

    assert excinfo.value.error_list == ["Enter a valid e-mail address."]
