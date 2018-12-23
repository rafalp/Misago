from django.urls import reverse
from django.utils import timezone

from .. import test
from .test_threads_api import ThreadsApiTestCase


class PostReadApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.post = test.reply_thread(
            self.thread, poster=self.user, posted_on=timezone.now()
        )

        self.api_link = reverse(
            "misago:api:thread-post-read",
            kwargs={"thread_pk": self.thread.pk, "pk": self.post.pk},
        )

    def test_read_anonymous(self):
        """api validates if reading user is authenticated"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    def test_read_post(self):
        """api marks post as read"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.postread_set.count(), 1)
        self.user.postread_set.get(post=self.post)

        # one post read, first post is still unread
        self.assertFalse(response.json()["thread_is_read"])

        # read second post
        response = self.client.post(
            reverse(
                "misago:api:thread-post-read",
                kwargs={"thread_pk": self.thread.pk, "pk": self.thread.first_post.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.postread_set.count(), 2)
        self.user.postread_set.get(post=self.thread.first_post)

        # both posts are read
        self.assertTrue(response.json()["thread_is_read"])

    def test_read_subscribed_thread_post(self):
        """api marks post as read and updates subscription"""
        self.thread.subscription_set.create(
            user=self.user,
            thread=self.thread,
            category=self.thread.category,
            last_read_on=self.thread.post_set.order_by("id").first().posted_on,
        )

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 200)

        subscription = self.thread.subscription_set.order_by("id").last()
        self.assertEqual(subscription.last_read_on, self.post.posted_on)
