from .. import test
from ...users.test import create_test_user
from ..models import ThreadParticipant
from .test_privatethreads import PrivateThreadsTestCase


class PrivateThreadReplyApiTestCase(PrivateThreadsTestCase):
    def setUp(self):
        super().setUp()

        self.thread = test.post_thread(self.category, poster=self.user)
        self.api_link = self.thread.get_posts_api_url()

        self.other_user = create_test_user("OtherUser", "otheruser@example.com")

    def test_reply_private_thread(self):
        """api sets other private thread participants sync thread flag"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participants(self.thread, [self.other_user])

        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        # don't count private thread replies
        self.reload_user()
        self.assertEqual(self.user.threads, 0)
        self.assertEqual(self.user.posts, 0)

        self.assertEqual(self.user.audittrail_set.count(), 1)

        # valid user was flagged to sync
        self.user.refresh_from_db()
        self.assertFalse(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)
