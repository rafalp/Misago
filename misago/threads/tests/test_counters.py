from datetime import timedelta
from time import time

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _

from misago.forums.models import Forum
from misago.readtracker.models import ThreadRead
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.counts import (NewThreadsCount,
                                   sync_user_unread_private_threads_count)
from misago.threads import testutils


class TestNewThreadsCount(AuthenticatedUserTestCase):
    def setUp(self):
        super(TestNewThreadsCount, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]

    def test_cast_to_int(self):
        """counter is castable to int"""
        counter = NewThreadsCount(self.user, {})
        self.assertEqual(int(counter), 0)

        threads = [testutils.post_thread(self.forum) for t in xrange(42)]
        counter = NewThreadsCount(self.user, {})
        self.assertEqual(int(counter), 42)

    def test_cast_to_bool(self):
        """counter is castable to bool"""
        counter = NewThreadsCount(self.user, {})
        self.assertFalse(counter)

        threads = [testutils.post_thread(self.forum) for t in xrange(42)]
        counter = NewThreadsCount(self.user, {})
        self.assertTrue(counter)

    def test_is_cache_valid(self):
        """is_cache_valid returns valid value for different caches"""
        counter = NewThreadsCount(self.user, {})

        self.assertTrue(counter.is_cache_valid({
            'expires': time() + 15,
            'user': self.user.pk
        }))

        self.assertFalse(counter.is_cache_valid({
            'expires': time() - 15,
            'user': self.user.pk
        }))

        self.assertFalse(counter.is_cache_valid({
            'expires': time() + 15,
            'user': self.user.pk + 1
        }))

    def test_get_expiration_timestamp(self):
        """get_expiration_timestamp returns greater time than current one"""
        counter = NewThreadsCount(self.user, {})
        self.assertTrue(counter.get_expiration_timestamp() > time())

    def test_get_current_count_dict(self):
        """get_current_count_dict returns valid count of new threads"""
        counter = NewThreadsCount(self.user, {})
        self.assertEqual(counter.count, 0)
        self.assertEqual(counter.get_current_count_dict()['threads'], 0)

        # create 10 new threads
        threads = [testutils.post_thread(self.forum) for t in xrange(10)]
        self.assertEqual(counter.get_current_count_dict()['threads'], 10)

        # create new counter
        counter = NewThreadsCount(self.user, {})
        self.assertEqual(counter.count, 10)
        self.assertEqual(counter.get_current_count_dict()['threads'], 10)

    def test_set(self):
        """set allows for changing count of threads"""
        session = {}
        counter = NewThreadsCount(self.user, session)
        counter.set(128)

        self.assertEqual(int(counter), 128)
        self.assertEqual(session[counter.name]['threads'], 128)

    def test_decrease(self):
        """decrease is not allowing for negative threads counts"""
        session = {}
        counter = NewThreadsCount(self.user, session)
        counter.set(128)
        counter.decrease()

        self.assertEqual(int(counter), 127)
        self.assertEqual(session[counter.name]['threads'], 127)

    def test_decrease_zero(self):
        """decrease is not allowing for negative threads counts"""
        session = {}
        counter = NewThreadsCount(self.user, session)
        counter.decrease()

        self.assertEqual(int(counter), 0)
        self.assertEqual(session[counter.name]['threads'], 0)


class TestSyncUnreadPrivateThreadsCount(AuthenticatedUserTestCase):
    def setUp(self):
        super(TestSyncUnreadPrivateThreadsCount, self).setUp()

        self.forum = Forum.objects.private_threads()
        self.user.sync_unread_private_threads = True

    def test_user_with_no_threads(self):
        """user with no private threads has 0 unread threads"""
        for i in range(5):
            # post 5 invisible threads
            testutils.post_thread(
                self.forum, started_on=timezone.now() - timedelta(days=2))

        sync_user_unread_private_threads_count(self.user)
        self.assertEqual(self.user.unread_private_threads, 0)

    def test_user_with_new_thread(self):
        """user has one new private thred"""
        for i in range(5):
            # post 5 invisible threads
            testutils.post_thread(
                self.forum, started_on=timezone.now() - timedelta(days=2))

        thread = testutils.post_thread(
            self.forum, started_on=timezone.now() - timedelta(days=2))
        thread.threadparticipant_set.create(user=self.user)

        sync_user_unread_private_threads_count(self.user)
        self.assertEqual(self.user.unread_private_threads, 1)

    def test_user_with_new_thread(self):
        """user has one unread private thred"""
        for i in range(5):
            # post 5 invisible threads
            testutils.post_thread(
                self.forum, started_on=timezone.now() - timedelta(days=2))

        thread = testutils.post_thread(
            self.forum, started_on=timezone.now() - timedelta(days=2))
        thread.threadparticipant_set.create(user=self.user)

        ThreadRead.objects.create(
            user=self.user,
            forum=self.forum,
            thread=thread,
            last_read_on=timezone.now() - timedelta(days=3))

        sync_user_unread_private_threads_count(self.user)
        self.assertEqual(self.user.unread_private_threads, 1)
