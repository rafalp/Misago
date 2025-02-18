from django.contrib.auth import get_user_model

from ...conf.test import override_dynamic_settings
from ...notifications.threads import ThreadNotifications
from ..setupnewuser import setup_new_user

User = get_user_model()

AVATAR_URL = "https://dummyimage.com/600/500"


def user(db):
    return User.objects.create_user("User", "user@example.com")


def test_default_avatar_is_set_for_user(dynamic_settings, user):
    setup_new_user(dynamic_settings, user)
    assert user.avatars
    assert user.avatar_set.exists()


def test_avatar_from_url_is_set_for_user(dynamic_settings, user):
    setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
    assert user.avatars
    assert user.avatar_set.exists()


def test_default_watch_started_threads_option_is_set_for_user(dynamic_settings, user):
    with override_dynamic_settings(watch_started_threads=ThreadNotifications.NONE):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert user.watch_started_threads == ThreadNotifications.NONE

    with override_dynamic_settings(watch_started_threads=ThreadNotifications.SITE_ONLY):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert user.watch_started_threads == ThreadNotifications.SITE_ONLY

    with override_dynamic_settings(
        watch_started_threads=ThreadNotifications.SITE_AND_EMAIL
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert user.watch_started_threads == ThreadNotifications.SITE_AND_EMAIL


def test_default_watch_replied_threads_option_is_set_for_user(dynamic_settings, user):
    with override_dynamic_settings(watch_replied_threads=ThreadNotifications.NONE):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert user.watch_replied_threads == ThreadNotifications.NONE

    with override_dynamic_settings(watch_replied_threads=ThreadNotifications.SITE_ONLY):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert user.watch_replied_threads == ThreadNotifications.SITE_ONLY

    with override_dynamic_settings(
        watch_replied_threads=ThreadNotifications.SITE_AND_EMAIL
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert user.watch_replied_threads == ThreadNotifications.SITE_AND_EMAIL


def test_default_watch_new_private_threads_by_followed_option_is_set_for_user(
    dynamic_settings, user
):
    with override_dynamic_settings(
        watch_new_private_threads_by_followed=ThreadNotifications.NONE
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert user.watch_new_private_threads_by_followed == ThreadNotifications.NONE

    with override_dynamic_settings(
        watch_new_private_threads_by_followed=ThreadNotifications.SITE_ONLY
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert (
            user.watch_new_private_threads_by_followed == ThreadNotifications.SITE_ONLY
        )

    with override_dynamic_settings(
        watch_new_private_threads_by_followed=ThreadNotifications.SITE_AND_EMAIL
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert (
            user.watch_new_private_threads_by_followed
            == ThreadNotifications.SITE_AND_EMAIL
        )


def test_default_watch_new_private_threads_by_other_users_option_is_set_for_user(
    dynamic_settings, user
):
    with override_dynamic_settings(
        watch_new_private_threads_by_other_users=ThreadNotifications.NONE
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert user.watch_new_private_threads_by_other_users == ThreadNotifications.NONE

    with override_dynamic_settings(
        watch_new_private_threads_by_other_users=ThreadNotifications.SITE_ONLY
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert (
            user.watch_new_private_threads_by_other_users
            == ThreadNotifications.SITE_ONLY
        )

    with override_dynamic_settings(
        watch_new_private_threads_by_other_users=ThreadNotifications.SITE_AND_EMAIL
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert (
            user.watch_new_private_threads_by_other_users
            == ThreadNotifications.SITE_AND_EMAIL
        )


def test_default_notify_new_private_threads_by_followed_option_is_set_for_user(
    dynamic_settings, user
):
    with override_dynamic_settings(
        notify_new_private_threads_by_followed=ThreadNotifications.NONE
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert user.notify_new_private_threads_by_followed == ThreadNotifications.NONE

    with override_dynamic_settings(
        notify_new_private_threads_by_followed=ThreadNotifications.SITE_ONLY
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert (
            user.notify_new_private_threads_by_followed == ThreadNotifications.SITE_ONLY
        )

    with override_dynamic_settings(
        notify_new_private_threads_by_followed=ThreadNotifications.SITE_AND_EMAIL
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert (
            user.notify_new_private_threads_by_followed
            == ThreadNotifications.SITE_AND_EMAIL
        )


def test_default_notify_new_private_threads_by_other_users_option_is_set_for_user(
    dynamic_settings, user
):
    with override_dynamic_settings(
        notify_new_private_threads_by_other_users=ThreadNotifications.NONE
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert (
            user.notify_new_private_threads_by_other_users == ThreadNotifications.NONE
        )

    with override_dynamic_settings(
        notify_new_private_threads_by_other_users=ThreadNotifications.SITE_ONLY
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert (
            user.notify_new_private_threads_by_other_users
            == ThreadNotifications.SITE_ONLY
        )

    with override_dynamic_settings(
        notify_new_private_threads_by_other_users=ThreadNotifications.SITE_AND_EMAIL
    ):
        setup_new_user(dynamic_settings, user, avatar_url=AVATAR_URL)
        assert (
            user.notify_new_private_threads_by_other_users
            == ThreadNotifications.SITE_AND_EMAIL
        )


def test_if_user_ip_is_available_audit_trail_is_created_for_user(dynamic_settings):
    user = User.objects.create_user(
        "User", "user@example.com", joined_from_ip="0.0.0.0"
    )
    setup_new_user(dynamic_settings, user)
    assert user.audittrail_set.count() == 1


def test_if_user_ip_is_not_available_audit_trail_is_not_created(dynamic_settings, user):
    setup_new_user(dynamic_settings, user)
    assert user.audittrail_set.exists() is False
