from django.test import TestCase

from misago.conf import CACHE_NAME
from misago.conf.tests import OverrideDatabaseSettings
from misago.conf.databasesettings import DatabaseSettings


class OverrideDatabaseSettingsTests(TestCase):
    def test_as_context_manager(self):
        settings = DatabaseSettings({CACHE_NAME: "abcdefgh"})
        assert settings.forum_name == "Misago"

        with OverrideDatabaseSettings(forum_name="Overrided"):
            assert settings.forum_name == "Overrided"

        assert settings.forum_name == "Misago"
