# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class SubscriptionMiddlewareTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(SubscriptionMiddlewareTestCase, self).setUp()
        self.category = Category.objects.get(slug='first-category')
        self.override_acl()

    def override_acl(self):
        new_acl = self.user.acl_cache
        new_acl['can_omit_flood_protection'] = True
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 1,
            'can_reply_threads': 1,
        })

        override_acl(self.user, new_acl)


class SubscribeStartedThreadTests(SubscriptionMiddlewareTestCase):
    def setUp(self):
        super(SubscribeStartedThreadTests, self).setUp()
        self.api_link = reverse('misago:api:thread-list')

    def test_dont_subscribe(self):
        """middleware makes no subscription to thread"""
        self.user.subscribe_to_started_threads = UserModel.SUBSCRIBE_NONE
        self.user.subscribe_to_replied_threads = UserModel.SUBSCRIBE_NOTIFY
        self.user.save()

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.id,
                'title': "This is an test thread!",
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        # user has no subscriptions
        self.assertEqual(self.user.subscription_set.count(), 0)

    def test_subscribe(self):
        """middleware subscribes thread"""
        self.user.subscribe_to_started_threads = UserModel.SUBSCRIBE_NOTIFY
        self.user.save()

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.id,
                'title': "This is an test thread!",
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        # user has subscribed to thread
        thread = self.user.thread_set.order_by('id').last()
        subscription = self.user.subscription_set.get(thread=thread)

        self.assertEqual(subscription.category_id, self.category.id)
        self.assertFalse(subscription.send_email)

    def test_email_subscribe(self):
        """middleware subscribes thread with an email"""
        self.user.subscribe_to_started_threads = UserModel.SUBSCRIBE_ALL
        self.user.save()

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.id,
                'title': "This is an test thread!",
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        # user has subscribed to thread
        thread = self.user.thread_set.order_by('id').last()
        subscription = self.user.subscription_set.get(thread=thread)

        self.assertEqual(subscription.category_id, self.category.id)
        self.assertTrue(subscription.send_email)


class SubscribeRepliedThreadTests(SubscriptionMiddlewareTestCase):
    def setUp(self):
        super(SubscribeRepliedThreadTests, self).setUp()
        self.thread = testutils.post_thread(self.category)
        self.api_link = reverse(
            'misago:api:thread-post-list', kwargs={
                'thread_pk': self.thread.pk,
            }
        )

    def test_dont_subscribe(self):
        """middleware makes no subscription to thread"""
        self.user.subscribe_to_started_threads = UserModel.SUBSCRIBE_NOTIFY
        self.user.subscribe_to_replied_threads = UserModel.SUBSCRIBE_NONE
        self.user.save()

        response = self.client.post(
            self.api_link, data={
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        # user has no subscriptions
        self.assertEqual(self.user.subscription_set.count(), 0)

    def test_subscribe(self):
        """middleware subscribes thread"""
        self.user.subscribe_to_replied_threads = UserModel.SUBSCRIBE_NOTIFY
        self.user.save()

        response = self.client.post(
            self.api_link, data={
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        # user has subscribed to thread
        subscription = self.user.subscription_set.get(thread=self.thread)

        self.assertEqual(subscription.category_id, self.category.id)
        self.assertFalse(subscription.send_email)

    def test_email_subscribe(self):
        """middleware subscribes thread with an email"""
        self.user.subscribe_to_replied_threads = UserModel.SUBSCRIBE_ALL
        self.user.save()

        response = self.client.post(
            self.api_link, data={
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        # user has subscribed to thread
        subscription = self.user.subscription_set.get(thread=self.thread)

        self.assertEqual(subscription.category_id, self.category.id)
        self.assertTrue(subscription.send_email)

    def test_dont_subscribe_replied(self):
        """middleware omits threads user already replied"""
        self.user.subscribe_to_replied_threads = UserModel.SUBSCRIBE_ALL
        self.user.save()

        response = self.client.post(
            self.api_link, data={
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        # clear subscription
        self.user.subscription_set.all().delete()
        # reply again
        response = self.client.post(
            self.api_link, data={
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        # user has no subscriptions
        self.assertEqual(self.user.subscription_set.count(), 0)
