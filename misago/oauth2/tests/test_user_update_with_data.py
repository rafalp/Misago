from unittest.mock import Mock

import pytest
from django.contrib.auth import get_user_model

from ..exceptions import OAuth2UserDataValidationError
from ..models import Subject
from ..user import get_user_from_data

User = get_user_model()


def test_user_is_updated_with_valid_data(user, dynamic_settings):
    Subject.objects.create(sub="1234", user=user)

    updated_user, created = get_user_from_data(
        Mock(settings=dynamic_settings, user_ip="83.0.0.1"),
        {
            "id": "1234",
            "name": "UpdatedName",
            "email": "updated@example.com",
            "avatar": None,
        },
        {},
    )

    assert created is False
    assert updated_user.id
    assert updated_user.id == user.id
    assert updated_user.username == "UpdatedName"
    assert updated_user.username != user.username
    assert updated_user.slug == "updatedname"
    assert updated_user.slug != user.slug
    assert updated_user.email == "updated@example.com"
    assert updated_user.email != user.email

    user_by_name = User.objects.get_by_username("UpdatedName")
    assert user_by_name.id == user.id

    user_by_email = User.objects.get_by_email("updated@example.com")
    assert user_by_email.id == user.id


def test_user_is_not_updated_with_unchanged_valid_data(user, dynamic_settings):
    Subject.objects.create(sub="1234", user=user)

    updated_user, created = get_user_from_data(
        Mock(settings=dynamic_settings, user_ip="83.0.0.1"),
        {
            "id": "1234",
            "name": user.username,
            "email": user.email,
            "avatar": None,
        },
        {},
    )

    assert created is False
    assert updated_user.id
    assert updated_user.id == user.id
    assert updated_user.username == "User"
    assert updated_user.username == user.username
    assert updated_user.slug == "user"
    assert updated_user.slug == user.slug
    assert updated_user.email == "user@example.com"
    assert updated_user.email == user.email

    user_by_name = User.objects.get_by_username("User")
    assert user_by_name.id == user.id

    user_by_email = User.objects.get_by_email("user@example.com")
    assert user_by_email.id == user.id


def test_user_name_conflict_during_update_with_valid_data_is_handled(
    user, other_user, dynamic_settings, disable_user_data_filters
):
    Subject.objects.create(sub="1234", user=user)

    with pytest.raises(OAuth2UserDataValidationError) as excinfo:
        get_user_from_data(
            Mock(settings=dynamic_settings, user_ip="83.0.0.1"),
            {
                "id": "1234",
                "name": other_user.username,
                "email": "test@example.com",
                "avatar": None,
            },
            {},
        )

    assert excinfo.value.error_list == [
        "Your username returned by the provider is not available "
        "for use on this site."
    ]


def test_user_email_conflict_during_update_with_valid_data_is_handled(
    user, other_user, dynamic_settings
):
    Subject.objects.create(sub="1234", user=user)

    with pytest.raises(OAuth2UserDataValidationError) as excinfo:
        get_user_from_data(
            Mock(settings=dynamic_settings, user_ip="83.0.0.1"),
            {
                "id": "1234",
                "name": "NewUser",
                "email": other_user.email,
                "avatar": None,
            },
            {},
        )

    assert excinfo.value.error_list == [
        "Your e-mail address returned by the provider is not available "
        "for use on this site."
    ]
