from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.acl import add_acl
from misago.forums.models import Forum
from misago.threads.models import Thread, Post
from misago.users.models import AnonymousUser

from misago.readtracker import forumstracker, threadstracker
from misago.readtracker.dates import cutoff_date


class ReadTrackerTests(TestCase):
    def setUp(self):
        self.forums = [f for f in Forum.objects.filter(role="forum")[:1]]
        self.forum = self.forums[0]

        User = get_user_model()
        self.user = User.objects.create_user("Bob", "bob@test.com", "Pass.123")
        self.anon = AnonymousUser()

    def post_thread(self, datetime):
        thread = Thread.objects.create(
            forum=self.forum,
            weight=0,
            started_on=datetime,
            starter_name='Tester',
            starter_slug='tester',
            last_post_on=datetime,
            last_poster_name='Tester',
            last_poster_slug='tester')
        self.forum.synchronize()
        self.forum.save()
        return thread


class ForumsTrackerTests(ReadTrackerTests):
    def test_anon_empty_forum_read(self):
        """anon users content is always read"""
        forumstracker.make_read_aware(self.anon, self.forums)
        self.assertIsNone(self.forum.last_post_on)
        self.assertTrue(self.forum.is_read)

    def test_anon_forum_with_recent_reply_read(self):
        """anon users content is always read"""
        forumstracker.make_read_aware(self.anon, self.forums)
        self.forum.last_post_on = timezone.now()
        self.assertTrue(self.forum.is_read)

    def test_empty_forum_is_read(self):
        """empty forum is read for signed in user"""
        forumstracker.make_read_aware(self.user, self.forums)
        self.assertTrue(self.forum.is_read)

    def test_make_read_aware_sets_read_flag_for_empty_forum(self):
        """make_read_aware sets read flag on empty forum"""
        forumstracker.make_read_aware(self.anon, self.forums)
        self.assertTrue(self.forum.is_read)

        forumstracker.make_read_aware(self.user, self.forums)
        self.assertTrue(self.forum.is_read)

    def test_make_read_aware_sets_read_flag_for_forum_with_old_thread(self):
        """make_read_aware sets read flag on forum with old thread"""
        self.forum.last_post_on = cutoff_date() - timedelta(days=1)

        forumstracker.make_read_aware(self.user, self.forums)
        self.assertTrue(self.forum.is_read)

    def test_make_read_aware_sets_unread_flag_for_forum_with_new_thread(self):
        """make_read_aware sets unread flag on forum with new thread"""
        self.forum.last_post_on = cutoff_date() + timedelta(days=1)

        forumstracker.make_read_aware(self.user, self.forums)
        self.assertFalse(self.forum.is_read)

    def test_sync_record_for_empty_forum(self):
        """sync_record sets read flag on empty forum"""
        add_acl(self.user, self.forums)
        forumstracker.sync_record(self.user, self.forum)
        self.user.forumread_set.get(forum=self.forum)

        forumstracker.make_read_aware(self.user, self.forums)
        self.assertTrue(self.forum.is_read)

    def test_sync_record_for_forum_with_old_thread_and_reply(self):
        """
        sync_record sets read flag on forum with old thread,
        then changes flag to unread when new reply is posted
        """
        self.post_thread(cutoff_date() - timedelta(days=1))

        add_acl(self.user, self.forums)
        forumstracker.sync_record(self.user, self.forum)
        self.user.forumread_set.get(forum=self.forum)

        forumstracker.make_read_aware(self.user, self.forums)
        self.assertTrue(self.forum.is_read)

        thread = self.post_thread(cutoff_date() + timedelta(days=1))
        forumstracker.sync_record(self.user, self.forum)
        forumstracker.make_read_aware(self.user, self.forums)
        self.assertFalse(self.forum.is_read)

    def test_sync_record_for_forum_with_new_thread(self):
        """
        sync_record sets read flag on forum with old thread,
        then keeps flag to unread when new reply is posted
        """
        self.post_thread(cutoff_date() + timedelta(days=1))

        add_acl(self.user, self.forums)
        forumstracker.sync_record(self.user, self.forum)
        self.user.forumread_set.get(forum=self.forum)

        forumstracker.make_read_aware(self.user, self.forums)
        self.assertFalse(self.forum.is_read)

        self.post_thread(cutoff_date() + timedelta(days=1))
        forumstracker.sync_record(self.user, self.forum)
        forumstracker.make_read_aware(self.user, self.forums)
        self.assertFalse(self.forum.is_read)

    def test_sync_record_for_forum_with_deleted_threads(self):
        """unread forum reverts to read after its emptied"""
        self.post_thread(cutoff_date() + timedelta(days=1))
        self.post_thread(cutoff_date() + timedelta(days=1))
        self.post_thread(cutoff_date() + timedelta(days=1))

        add_acl(self.user, self.forums)
        forumstracker.sync_record(self.user, self.forum)
        forumstracker.make_read_aware(self.user, self.forums)
        self.assertFalse(self.forum.is_read)

        self.forum.thread_set.all().delete()
        self.forum.synchronize()
        self.forum.save()

        forumstracker.make_read_aware(self.user, self.forums)
        self.assertTrue(self.forum.is_read)

    def test_sync_record_for_forum_with_many_threads(self):
        """sync_record sets unread flag on forum with many threads"""
        self.post_thread(cutoff_date() + timedelta(days=1))
        self.post_thread(cutoff_date() - timedelta(days=1))
        self.post_thread(cutoff_date() + timedelta(days=1))
        self.post_thread(cutoff_date() - timedelta(days=1))

        add_acl(self.user, self.forums)
        forumstracker.sync_record(self.user, self.forum)
        self.user.forumread_set.get(forum=self.forum)

        forumstracker.make_read_aware(self.user, self.forums)
        self.assertFalse(self.forum.is_read)

        self.post_thread(cutoff_date() + timedelta(days=1))
        forumstracker.sync_record(self.user, self.forum)
        forumstracker.make_read_aware(self.user, self.forums)
        self.assertFalse(self.forum.is_read)
