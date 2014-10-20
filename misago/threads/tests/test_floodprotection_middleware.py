from datetime import timedelta

from django.utils import timezone

from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.posting import PostingInterrupt
from misago.threads.posting.floodprotection import (MIN_POSTING_PAUSE,
                                                    FloodProtectionMiddleware)


class FloodProtectionMiddlewareTests(AuthenticatedUserTestCase):
    def test_flood_protection_middleware_on_no_posts(self):
        """middleware sets last_post on user"""
        self.user.update_fields = []
        self.assertIsNone(self.user.last_post)

        middleware = FloodProtectionMiddleware(user=self.user)
        middleware.save(None)

        self.assertIsNotNone(self.user.last_post)

    def test_flood_protection_middleware_old_posts(self):
        """middleware is not complaining about old post"""
        self.user.update_fields = []

        original_last_post = timezone.now() - timedelta(days=1)
        self.user.last_post = original_last_post

        middleware = FloodProtectionMiddleware(user=self.user)
        middleware.save(None)

        self.assertTrue(self.user.last_post > original_last_post)

    def test_flood_protection_middleware_on_flood(self):
        """middleware is complaining about flood"""
        original_last_post = timezone.now() - timedelta(days=1)
        self.user.last_post = timezone.now()

        with self.assertRaises(PostingInterrupt):
            middleware = FloodProtectionMiddleware(user=self.user)
            middleware.save(None)
