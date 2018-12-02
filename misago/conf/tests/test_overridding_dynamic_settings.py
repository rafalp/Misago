from django.test import TestCase

from misago.conf import CACHE_NAME
from misago.conf.tests import override_dynamic_settings
from misago.conf.dynamicsettings import DynamicSettings

cache_versions = {CACHE_NAME: "abcdefgh"}


class OverrideDynamicSettingsTests(TestCase):
    def test_setting_can_be_overridden_using_context_manager(self):
        settings = DynamicSettings(cache_versions)
        assert settings.forum_name == "Misago"

        with override_dynamic_settings(forum_name="Overrided"):
            assert settings.forum_name == "Overrided"

        assert settings.forum_name == "Misago"

    def test_setting_can_be_overridden_using_decorator(self):
        @override_dynamic_settings(forum_name="Overrided")
        def decorated_function(settings):
            return settings.forum_name

        settings = DynamicSettings(cache_versions)
        assert settings.forum_name == "Misago"
        assert decorated_function(settings) == "Overrided"
        assert settings.forum_name == "Misago"
