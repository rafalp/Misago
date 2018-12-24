from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ...categories.models import Category
from ...conf import settings
from ...threads import test
from ...users.test import create_test_user
from ..poststracker import make_read_aware, save_read


class AnonymousUser:
    is_authenticated = False
    is_anonymous = True


class PostsTrackerTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")
        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(self.category)

    def test_falsy_value(self):
        """passing falsy value to readtracker causes no errors"""
        make_read_aware(self.user, None)
        make_read_aware(self.user, False)
        make_read_aware(self.user, [])

    def test_anon_post_before_cutoff(self):
        """non-tracked post is marked as read for anonymous users"""
        posted_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        post = test.reply_thread(self.thread, posted_on=posted_on)

        make_read_aware(AnonymousUser(), post)
        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)

    def test_anon_post_after_cutoff(self):
        """tracked post is marked as read for anonymous users"""
        post = test.reply_thread(self.thread, posted_on=timezone.now())

        make_read_aware(AnonymousUser(), post)
        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)

    def test_user_post_before_cutoff(self):
        """untracked post is marked as read for authenticated users"""
        posted_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        post = test.reply_thread(self.thread, posted_on=posted_on)

        make_read_aware(self.user, post)
        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)

    def test_user_unread_post(self):
        """tracked post is marked as unread for authenticated users"""
        post = test.reply_thread(self.thread, posted_on=timezone.now())

        make_read_aware(self.user, post)
        self.assertFalse(post.is_read)
        self.assertTrue(post.is_new)

    def test_user_created_after_post(self):
        """tracked post older than user is marked as read"""
        posted_on = timezone.now() - timedelta(days=1)
        post = test.reply_thread(self.thread, posted_on=posted_on)

        make_read_aware(self.user, post)
        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)

    def test_user_read_post(self):
        """tracked post is marked as read for authenticated users with read entry"""
        post = test.reply_thread(self.thread, posted_on=timezone.now())

        save_read(self.user, post)
        make_read_aware(self.user, post)

        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)
