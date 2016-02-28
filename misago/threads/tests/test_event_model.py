from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.categories.models import Category

from misago.threads.checksums import is_event_valid, update_event_checksum
from misago.threads.models import Thread, Event


class EventModelTests(TestCase):
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

    def test_is_event_valid(self):
        """event is_valid flag returns valid value"""
        event = Event.objects.create(
            category=self.category,
            thread=self.thread,
            author=self.user,
            message="Lorem ipsum",
            author_name=self.user.username,
            author_slug=self.user.slug
        )

        update_event_checksum(event)

        self.assertTrue(is_event_valid(event))
        self.assertTrue(event.is_valid)

        event.message = "Ipsum lorem"

        self.assertFalse(is_event_valid(event))
        self.assertFalse(event.is_valid)
