from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import moderation, testutils
from misago.threads.models import Thread, Post, Event


class ThreadsModerationTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadsModerationTests, self).setUp()

        self.category = Category.objects.all_categories()[:1][0]
        self.thread = testutils.post_thread(self.category)

    def tearDown(self):
        super(ThreadsModerationTests, self).tearDown()

    def reload_thread(self):
        self.thread = Thread.objects.get(pk=self.thread.pk)

    def test_announce_thread(self):
        """announce_thread makes announcement"""
        self.assertEqual(self.thread.weight, 0)
        self.assertTrue(moderation.announce_thread(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 2)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertEqual(event.icon, "star")
        self.assertIn("into an announcement.", event.message)

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

    def test_remove_announced_thread_weight(self):
        """unpin_thread defaults announced thread weight"""
        moderation.announce_thread(self.user, self.thread)

        self.assertEqual(self.thread.weight, 2)
        self.assertTrue(moderation.remove_thread_weight(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 0)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("removed thread weight.", event.message)
        self.assertEqual(event.icon, "circle")

    def test_remove_pinned_thread_weight(self):
        """unpin_thread defaults pinned thread weight"""
        moderation.pin_thread(self.user, self.thread)

        self.assertEqual(self.thread.weight, 1)
        self.assertTrue(moderation.remove_thread_weight(self.user, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 0)

        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("removed thread weight.", event.message)
        self.assertEqual(event.icon, "circle")

    def test_remove_weightless_thread_weight(self):
        """remove_thread_weight returns false for already weightless thread"""
        self.assertFalse(
            moderation.remove_thread_weight(self.user, self.thread))
        self.assertEqual(self.thread.weight, 0)

    def test_approve_thread(self):
        """approve_thread approves moderated thread"""
        thread = testutils.post_thread(self.category, is_moderated=True)

        self.assertTrue(thread.is_moderated)
        self.assertTrue(thread.first_post.is_moderated)
        self.assertTrue(moderation.approve_thread(self.user, thread))

        self.reload_thread()
        self.assertFalse(thread.is_moderated)
        self.assertFalse(thread.first_post.is_moderated)
        self.assertTrue(thread.has_events)
        event = thread.event_set.last()

        self.assertIn("approved thread.", event.message)
        self.assertEqual(event.icon, "check")

    def test_move_thread(self):
        """moves_thread moves moderated thread to other category"""
        root_category = Category.objects.root_category()
        Category(
            name='New Category',
            slug='new-category',
        ).insert_at(root_category, position='last-child', save=True)
        new_category = Category.objects.get(slug='new-category')

        self.assertEqual(self.thread.category, self.category)
        self.assertTrue(
            moderation.move_thread(self.user, self.thread, new_category))

        self.reload_thread()
        self.assertEqual(self.thread.category, new_category)
        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("moved thread", event.message)
        self.assertEqual(event.icon, "arrow-right")

    def test_move_thread_to_same_category(self):
        """moves_thread does not move thread to same category it is in"""
        self.assertEqual(self.thread.category, self.category)
        self.assertFalse(
            moderation.move_thread(self.user, self.thread, self.category))

        self.reload_thread()
        self.assertEqual(self.thread.category, self.category)
        self.assertFalse(self.thread.has_events)

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

    def test_hide_thread(self):
        """hide_thread hides thread"""
        self.assertFalse(self.thread.is_hidden)
        self.assertTrue(moderation.hide_thread(self.user, self.thread))

        self.reload_thread()
        self.assertTrue(self.thread.is_hidden)
        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("hidden thread.", event.message)
        self.assertEqual(event.icon, "eye-slash")

    def test_hide_hidden_thread(self):
        """hide_thread fails gracefully for hidden thread"""
        self.thread.is_hidden = True
        self.assertFalse(moderation.hide_thread(self.user, self.thread))

    def test_unhide_thread(self):
        """unhide_thread unhides thread"""
        moderation.hide_thread(self.user, self.thread)
        self.reload_thread()

        self.assertTrue(self.thread.is_hidden)
        self.assertTrue(moderation.unhide_thread(self.user, self.thread))

        self.reload_thread()
        self.assertFalse(self.thread.is_hidden)
        self.assertTrue(self.thread.has_events)
        event = self.thread.event_set.last()

        self.assertIn("made thread visible.", event.message)
        self.assertEqual(event.icon, "eye")

    def test_unhide_visible_thread(self):
        """unhide_thread fails gracefully for visible thread"""
        self.assertFalse(moderation.unhide_thread(self.user, self.thread))

    def test_delete_thread(self):
        """delete_thread deletes thread"""
        self.assertTrue(moderation.delete_thread(self.user, self.thread))
        with self.assertRaises(Thread.DoesNotExist):
            self.reload_thread()
