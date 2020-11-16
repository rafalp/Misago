from datetime import timedelta

from django.core import mail
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_str

from ...conf.test import override_dynamic_settings
from .. import test
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase, create_test_user
from ..test import patch_category_acl, patch_other_user_category_acl


class EmailNotificationTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(
            category=self.category, started_on=timezone.now() - timedelta(seconds=5)
        )

        self.api_link = reverse(
            "misago:api:thread-post-list", kwargs={"thread_pk": self.thread.pk}
        )

        self.other_user = create_test_user("OtherUser", "otheruser@example.com")

    @patch_category_acl({"can_reply_threads": True})
    def test_no_subscriptions(self):
        """no emails are sent because noone subscibes to thread"""
        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    @patch_category_acl({"can_reply_threads": True})
    def test_poster_not_notified(self):
        """no emails are sent because only poster subscribes to thread"""
        self.user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    @patch_category_acl({"can_reply_threads": True})
    def test_other_user_no_email_subscription(self):
        """no emails are sent because subscriber has e-mails off"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=False,
        )

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    @patch_category_acl({"can_reply_threads": True})
    @patch_other_user_category_acl({"can_see": False})
    def test_other_user_no_permission(self):
        """no emails are sent because subscriber has no permission to read thread"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    @patch_category_acl({"can_reply_threads": True})
    def test_moderation_queue(self):
        """no emails are sent because new post is moderated"""
        self.category.require_replies_approval = True
        self.category.save()

        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    @patch_category_acl({"can_reply_threads": True})
    def test_other_user_not_read(self):
        """no emails are sent because subscriber didn't read previous post"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )

        test.reply_thread(self.thread, posted_on=timezone.now())

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    @override_dynamic_settings(forum_address="http://test.com/")
    @patch_category_acl({"can_reply_threads": True})
    def test_other_notified(self):
        """email is sent to subscriber"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)
        last_email = mail.outbox[-1]

        self.assertIn(self.user.username, last_email.subject)
        self.assertIn(self.thread.title, last_email.subject)

        message = smart_str(last_email.body)

        self.assertIn(self.user.username, message)
        self.assertIn(self.thread.title, message)
        self.assertIn(self.thread.get_absolute_url(), message)

        last_post = self.thread.post_set.order_by("id").last()
        self.assertIn(last_post.get_absolute_url(), message)

    @override_dynamic_settings(forum_address="http://test.com/")
    @patch_category_acl({"can_reply_threads": True})
    def test_other_notified_after_reading(self):
        """email is sent to subscriber that had sub updated by read api"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=self.thread.last_post_on,
            send_email=True,
        )

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)
        last_email = mail.outbox[-1]

        self.assertIn(self.user.username, last_email.subject)
        self.assertIn(self.thread.title, last_email.subject)

        message = smart_str(last_email.body)

        self.assertIn(self.user.username, message)
        self.assertIn(self.thread.title, message)
        self.assertIn(self.thread.get_absolute_url(), message)

        last_post = self.thread.post_set.order_by("id").last()
        self.assertIn(last_post.get_absolute_url(), message)
