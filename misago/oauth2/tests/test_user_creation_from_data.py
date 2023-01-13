from unittest.mock import Mock

from django.contrib.auth import get_user_model

from ...conf.test import override_dynamic_settings
from ..models import Subject
from ..user import get_user_from_data

User = get_user_model()


def test_activated_user_is_created_from_valid_data(db, dynamic_settings):
    user, created = get_user_from_data(
        Mock(settings=dynamic_settings, user_ip="83.0.0.1"),
        {
            "id": "1234",
            "name": "NewUser",
            "email": "user@example.com",
            "avatar": None,
        },
    )

    assert created
    assert user.id
    assert user.username == "NewUser"
    assert user.slug == "newuser"
    assert user.email == "user@example.com"
    assert user.requires_activation == User.ACTIVATION_NONE

    user_by_name = User.objects.get_by_username("NewUser")
    assert user_by_name.id == user.id

    user_by_email = User.objects.get_by_email("user@example.com")
    assert user_by_email.id == user.id


def test_user_subject_is_created_from_valid_data(db, dynamic_settings):
    user, created = get_user_from_data(
        Mock(settings=dynamic_settings, user_ip="83.0.0.1"),
        {
            "id": "1234",
            "name": "NewUser",
            "email": "user@example.com",
            "avatar": None,
        },
    )

    assert created
    assert user

    user_subject = Subject.objects.get(sub="1234")
    assert user_subject.user_id == user.id


def test_user_is_created_with_avatar_from_valid_data(db, dynamic_settings):
    user, created = get_user_from_data(
        Mock(settings=dynamic_settings, user_ip="83.0.0.1"),
        {
            "id": "1234",
            "name": "NewUser",
            "email": "user@example.com",
            "avatar": "https://placekitten.com/600/500",
        },
    )

    assert created
    assert user
    assert user.avatars
    assert user.avatar_set.exists()


@override_dynamic_settings(account_activation="admin")
def test_user_is_created_with_admin_activation_from_valid_data(db, dynamic_settings):
    user, created = get_user_from_data(
        Mock(settings=dynamic_settings, user_ip="83.0.0.1"),
        {
            "id": "1234",
            "name": "NewUser",
            "email": "user@example.com",
            "avatar": None,
        },
    )

    assert created
    assert user
    assert user.requires_activation == User.ACTIVATION_ADMIN
