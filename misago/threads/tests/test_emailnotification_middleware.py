# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_str

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class EmailNotificationTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(EmailNotificationTests, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(
            category=self.category,
            started_on=timezone.now() - timedelta(seconds=5),
        )
        self.override_acl()

        self.api_link = reverse(
            'misago:api:thread-post-list', kwargs={
                'thread_pk': self.thread.pk,
            }
        )

        self.other_user = UserModel.objects.create_user('Bob', 'bob@boberson.com', 'pass123')

    def override_acl(self):
        new_acl = deepcopy(self.user.acl_cache)
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 1,
            'can_reply_threads': 1,
            'can_edit_posts': 1,
        })

        override_acl(self.user, new_acl)

    def override_other_user_acl(self, hide=False):
        new_acl = deepcopy(self.other_user.acl_cache)
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 1,
            'can_reply_threads': 1,
            'can_edit_posts': 1,
        })

        if hide:
            new_acl['categories'][self.category.pk].update({
                'can_browse': False,
            })

        override_acl(self.other_user, new_acl)

    def test_no_subscriptions(self):
        """no emails are sent because noone subscibes to thread"""
        response = self.client.post(
            self.api_link, data={
                'post': 'This is test response!',
            }
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    def test_poster_not_notified(self):
        """no emails are sent because only poster subscribes to thread"""
        self.user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )

        response = self.client.post(
            self.api_link, data={
                'post': 'This is test response!',
            }
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    def test_other_user_no_email_subscription(self):
        """no emails are sent because subscriber has e-mails off"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=False,
        )

        response = self.client.post(
            self.api_link, data={
                'post': 'This is test response!',
            }
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    def test_other_user_no_permission(self):
        """no emails are sent because subscriber has no permission to read thread"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )
        self.override_other_user_acl(hide=True)

        response = self.client.post(
            self.api_link, data={
                'post': 'This is test response!',
            }
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    def test_other_user_not_read(self):
        """no emails are sent because subscriber didn't read previous post"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )
        self.override_other_user_acl()

        testutils.reply_thread(self.thread, posted_on=timezone.now())

        response = self.client.post(
            self.api_link, data={
                'post': 'This is test response!',
            }
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

    def test_other_notified(self):
        """email is sent to subscriber"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=timezone.now(),
            send_email=True,
        )
        self.override_other_user_acl()

        response = self.client.post(
            self.api_link, data={
                'post': 'This is test response!',
            }
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

        last_post = self.thread.post_set.order_by('id').last()
        self.assertIn(last_post.get_absolute_url(), message)

    def test_other_notified_after_reading(self):
        """email is sent to subscriber that had sub updated by read api"""
        self.other_user.subscription_set.create(
            thread=self.thread,
            category=self.category,
            last_read_on=self.thread.last_post_on,
            send_email=True,
        )
        self.override_other_user_acl()

        response = self.client.post(
            self.api_link, data={
                'post': 'This is test response!',
            }
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

        last_post = self.thread.post_set.order_by('id').last()
        self.assertIn(last_post.get_absolute_url(), message)
