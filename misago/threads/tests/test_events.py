#-*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.acl import add_acl
from misago.categories.models import Category

from misago.threads.events import record_event, add_events_to_posts
from misago.threads.models import Thread, Event
from misago.threads.testutils import reply_thread


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

    def test_record_event(self):
        """record_event registers event in thread"""
        message = "%(user)s has changed this thread to announcement."
        event = record_event(self.user, self.thread, "announcement", message, {
            'user': (u"Łob", self.user.get_absolute_url())
        })

        self.assertTrue(event.is_valid)
        self.assertTrue(event.message.endswith(message[8:]))
        self.assertTrue(self.thread.has_events)

    def test_add_events_to_posts(self):
        """add_events_to_posts makes posts event-aware"""
        message = "Test event was recorded."

        for p in xrange(2):
            reply_thread(self.thread, posted_on=timezone.now())
        event = record_event(self.user, self.thread, "check", message)
        for p in xrange(2):
            reply_thread(self.thread, posted_on=timezone.now())

        posts = [p for p in self.thread.post_set.all().order_by('id')]
        add_events_to_posts(self.user, self.thread, posts)

        for i, post in enumerate(posts):
            if i == 1:
                self.assertEqual(post.events[0].message, message)
            else:
                self.assertEqual(post.events, [])
