from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from misago.acl.useracl import get_user_acl
from misago.categories.models import Category
from misago.conf import settings
from misago.conftest import get_cache_versions
from misago.readtracker import categoriestracker, poststracker
from misago.readtracker.models import PostRead
from misago.threads import test
from misago.users.test import create_test_user

cache_versions = get_cache_versions()


class AnonymousUser(object):
    is_authenticated = False
    is_anonymous = True


class CategoriesTrackerTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")
        self.user_acl = get_user_acl(self.user, cache_versions)
        self.category = Category.objects.get(slug="first-category")

    def test_falsy_value(self):
        """passing falsy value to readtracker causes no errors"""
        categoriestracker.make_read_aware(self.user, self.user_acl, None)
        categoriestracker.make_read_aware(self.user, self.user_acl, False)
        categoriestracker.make_read_aware(self.user, self.user_acl, [])

    def test_anon_thread_before_cutoff(self):
        """non-tracked thread is marked as read for anonymous users"""
        started_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        test.post_thread(self.category, started_on=started_on)

        categoriestracker.make_read_aware(AnonymousUser(), None, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)

    def test_anon_thread_after_cutoff(self):
        """tracked thread is marked as read for anonymous users"""
        test.post_thread(self.category, started_on=timezone.now())

        categoriestracker.make_read_aware(AnonymousUser(), None, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)

    def test_user_thread_before_cutoff(self):
        """non-tracked thread is marked as read for authenticated users"""
        started_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        test.post_thread(self.category, started_on=started_on)

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)

    def test_user_unread_thread(self):
        """tracked thread is marked as unread for authenticated users"""
        test.post_thread(self.category, started_on=timezone.now())

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertFalse(self.category.is_read)
        self.assertTrue(self.category.is_new)

    def test_user_created_after_thread(self):
        """tracked thread older than user is marked as read"""
        started_on = timezone.now() - timedelta(days=1)
        test.post_thread(self.category, started_on=started_on)

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)

    def test_user_read_post(self):
        """tracked thread with read post marked as read"""
        thread = test.post_thread(self.category, started_on=timezone.now())

        poststracker.save_read(self.user, thread.first_post)

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)

    def test_user_first_unread_last_read_post(self):
        """tracked thread with unread first and last read post marked as unread"""
        thread = test.post_thread(self.category, started_on=timezone.now())

        post = test.reply_thread(thread, posted_on=timezone.now())
        poststracker.save_read(self.user, post)

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertFalse(self.category.is_read)
        self.assertTrue(self.category.is_new)

    def test_user_first_read_post_unread_event(self):
        """tracked thread with read first post and unread event"""
        thread = test.post_thread(self.category, started_on=timezone.now())
        poststracker.save_read(self.user, thread.first_post)

        test.reply_thread(thread, posted_on=timezone.now(), is_event=True)

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertFalse(self.category.is_read)
        self.assertTrue(self.category.is_new)

    def test_user_hidden_event(self):
        """tracked thread with unread first post and hidden event"""
        thread = test.post_thread(self.category, started_on=timezone.now())

        test.reply_thread(
            thread, posted_on=timezone.now(), is_event=True, is_hidden=True
        )

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertFalse(self.category.is_read)
        self.assertTrue(self.category.is_new)

    def test_user_first_read_post_hidden_event(self):
        """tracked thread with read first post and hidden event"""
        thread = test.post_thread(self.category, started_on=timezone.now())
        poststracker.save_read(self.user, thread.first_post)

        test.reply_thread(
            thread, posted_on=timezone.now(), is_event=True, is_hidden=True
        )

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)

    def test_user_thread_before_cutoff_unread_post(self):
        """non-tracked thread is marked as unread for anonymous users"""
        started_on = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        test.post_thread(self.category, started_on=started_on)

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)

    def test_user_first_read_post_unapproved_post(self):
        """tracked thread with read first post and unapproved post"""
        thread = test.post_thread(self.category, started_on=timezone.now())
        poststracker.save_read(self.user, thread.first_post)

        test.reply_thread(thread, posted_on=timezone.now(), is_unapproved=True)

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)

    def test_user_first_read_post_unapproved_own_post(self):
        """tracked thread with read first post and unapproved own post"""
        thread = test.post_thread(self.category, started_on=timezone.now())
        poststracker.save_read(self.user, thread.first_post)

        test.reply_thread(
            thread, posted_on=timezone.now(), poster=self.user, is_unapproved=True
        )

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertFalse(self.category.is_read)
        self.assertTrue(self.category.is_new)

    def test_user_first_read_post_unapproved_own_post(self):
        """tracked thread with read first post and unapproved own post"""
        thread = test.post_thread(self.category, started_on=timezone.now())
        poststracker.save_read(self.user, thread.first_post)

        test.reply_thread(
            thread, posted_on=timezone.now(), poster=self.user, is_unapproved=True
        )

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertFalse(self.category.is_read)
        self.assertTrue(self.category.is_new)

    def test_user_unapproved_thread_unread_post(self):
        """tracked unapproved thread"""
        thread = test.post_thread(
            self.category, started_on=timezone.now(), is_unapproved=True
        )

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)

    def test_user_unapproved_own_thread_unread_post(self):
        """tracked unapproved but visible thread"""
        thread = test.post_thread(
            self.category,
            poster=self.user,
            started_on=timezone.now(),
            is_unapproved=True,
        )

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertFalse(self.category.is_read)
        self.assertTrue(self.category.is_new)

    def test_user_hidden_thread_unread_post(self):
        """tracked hidden thread"""
        thread = test.post_thread(
            self.category, started_on=timezone.now(), is_hidden=True
        )

        categoriestracker.make_read_aware(self.user, self.user_acl, self.category)
        self.assertTrue(self.category.is_read)
        self.assertFalse(self.category.is_new)
