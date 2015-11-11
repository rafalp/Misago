from misago.acl import add_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import goto
from misago.threads.testutils import post_thread, reply_thread


class GotoViewsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(GotoViewsTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.forum.labels = []

        self.thread = post_thread(self.forum)
        add_acl(self.user, self.forum)
        add_acl(self.user, self.thread)

    def test_goto_last(self):
        """thread_last link points to last post in thread"""
        response = self.client.get(self.thread.get_last_reply_url())
        self.assertEqual(response.status_code, 302)
        last_link = goto.last(self.thread, self.thread.post_set)
        self.assertTrue(response['location'].endswith(last_link))

        # add 36 posts to thread
        [reply_thread(self.thread) for p in xrange(36)]

        response = self.client.get(self.thread.get_last_reply_url())
        self.assertEqual(response.status_code, 302)
        last_link = goto.last(self.thread, self.thread.post_set)
        self.assertTrue(response['location'].endswith(last_link))

    def test_goto_new(self):
        """thread_new link points to first unread post in thread"""
        # add 32 posts to thread
        [reply_thread(self.thread) for p in xrange(32)]

        # read thread
        response = self.client.get(self.thread.get_last_reply_url())
        response = self.client.get(response['location'])

        # add unread posts
        unread_post = reply_thread(self.thread)
        [reply_thread(self.thread) for p in xrange(32)]

        response = self.client.get(self.thread.get_new_reply_url())
        self.assertEqual(response.status_code, 302)
        unread_link = goto.new(self.user, self.thread, self.thread.post_set)
        self.assertTrue(response['location'].endswith(unread_link))

    def test_goto_post(self):
        """thread_post link points to specific post in thread"""
        # add 32 posts to thread
        [reply_thread(self.thread) for p in xrange(32)]

        # add target post to thread
        target_post = reply_thread(self.thread)

        # add 32 more posts to thread
        [reply_thread(self.thread) for p in xrange(32)]

        # see post link
        post_link = goto.post(self.thread, self.thread.post_set, target_post)

        response = self.client.get(target_post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(post_link))
