from django.contrib.auth import get_user_model

from ...conf.test import override_dynamic_settings
from ..setupnewuser import set_default_subscription_options, setup_new_user

User = get_user_model()


def user(db):
    return User.objects.create_user("User", "user@example.com")


def test_default_avatar_is_set_for_user(dynamic_settings, user):
    setup_new_user(dynamic_settings, user)
    assert user.avatars
    assert user.avatar_set.exists()


def test_default_started_threads_subscription_option_is_set_for_user(
    dynamic_settings, user
):
    with override_dynamic_settings(subscribe_start="no"):
        set_default_subscription_options(dynamic_settings, user)
        assert user.subscribe_to_started_threads == User.SUBSCRIPTION_NONE

    with override_dynamic_settings(subscribe_start="watch"):
        set_default_subscription_options(dynamic_settings, user)
        assert user.subscribe_to_started_threads == User.SUBSCRIPTION_NOTIFY

    with override_dynamic_settings(subscribe_start="watch_email"):
        set_default_subscription_options(dynamic_settings, user)
        assert user.subscribe_to_started_threads == User.SUBSCRIPTION_ALL


def test_default_replied_threads_subscription_option_is_set_for_user(
    dynamic_settings, user
):
    with override_dynamic_settings(subscribe_reply="no"):
        set_default_subscription_options(dynamic_settings, user)
        assert user.subscribe_to_replied_threads == User.SUBSCRIPTION_NONE

    with override_dynamic_settings(subscribe_reply="watch"):
        set_default_subscription_options(dynamic_settings, user)
        assert user.subscribe_to_replied_threads == User.SUBSCRIPTION_NOTIFY

    with override_dynamic_settings(subscribe_reply="watch_email"):
        set_default_subscription_options(dynamic_settings, user)
        assert user.subscribe_to_replied_threads == User.SUBSCRIPTION_ALL


def test_if_user_ip_is_available_audit_trail_is_created_for_user(dynamic_settings):
    user = User.objects.create_user(
        "User", "user@example.com", joined_from_ip="0.0.0.0"
    )
    setup_new_user(dynamic_settings, user)
    assert user.audittrail_set.count() == 1


def test_if_user_ip_is_not_available_audit_trail_is_not_created(dynamic_settings, user):
    setup_new_user(dynamic_settings, user)
    assert user.audittrail_set.exists() is False
