from django.contrib.auth import get_user_model
from django.urls import reverse

from .. import test
from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase
from ..test import patch_category_acl

User = get_user_model()


class SubscriptionMiddlewareTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.get(slug="first-category")


class SubscribeStartedThreadTests(SubscriptionMiddlewareTestCase):
    def setUp(self):
        super().setUp()
        self.api_link = reverse("misago:api:thread-list")

    @patch_category_acl({"can_start_threads": True})
    def test_dont_subscribe(self):
        """middleware makes no subscription to thread"""
        self.user.subscribe_to_started_threads = User.SUBSCRIPTION_NONE
        self.user.subscribe_to_replied_threads = User.SUBSCRIPTION_NOTIFY
        self.user.save()

        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.id,
                "title": "This is an test thread!",
                "post": "This is test response!",
            },
        )
        self.assertEqual(response.status_code, 200)

        # user has no subscriptions
        self.assertEqual(self.user.subscription_set.count(), 0)

    @patch_category_acl({"can_start_threads": True})
    def test_subscribe(self):
        """middleware subscribes thread"""
        self.user.subscribe_to_started_threads = User.SUBSCRIPTION_NOTIFY
        self.user.save()

        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.id,
                "title": "This is an test thread!",
                "post": "This is test response!",
            },
        )
        self.assertEqual(response.status_code, 200)

        # user has subscribed to thread
        thread = self.user.thread_set.order_by("id").last()
        subscription = self.user.subscription_set.get(thread=thread)

        self.assertEqual(subscription.category_id, self.category.id)
        self.assertFalse(subscription.send_email)

    @patch_category_acl({"can_start_threads": True})
    def test_email_subscribe(self):
        """middleware subscribes thread with an email"""
        self.user.subscribe_to_started_threads = User.SUBSCRIPTION_ALL
        self.user.save()

        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.id,
                "title": "This is an test thread!",
                "post": "This is test response!",
            },
        )
        self.assertEqual(response.status_code, 200)

        # user has subscribed to thread
        thread = self.user.thread_set.order_by("id").last()
        subscription = self.user.subscription_set.get(thread=thread)

        self.assertEqual(subscription.category_id, self.category.id)
        self.assertTrue(subscription.send_email)


class SubscribeRepliedThreadTests(SubscriptionMiddlewareTestCase):
    def setUp(self):
        super().setUp()
        self.thread = test.post_thread(self.category)
        self.api_link = reverse(
            "misago:api:thread-post-list", kwargs={"thread_pk": self.thread.pk}
        )

    @patch_category_acl({"can_reply_threads": True})
    def test_dont_subscribe(self):
        """middleware makes no subscription to thread"""
        self.user.subscribe_to_started_threads = User.SUBSCRIPTION_NOTIFY
        self.user.subscribe_to_replied_threads = User.SUBSCRIPTION_NONE
        self.user.save()

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        # user has no subscriptions
        self.assertEqual(self.user.subscription_set.count(), 0)

    @patch_category_acl({"can_reply_threads": True})
    def test_subscribe(self):
        """middleware subscribes thread"""
        self.user.subscribe_to_replied_threads = User.SUBSCRIPTION_NOTIFY
        self.user.save()

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        # user has subscribed to thread
        subscription = self.user.subscription_set.get(thread=self.thread)

        self.assertEqual(subscription.category_id, self.category.id)
        self.assertFalse(subscription.send_email)

    @patch_category_acl({"can_reply_threads": True})
    def test_email_subscribe(self):
        """middleware subscribes thread with an email"""
        self.user.subscribe_to_replied_threads = User.SUBSCRIPTION_ALL
        self.user.save()

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        # user has subscribed to thread
        subscription = self.user.subscription_set.get(thread=self.thread)

        self.assertEqual(subscription.category_id, self.category.id)
        self.assertTrue(subscription.send_email)

    @patch_category_acl({"can_reply_threads": True})
    def test_subscribe_with_events(self):
        """middleware omits events when testing for replied thread"""
        self.user.subscribe_to_replied_threads = User.SUBSCRIPTION_ALL
        self.user.save()

        # set event in thread
        test.reply_thread(self.thread, self.user, is_event=True)

        # reply thread
        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        # user has subscribed to thread
        subscription = self.user.subscription_set.get(thread=self.thread)

        self.assertEqual(subscription.category_id, self.category.id)
        self.assertTrue(subscription.send_email)

    @patch_category_acl({"can_reply_threads": True})
    @patch_user_acl({"can_omit_flood_protection": True})
    def test_dont_subscribe_replied(self):
        """middleware omits threads user already replied"""
        self.user.subscribe_to_replied_threads = User.SUBSCRIPTION_ALL
        self.user.save()

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        # clear subscription
        self.user.subscription_set.all().delete()

        # reply again
        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        # user has no subscriptions
        self.assertEqual(self.user.subscription_set.count(), 0)
