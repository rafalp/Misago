from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.cache.versions import get_cache_versions
from misago.conf.dynamicsettings import DynamicSettings
from misago.conf.test import override_dynamic_settings

from misago.users.setupnewuser import (
    set_default_subscription_options, setup_new_user
)

User = get_user_model()


class NewUserSetupTests(TestCase):
    def test_default_avatar_is_set_for_user(self):
        user = User.objects.create_user("User", "test@example.com")
        cache_versions = get_cache_versions()
        settings = DynamicSettings(cache_versions)
        setup_new_user(settings, user)
        assert user.avatars
        assert user.avatar_set.exists()

    def test_default_started_threads_subscription_option_is_set_for_user(self):
        user = User.objects.create_user("User", "test@example.com")
        cache_versions = get_cache_versions()
        settings = DynamicSettings(cache_versions)

        with override_dynamic_settings(subscribe_start="no"):
            set_default_subscription_options(settings, user)
            assert user.subscribe_to_started_threads == User.SUBSCRIPTION_NONE

        with override_dynamic_settings(subscribe_start="watch"):
            set_default_subscription_options(settings, user)
            assert user.subscribe_to_started_threads == User.SUBSCRIPTION_NOTIFY

        with override_dynamic_settings(subscribe_start="watch_email"):
            set_default_subscription_options(settings, user)
            assert user.subscribe_to_started_threads == User.SUBSCRIPTION_ALL

    def test_default_replied_threads_subscription_option_is_set_for_user(self):
        user = User.objects.create_user("User", "test@example.com")
        cache_versions = get_cache_versions()
        settings = DynamicSettings(cache_versions)

        with override_dynamic_settings(subscribe_reply="no"):
            set_default_subscription_options(settings, user)
            assert user.subscribe_to_replied_threads == User.SUBSCRIPTION_NONE

        with override_dynamic_settings(subscribe_reply="watch"):
            set_default_subscription_options(settings, user)
            assert user.subscribe_to_replied_threads == User.SUBSCRIPTION_NOTIFY

        with override_dynamic_settings(subscribe_reply="watch_email"):
            set_default_subscription_options(settings, user)
            assert user.subscribe_to_replied_threads == User.SUBSCRIPTION_ALL

    def test_if_user_ip_is_available_audit_trail_is_created_for_user(self):
        user = User.objects.create_user("User", "test@example.com", joined_from_ip="0.0.0.0")
        cache_versions = get_cache_versions()
        settings = DynamicSettings(cache_versions)
        setup_new_user(settings, user)
        assert user.audittrail_set.count() == 1

    def test_if_user_ip_is_not_available_audit_trail_is_not_created(self):
        user = User.objects.create_user("User", "test@example.com")
        cache_versions = get_cache_versions()
        settings = DynamicSettings(cache_versions)
        setup_new_user(settings, user)
        assert user.audittrail_set.exists() is False