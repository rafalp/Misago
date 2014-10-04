from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import moderation, testutils
from misago.threads.models import Thread, Post, Event


class ThreadsModerationTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadsModerationTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.thread = testutils.post_thread(self.forum)

    def reload_thread(self):
        self.thread = Thread.objects.get(pk=self.thread.pk)

    def test_announce_thread(self):
        """announce_thread makes thread announcement"""
        self.assertEqual(self.thread.weight, 0)
        self.assertTrue(moderation.announce_thread(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 2)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertEqual(event.icon, "star")
        self.assertIn("changed thread to announcement.", event.message)

    def test_announce_invalid_thread(self):
        """announce_thread returns false for already announced thread"""
        self.thread.weight = 2

        self.assertFalse(moderation.announce_thread(self.user, self.thread))
        self.assertEqual(self.thread.weight, 2)

    def test_pin_thread(self):
        """pin_thread makes thread pinned"""
        self.assertEqual(self.thread.weight, 0)
        self.assertTrue(moderation.pin_thread(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 1)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertEqual(event.icon, "bookmark")
        self.assertIn("pinned thread.", event.message)

    def test_pin_invalid_thread(self):
        """pin_thread returns false for already pinned thread"""
        self.thread.weight = 1

        self.assertFalse(moderation.pin_thread(self.user, self.thread))
        self.assertEqual(self.thread.weight, 1)

    def test_default_thread(self):
        """default_thread defaults thread weight"""
        moderation.pin_thread(self.user, self.thread)

        self.assertEqual(self.thread.weight, 1)
        self.assertTrue(moderation.default_thread(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 0)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("unpinned thread.", event.message)
        self.assertEqual(event.icon, "circle")

    def test_default_invalid_thread(self):
        """default_thread returns false for already default thread"""
        self.assertFalse(moderation.default_thread(self.user, self.thread))
        self.assertEqual(self.thread.weight, 0)
