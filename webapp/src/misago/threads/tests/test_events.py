from unittest.mock import Mock

from django.test import TestCase
from django.utils import timezone

from ...acl import useracl
from ...acl.objectacl import add_acl_to_obj
from ...categories.models import Category
from ...conftest import get_cache_versions
from ...users.test import create_test_user
from ..events import record_event
from ..models import Thread

cache_versions = get_cache_versions()


class EventsApiTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")

        datetime = timezone.now()

        self.category = Category.objects.all_categories()[:1][0]
        self.thread = Thread(
            category=self.category,
            started_on=datetime,
            starter_name="Tester",
            starter_slug="tester",
            last_post_on=datetime,
            last_poster_name="Tester",
            last_poster_slug="tester",
        )

        self.thread.set_title("Test thread")
        self.thread.save()

        user_acl = useracl.get_user_acl(self.user, cache_versions)
        add_acl_to_obj(user_acl, self.category)
        add_acl_to_obj(user_acl, self.thread)

    def test_record_event_with_context(self):
        """record_event registers event with context in thread"""
        request = Mock(user=self.user, user_ip="123.14.15.222")
        context = {"user": "Lorem ipsum"}
        event = record_event(request, self.thread, "announcement", context)

        event_post = self.thread.post_set.order_by("-id")[:1][0]
        self.assertEqual(self.thread.last_post, event_post)
        self.assertTrue(self.thread.has_events)
        self.assertTrue(self.thread.last_post_is_event)

        self.assertEqual(event.pk, event_post.pk)
        self.assertTrue(event_post.is_event)
        self.assertEqual(event_post.event_type, "announcement")
        self.assertEqual(event_post.event_context, context)
        self.assertEqual(event_post.poster_id, request.user.pk)

    def test_record_event_is_read(self):
        """record_event makes recorded event read to its author"""
        request = Mock(user=self.user, user_ip="123.14.15.222")
        event = record_event(request, self.thread, "announcement")

        self.user.postread_set.get(
            category=self.category, thread=self.thread, post=event
        )
