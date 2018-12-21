from unittest.mock import Mock

from django.core.management import call_command


def test_management_command_invalidates_all_caches(mocker):
    invalidate_all_caches = mocker.patch("misago.cache.versions.invalidate_all_caches")
    call_command("invalidateversionedcaches", stdout=Mock())
    invalidate_all_caches.assert_called_once()
