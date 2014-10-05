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

    def test_reset_thread(self):
        """reset_thread defaults thread weight"""
        moderation.pin_thread(self.user, self.thread)

        self.assertEqual(self.thread.weight, 1)
        self.assertTrue(moderation.reset_thread(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 0)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("unpinned thread.", event.message)
        self.assertEqual(event.icon, "circle")

    def test_reset_invalid_thread(self):
        """reset_thread returns false for already default thread"""
        self.assertFalse(moderation.reset_thread(self.user, self.thread))
        self.assertEqual(self.thread.weight, 0)

    def test_close_thread(self):
        """close_thread closes thread"""
        self.assertFalse(self.thread.is_closed)
        self.assertTrue(moderation.close_thread(self.user, self.thread))

        self.reload_thread()
        self.assertTrue(self.thread.is_closed)
        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("closed thread.", event.message)
        self.assertEqual(event.icon, "lock")

    def test_close_invalid_thread(self):
        """close_thread fails gracefully for opened thread"""
        moderation.close_thread(self.user, self.thread)
        self.reload_thread()

        self.assertTrue(self.thread.is_closed)
        self.assertFalse(moderation.close_thread(self.user, self.thread))

    def test_open_thread(self):
        """open_thread closes thread"""
        moderation.close_thread(self.user, self.thread)
        self.reload_thread()

        self.assertTrue(self.thread.is_closed)
        self.assertTrue(moderation.open_thread(self.user, self.thread))

        self.reload_thread()
        self.assertFalse(self.thread.is_closed)
        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("opened thread.", event.message)
        self.assertEqual(event.icon, "unlock-alt")

    def test_open_invalid_thread(self):
        """open_thread fails gracefully for opened thread"""
        self.assertFalse(self.thread.is_closed)
        self.assertFalse(moderation.open_thread(self.user, self.thread))
