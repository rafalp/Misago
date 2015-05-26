from django.contrib.auth import get_user_model

from misago.conf import settings

from misago.users.testutils import AuthenticatedUserTestCase


class UserForumOptionsTests(AuthenticatedUserTestCase):
    """
    tests for user forum options RPC (POST to /api/users/1/forum-options/)
    """
    def setUp(self):
        super(UserForumOptionsTests, self).setUp()
        self.link = '/api/users/%s/forum-options/' % self.user.pk

    def test_empty_request(self):
        """empty request is handled"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 400)

        fields = (
            'limits_private_thread_invites_to',
            'subscribe_to_started_threads',
            'subscribe_to_replied_threads'
        )

        for field in fields:
            self.assertIn('"%s"' % field, response.content)

    def test_change_forum_options(self):
        """forum options are changed"""
        response = self.client.post(self.link, data={
            'limits_private_thread_invites_to': 1,
            'subscribe_to_started_threads': 2,
            'subscribe_to_replied_threads': 1
        })
        self.assertEqual(response.status_code, 200)

        self.reload_user();

        self.assertFalse(self.user.is_hiding_presence)
        self.assertEqual(self.user.limits_private_thread_invites_to, 1)
        self.assertEqual(self.user.subscribe_to_started_threads, 2)
        self.assertEqual(self.user.subscribe_to_replied_threads, 1)
