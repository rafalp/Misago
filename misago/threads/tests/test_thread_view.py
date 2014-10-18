from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.models import Thread
from misago.threads.testutils import post_thread, reply_thread


class ThreadViewTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadViewTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.thread = post_thread(self.forum)

    def override_acl(self, new_acl):
        new_acl.update({'can_browse': True})

        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = new_acl
        override_acl(self.user, forums_acl)

        self.forum.acl = {}
        add_acl(self.user, self.forum)

    def reload_thread(self):
        self.thread = Thread.objects.get(id=thread.id)
        return self.thread


class ThreadViewModerationTests(ThreadViewTests):
    def test_pin_thread(self):
        """its possible to pin thread"""
        self.override_acl({'can_pin_threads': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'pin'})
        self.assertEqual(response.status_code, 200)

        # allow for pinning threads
        self.override_acl({'can_pin_threads': 1})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'pin'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.reload_thread().is_pinned)

    def test_unpin_thread(self):
        """its possible to unpin thread"""
        self.thread.is_pinned = True
        self.thread.save()

        self.override_acl({'can_pin_threads': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'unpin'})
        self.assertEqual(response.status_code, 200)

        # allow for pinning threads
        self.override_acl({'can_pin_threads': 1})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'unpin'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.reload_thread().is_pinned)
