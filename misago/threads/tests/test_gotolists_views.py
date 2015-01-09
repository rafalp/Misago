from misago.acl import add_acl
from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.testutils import post_thread, reply_thread


class GotoListsViewsTests(AuthenticatedUserTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def setUp(self):
        super(GotoListsViewsTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.forum.labels = []

        self.thread = post_thread(self.forum)

    def override_acl(self, new_acl):
        new_acl.update({
            'can_browse': True,
            'can_see': True,
            'can_see_all_threads': True,
        })

        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = new_acl
        override_acl(self.user, forums_acl)

        self.forum.acl = {}
        add_acl(self.user, self.forum)

    def test_moderated_list(self):
        """moderated posts list works"""
        self.override_acl({'can_review_moderated_content': True})
        response = self.client.get(self.thread.get_moderated_url(),
                                   **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("0 unapproved posts", response.content)
        self.assertIn("There are no posts to display on this list.",
                      response.content)

        # post 10 not moderated posts
        [reply_thread(self.thread) for i in xrange(10)]

        # assert that posts don't show
        self.override_acl({'can_review_moderated_content': True})
        response = self.client.get(self.thread.get_moderated_url(),
                                   **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("0 unapproved posts", response.content)
        self.assertIn("There are no posts to display on this list.",
                      response.content)

        # post 10 reported posts
        posts = []
        for i in xrange(10):
            posts.append(reply_thread(self.thread, is_moderated=True))

        # assert that posts show
        self.override_acl({'can_review_moderated_content': True})
        response = self.client.get(self.thread.get_moderated_url(),
                                   **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("10 unapproved posts", response.content)
        self.assertNotIn("There are no posts to display on this list.",
                         response.content)

        for post in posts:
            self.assertIn(post.get_absolute_url(), response.content)

        # overflow list via posting extra 20 reported posts
        posts = []
        for i in xrange(20):
            posts.append(reply_thread(self.thread, is_moderated=True))

        # assert that posts don't show
        self.override_acl({'can_review_moderated_content': True})
        response = self.client.get(self.thread.get_moderated_url(),
                                   **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("30 unapproved posts", response.content)
        self.assertIn("This list is limited to last 15 posts.",
                      response.content)

        for post in posts[15:]:
            self.assertIn(post.get_absolute_url(), response.content)

    def test_reported_list(self):
        """reported posts list works"""
        self.override_acl({'can_see_reports': True})
        response = self.client.get(self.thread.get_reported_url(),
                                   **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("0 reported posts", response.content)
        self.assertIn("There are no posts to display on this list.",
                      response.content)

        # post 10 not reported posts
        [reply_thread(self.thread) for i in xrange(10)]

        # assert that posts don't show
        self.override_acl({'can_see_reports': True})
        response = self.client.get(self.thread.get_reported_url(),
                                   **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("0 reported posts", response.content)
        self.assertIn("There are no posts to display on this list.",
                      response.content)

        # post 10 posts with closed reports
        [reply_thread(self.thread, has_reports=True) for i in xrange(10)]

        # assert that posts don't show
        self.override_acl({'can_see_reports': True})
        response = self.client.get(self.thread.get_reported_url(),
                                   **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("0 reported posts", response.content)
        self.assertIn("There are no posts to display on this list.",
                      response.content)

        # post 10 reported posts
        posts = []
        for i in xrange(10):
            posts.append(reply_thread(self.thread, has_open_reports=True))

        # assert that posts show
        self.override_acl({'can_see_reports': True})
        response = self.client.get(self.thread.get_reported_url(),
                                   **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("10 reported posts", response.content)
        self.assertNotIn("There are no posts to display on this list.",
                         response.content)

        for post in posts:
            self.assertIn(post.get_absolute_url(), response.content)

        # overflow list via posting extra 20 reported posts
        posts = []
        for i in xrange(20):
            posts.append(reply_thread(self.thread, has_open_reports=True))

        # assert that posts don't show
        self.override_acl({'can_see_reports': True})
        response = self.client.get(self.thread.get_reported_url(),
                                   **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("30 reported posts", response.content)
        self.assertIn("This list is limited to last 15 posts.",
                      response.content)

        for post in posts[15:]:
            self.assertIn(post.get_absolute_url(), response.content)
