from misago.acl import add_acl
from misago.acl.testutils import override_acl
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

    def override_acl(self, new_acl):
        new_acl.update({'can_see': True, 'can_browse': True})

        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk].update(new_acl)
        override_acl(self.user, forums_acl)

    def test_goto_last(self):
        """thread_last link points to last post in thread"""
        response = self.client.get(self.thread.get_last_reply_url())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response['location'].endswith(goto.last(self.user, self.thread)))

        # add 36 posts to thread
        [reply_thread(self.thread) for p in xrange(36)]

        response = self.client.get(self.thread.get_last_reply_url())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response['location'].endswith(goto.last(self.user, self.thread)))

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

        unread_post_link = goto.new(self.user, self.thread)

        response = self.client.get(self.thread.get_new_reply_url())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(unread_post_link))

    def test_goto_reported(self):
        """thread_reported link points to first reported post in thread"""
        # add 32 posts to thread
        [reply_thread(self.thread) for p in xrange(32)]

        # add reported post to thread
        reported_post = reply_thread(self.thread, is_reported=True)

        # add 32 more posts to thread
        [reply_thread(self.thread) for p in xrange(32)]

        # see reported post link
        self.override_acl({'can_see_reports': 1})
        reported_post_link = goto.post(self.user, self.thread, reported_post)

        self.override_acl({'can_see_reports': 1})
        response = self.client.get(self.thread.get_reported_reply_url())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(reported_post_link))

    def test_goto_moderated(self):
        """thread_moderated link points to first moderated post in thread"""
        # add 32 posts to thread
        [reply_thread(self.thread) for p in xrange(32)]

        # add moderated post to thread
        moderated_post = reply_thread(self.thread, is_moderated=True)

        # add 32 more posts to thread
        [reply_thread(self.thread) for p in xrange(32)]

        # see moderated post link
        self.override_acl({'can_review_moderated_content': 1})
        moderated_post_link = goto.post(self.user, self.thread, moderated_post)

        response = self.client.get(self.thread.get_moderated_reply_url())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(moderated_post_link))

    def test_goto_post(self):
        """thread_post link points to specific post in thread"""
        # add 32 posts to thread
        [reply_thread(self.thread) for p in xrange(32)]

        # add target post to thread
        target_post = reply_thread(self.thread)

        # add 32 more posts to thread
        [reply_thread(self.thread) for p in xrange(32)]

        # see post link
        post_link = goto.post(self.user, self.thread, target_post)

        response = self.client.get(target_post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(post_link))
