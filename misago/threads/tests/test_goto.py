from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import goto
from misago.threads.testutils import post_thread, reply_thread


class GotoTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(GotoTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.forum.labels = []

        self.thread = post_thread(self.forum)

    def test_get_thread_pages(self):
        """get_thread_pages returns valid count of pages for given positions"""
        self.assertEqual(goto.get_thread_pages(1), 1)
        self.assertEqual(goto.get_thread_pages(10), 1)
        self.assertEqual(goto.get_thread_pages(13), 1)
        self.assertEqual(goto.get_thread_pages(14), 2)
        self.assertEqual(goto.get_thread_pages(19), 2)
        self.assertEqual(goto.get_thread_pages(20), 2)
        self.assertEqual(goto.get_thread_pages(23), 2)
        self.assertEqual(goto.get_thread_pages(24), 3)
        self.assertEqual(goto.get_thread_pages(27), 3)
        self.assertEqual(goto.get_thread_pages(36), 4)
        self.assertEqual(goto.get_thread_pages(373), 37)

    def test_get_post_page(self):
        """get_post_page returns valid page number for given queryset"""
        self.assertEqual(goto.get_post_page(1, self.thread.post_set), 1)

        # add 12 posts, bumping no of posts on page to to 13
        [reply_thread(self.thread) for p in xrange(12)]
        self.assertEqual(goto.get_post_page(13, self.thread.post_set), 1)

        # add 2 posts
        [reply_thread(self.thread) for p in xrange(2)]
        self.assertEqual(goto.get_post_page(15, self.thread.post_set), 2)
