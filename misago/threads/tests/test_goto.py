from django.conf import settings

from misago.acl import add_acl
from misago.forums.models import Forum
from misago.readtracker import threadstracker
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import goto
from misago.threads.permissions import exclude_invisible_posts
from misago.threads.testutils import post_thread, reply_thread


POSTS_PER_PAGE = settings.MISAGO_POSTS_PER_PAGE
THREAD_TAIL = settings.MISAGO_THREAD_TAIL
MAX_PAGE_LEN = POSTS_PER_PAGE + THREAD_TAIL


class MockThreadsCounter(object):
    def set(self, *args, **kwargs):
        pass

    def decrease(self, *args, **kwargs):
        pass


class GotoTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(GotoTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.forum.labels = []

        self.thread = post_thread(self.forum)
        add_acl(self.user, self.forum)
        add_acl(self.user, self.thread)

    def test_get_thread_pages(self):
        """get_thread_pages returns valid count of pages for given positions"""
        self.assertEqual(goto.get_thread_pages(1), 1)
        self.assertEqual(goto.get_thread_pages(POSTS_PER_PAGE), 1)
        self.assertEqual(goto.get_thread_pages(MAX_PAGE_LEN), 1)
        self.assertEqual(goto.get_thread_pages(MAX_PAGE_LEN + 1), 2)
        self.assertEqual(goto.get_thread_pages(POSTS_PER_PAGE * 2 - 1), 2)
        self.assertEqual(goto.get_thread_pages(POSTS_PER_PAGE * 2), 2)

        self.assertEqual(goto.get_thread_pages(POSTS_PER_PAGE * 3), 3)
        self.assertEqual(goto.get_thread_pages(
            POSTS_PER_PAGE * 5 + THREAD_TAIL - 1), 5)

    def test_get_post_page(self):
        """get_post_page returns valid page number for given queryset"""
        self.assertEqual(goto.get_post_page(1, self.thread.post_set), 1)

        # fill out page
        [reply_thread(self.thread) for p in xrange(MAX_PAGE_LEN - 1)]
        self.assertEqual(
            goto.get_post_page(MAX_PAGE_LEN, self.thread.post_set), 1)

        # add 2 posts, adding second page
        [reply_thread(self.thread) for p in xrange(2)]
        self.assertEqual(
            goto.get_post_page(MAX_PAGE_LEN + 2, self.thread.post_set), 2)

    def test_hashed_reverse(self):
        """hashed_reverse returns complete url for given post"""
        url = goto.hashed_reverse(self.thread, self.thread.first_post)
        url_formats = self.thread.get_absolute_url(), self.thread.first_post_id
        self.assertEqual(url, '%s#post-%s' % url_formats)

        url = goto.hashed_reverse(self.thread, self.thread.first_post, 4)
        url_formats = self.thread.get_absolute_url(), self.thread.first_post_id
        self.assertEqual(url, '%s4/#post-%s' % url_formats)

    def test_last(self):
        """last returns link to last post in thread"""
        url_last = goto.last(self.thread, self.thread.post_set)
        url_formats = self.thread.get_absolute_url(), self.thread.last_post_id
        self.assertEqual(url_last, '%s#post-%s' % url_formats)

        # add posts to reach page limit
        [reply_thread(self.thread) for p in xrange(MAX_PAGE_LEN - 1)]

        url_last = goto.last(self.thread, self.thread.post_set)
        url_formats = self.thread.get_absolute_url(), self.thread.last_post_id
        self.assertEqual(url_last, '%s#post-%s' % url_formats)

        # add 2 posts to add second page to thread
        [reply_thread(self.thread) for p in xrange(2)]

        url_last = goto.last(self.thread, self.thread.post_set)
        url_formats = self.thread.get_absolute_url(), self.thread.last_post_id
        self.assertEqual(url_last, '%s2/#post-%s' % url_formats)

    def test_get_post_link(self):
        """get_post_link returns link to specified post"""
        post_link = goto.get_post_link(
            1, self.thread.post_set, self.thread, self.thread.last_post)
        last_link = goto.last(self.thread, self.thread.post_set)
        self.assertEqual(post_link, last_link)

        # add posts to add extra page to thread
        [reply_thread(self.thread) for p in xrange(MAX_PAGE_LEN)]

        post_link = goto.get_post_link(
            MAX_PAGE_LEN + 1,
            self.thread.post_set, self.thread, self.thread.last_post)
        last_link = goto.last(self.thread, self.thread.post_set)
        self.assertEqual(post_link, last_link)

    def test_new(self):
        """new returns link to first unread post"""
        self.user.new_threads = MockThreadsCounter()
        self.user.unread_threads = MockThreadsCounter()

        post_link = goto.new(self.user, self.thread, self.thread.post_set)
        last_link = goto.last(self.thread, self.thread.post_set)
        self.assertEqual(post_link, last_link)

        # add extra page to thread, then read them
        [reply_thread(self.thread) for p in xrange(MAX_PAGE_LEN)]
        threadstracker.read_thread(
            self.user, self.thread, self.thread.last_post)

        # add extra unread posts
        first_unread = reply_thread(self.thread)
        [reply_thread(self.thread) for p in xrange(20)]

        new_link = goto.new(self.user, self.thread, self.thread.post_set)
        post_link = goto.get_post_link(
            MAX_PAGE_LEN + 21, self.thread.post_set, self.thread, first_unread)
        self.assertEqual(new_link, post_link)

        # read thread
        threadstracker.read_thread(
            self.user, self.thread, self.thread.last_post)

        # assert new() points to last reply
        post_link = goto.new(self.user, self.thread, self.thread.post_set)
        last_link = goto.last(self.thread, self.thread.post_set)
        self.assertEqual(post_link, last_link)

    def test_post(self):
        """post returns link to post given"""
        thread = self.thread

        post_link = goto.post(thread, thread.post_set, thread.last_post)
        last_link = goto.last(self.thread, self.thread.post_set)
        self.assertEqual(post_link, last_link)

        # add 24 posts
        [reply_thread(self.thread) for p in xrange(24)]

        post_link = goto.post(thread, thread.post_set, thread.last_post)
        last_link = goto.last(self.thread, self.thread.post_set)
        self.assertEqual(post_link, last_link)
