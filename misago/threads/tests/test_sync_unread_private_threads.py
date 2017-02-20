from django.contrib.auth import get_user_model

from misago.threads import testutils
from misago.threads.models import ThreadParticipant

from .test_privatethreads import PrivateThreadsTestCase


UserModel = get_user_model()


class SyncUnreadPrivateThreadsTestCase(PrivateThreadsTestCase):
    def setUp(self):
        super(SyncUnreadPrivateThreadsTestCase, self).setUp()

        self.other_user = UserModel.objects.create_user(
            'BobBoberson', 'bob@boberson.com', 'pass123'
        )

        self.thread = testutils.post_thread(self.category, poster=self.user)

        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

    def test_middleware_counts_new_thread(self):
        """middleware counts new thread"""
        self.user.sync_unread_private_threads = True
        self.user.save()

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # user was resynced
        self.reload_user()

        self.assertFalse(self.user.sync_unread_private_threads)
        self.assertEqual(self.user.unread_private_threads, 1)

    def test_middleware_counts_unread_thread(self):
        """middleware counts thread with unread reply, post read flags user for recount"""
        self.user.sync_unread_private_threads = True
        self.user.save()

        self.client.post(self.thread.last_post.get_read_api_url())

        # post read zeroed list of unread private threads
        self.reload_user()
        self.assertFalse(self.user.sync_unread_private_threads)
        self.assertEqual(self.user.unread_private_threads, 0)

        # reply to thread
        testutils.reply_thread(self.thread)

        self.user.sync_unread_private_threads = True
        self.user.save()

        # middleware did recount and accounted for new unread post
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertFalse(self.user.sync_unread_private_threads)
        self.assertEqual(self.user.unread_private_threads, 1)
