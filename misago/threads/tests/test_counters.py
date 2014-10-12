from time import time

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.counts import NewThreadsCount, UnreadThreadsCount
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

        self.assertTrue(counter.is_cache_valid({'expires': time() + 15}))
        self.assertFalse(counter.is_cache_valid({'expires': time() - 15}))

    def test_get_expiration_timestamp(self):
        """get_expiration_timestamp returns greater time than current one"""
        counter = NewThreadsCount(self.user, {})
        self.assertTrue(counter.get_expiration_timestamp() > time())

    def test_get_real_count(self):
        """get_real_count returns valid count of new threads"""
        counter = NewThreadsCount(self.user, {})
        self.assertEqual(counter.count, 0)
        self.assertEqual(counter.get_real_count()['threads'], 0)

        # create 10 new threads
        threads = [testutils.post_thread(self.forum) for t in xrange(10)]
        self.assertEqual(counter.get_real_count()['threads'], 10)

        # create new counter
        counter = NewThreadsCount(self.user, {})
        self.assertEqual(counter.count, 10)
        self.assertEqual(counter.get_real_count()['threads'], 10)

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
