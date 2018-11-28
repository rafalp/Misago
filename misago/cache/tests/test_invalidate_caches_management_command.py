from unittest.mock import Mock, patch

from django.core.management import call_command
from django.test import TestCase


class InvalidateCachesManagementCommandTests(TestCase):
    @patch("misago.cache.versions.invalidate_all_caches")
    def test_management_command_invalidates_all_caches(self, invalidate_all_caches):
        call_command('invalidateversionedcaches', stdout=Mock())
        invalidate_all_caches.assert_called_once()
