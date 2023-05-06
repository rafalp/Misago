from unittest.mock import patch

from django.urls import reverse

from .. import test
from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase


class FloodProtectionTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category=self.category)

        self.post_link = reverse(
            "misago:api:thread-post-list", kwargs={"thread_pk": self.thread.pk}
        )

    @patch(
        "misago.threads.api.postingendpoint.notifications.notify_on_new_thread_reply"
    )
    def test_flood_has_no_showstoppers(self, notify_on_new_thread_reply_mock):
        """endpoint handles posting interruption"""
        response = self.client.post(
            self.post_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.post_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't post message so quickly after previous one."},
        )

    @patch_user_acl({"can_omit_flood_protection": True})
    @patch(
        "misago.threads.api.postingendpoint.notifications.notify_on_new_thread_reply"
    )
    def test_user_with_permission_omits_flood_protection(
        self, notify_on_new_thread_reply_mock
    ):
        response = self.client.post(
            self.post_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.post_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)
