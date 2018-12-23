import json

from django.urls import reverse

from .. import test
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase


class ThreadPollApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(self.category, poster=self.user)

        self.api_link = reverse(
            "misago:api:thread-poll-list", kwargs={"thread_pk": self.thread.pk}
        )

    def post(self, url, data=None):
        return self.client.post(
            url, json.dumps(data or {}), content_type="application/json"
        )

    def put(self, url, data=None):
        return self.client.put(
            url, json.dumps(data or {}), content_type="application/json"
        )

    def mock_poll(self):
        self.poll = self.thread.poll = test.post_poll(self.thread, self.user)

        self.api_link = reverse(
            "misago:api:thread-poll-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": self.poll.pk},
        )
