from .. import test
from ...users.test import create_test_user
from ..models import ThreadParticipant
from .test_privatethreads import PrivateThreadsTestCase


class SyncUnreadPrivateThreadsTestCase(PrivateThreadsTestCase):
    def setUp(self):
        super().setUp()

        self.other_user = create_test_user("OtherUser", "user@example.com")
        self.thread = test.post_thread(self.category, poster=self.user)

        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

    def test_middleware_counts_new_thread(self):
        """middleware counts new thread"""
        self.user.sync_unread_private_threads = True
        self.user.save()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        # user was resynced
        self.reload_user()

        self.assertFalse(self.user.sync_unread_private_threads)
        self.assertEqual(self.user.unread_private_threads, 1)

    def test_middleware_counts_unread_thread(self):
        """
        middleware counts thread with unread reply, post read flags user for recount
        """
        self.user.sync_unread_private_threads = True
        self.user.save()

        self.client.post(self.thread.last_post.get_read_api_url())

        # post read zeroed list of unread private threads
        self.reload_user()
        self.assertFalse(self.user.sync_unread_private_threads)
        self.assertEqual(self.user.unread_private_threads, 0)

        # reply to thread
        test.reply_thread(self.thread)

        self.user.sync_unread_private_threads = True
        self.user.save()

        # middleware did recount and accounted for new unread post
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertFalse(self.user.sync_unread_private_threads)
        self.assertEqual(self.user.unread_private_threads, 1)
