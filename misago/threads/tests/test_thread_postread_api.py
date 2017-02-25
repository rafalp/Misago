from django.urls import reverse
from django.utils import timezone

from misago.threads import testutils

from .test_threads_api import ThreadsApiTestCase


class PostReadApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(PostReadApiTests, self).setUp()

        self.post = testutils.reply_thread(
            self.thread,
            poster=self.user,
            posted_on=timezone.now(),
        )

        self.api_link = reverse(
            'misago:api:thread-post-read',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.post.pk,
            }
        )

    def test_read_anonymous(self):
        """api validates if reading user is authenticated"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertContains(response, "This action is not available to guests.", status_code=403)

    def test_read_post(self):
        """api marks post as read"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 200)

        thread_read = self.user.threadread_set.order_by('id').last()
        self.assertEqual(thread_read.thread_id, self.thread.id)
        self.assertEqual(thread_read.last_read_on, self.post.posted_on)

        category_read = self.user.categoryread_set.order_by('id').last()
        self.assertTrue(category_read.last_read_on >= self.post.posted_on)

    def test_read_subscribed_thread_post(self):
        """api marks post as read and updates subscription"""
        self.thread.subscription_set.create(
            user=self.user,
            thread=self.thread,
            category=self.thread.category,
            last_read_on=self.thread.post_set.order_by('id').first().posted_on,
        )

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 200)

        thread_read = self.user.threadread_set.order_by('id').last()
        self.assertEqual(thread_read.thread_id, self.thread.id)
        self.assertEqual(thread_read.last_read_on, self.post.posted_on)

        category_read = self.user.categoryread_set.order_by('id').last()
        self.assertTrue(category_read.last_read_on >= self.post.posted_on)

        subscription = self.thread.subscription_set.order_by('id').last()
        self.assertEqual(subscription.last_read_on, self.post.posted_on)
