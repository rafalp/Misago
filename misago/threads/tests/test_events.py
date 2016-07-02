#-*- coding: utf-8 -*-
import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.acl import add_acl
from misago.categories.models import Category

from misago.threads.events import record_event
from misago.threads.models import Thread, Post
from misago.threads.testutils import reply_thread


class MockRequest(object):
    def __init__(self, user):
        self.user = user
        self.user_ip = '123.14.15.222'


class EventsAPITests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("Bob", "bob@bob.com", "Pass.123")

        datetime = timezone.now()

        self.category = Category.objects.all_categories()[:1][0]
        self.thread = Thread(
            category=self.category,
            started_on=datetime,
            starter_name='Tester',
            starter_slug='tester',
            last_post_on=datetime,
            last_poster_name='Tester',
            last_poster_slug='tester'
        )

        self.thread.set_title("Test thread")
        self.thread.save()

        add_acl(self.user, self.category)
        add_acl(self.user, self.thread)

    def test_record_event_with_context(self):
        """record_event registers event with context in thread"""
        request = MockRequest(self.user)
        context = {'user': 'Lorem ipsum'}
        event = record_event(request, self.thread, 'announcement', context)

        event_post = self.thread.post_set.order_by('-id')[:1][0]
        self.assertTrue(self.thread.last_post, event_post)

        self.assertEqual(event.pk, event_post.pk)
        self.assertTrue(event_post.is_event)
        self.assertEqual(event_post.event_type, 'announcement')
        self.assertEqual(event_post.event_context, context)
        self.assertEqual(event_post.poster_id, request.user.pk)
        self.assertEqual(event_post.poster_ip, request.user_ip)

