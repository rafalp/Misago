from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.categories.models import Category
from misago.conf import settings
from misago.readtracker import poststracker
from misago.readtracker.models import PostRead
from misago.threads import testutils


UserModel = get_user_model()


class AnonymousUser(object):
    is_authenticated = False
    is_anonymous = True


class PostsTrackerTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user("UserA", "testa@user.com", 'Pass.123')
        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(self.category)

    def test_falsy_value(self):
        """passing falsy value to readtracker causes no errors"""
        poststracker.make_read_aware(self.user, None)
        poststracker.make_read_aware(self.user, False)
        poststracker.make_read_aware(self.user, [])

    def test_anon_post_behind_cutoff(self):
        """non-tracked post is marked as read for anonymous users"""
        posted_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        post = testutils.reply_thread(self.thread, posted_on=posted_on)

        poststracker.make_read_aware(AnonymousUser(), post)
        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)

    def test_anon_post_after_cutoff(self):
        """tracked post is marked as read for anonymous users"""
        post = testutils.reply_thread(self.thread, posted_on=timezone.now())

        poststracker.make_read_aware(AnonymousUser(), post)
        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)

    def test_user_post_behind_cutoff(self):
        """untracked post is marked as read for authenticated users"""
        posted_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        post = testutils.reply_thread(self.thread, posted_on=posted_on)

        poststracker.make_read_aware(self.user, post)
        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)

    def test_user_unread_post(self):
        """tracked post is marked as unread for authenticated users"""
        post = testutils.reply_thread(self.thread, posted_on=timezone.now())

        poststracker.make_read_aware(self.user, post)
        self.assertFalse(post.is_read)
        self.assertTrue(post.is_new)

    def test_user_created_after_post(self):
        """tracked post older than user is marked as read"""
        posted_on = timezone.now() - timedelta(days=1)
        post = testutils.reply_thread(self.thread, posted_on=posted_on)

        poststracker.make_read_aware(self.user, post)
        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)

    def test_user_read_post(self):
        """tracked post is marked as read for authenticated users with read entry"""
        post = testutils.reply_thread(self.thread, posted_on=timezone.now())

        poststracker.save_read(self.user, post)
        poststracker.make_read_aware(self.user, post)

        self.assertTrue(post.is_read)
        self.assertFalse(post.is_new)

    def test_delete_reads(self):
        """delete_reads util removes post's reads"""
        post = testutils.reply_thread(self.thread, posted_on=timezone.now())
        other_post = testutils.reply_thread(self.thread, posted_on=timezone.now())

        poststracker.save_read(self.user, post)
        poststracker.save_read(self.user, other_post)

        self.assertEqual(PostRead.objects.count(), 2)

        poststracker.delete_reads(post)

        self.assertEqual(PostRead.objects.count(), 1)

