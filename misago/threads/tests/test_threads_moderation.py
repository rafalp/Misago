from misago.categories.models import Category
from misago.threads import moderation, testutils
from misago.threads.models import Thread
from misago.users.testutils import AuthenticatedUserTestCase


class MockRequest(object):
    def __init__(self, user):
        self.user = user
        self.user_ip = '123.14.15.222'


class ThreadsModerationTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadsModerationTests, self).setUp()

        self.request = MockRequest(self.user)
        self.category = Category.objects.all_categories()[:1][0]
        self.thread = testutils.post_thread(self.category)

    def tearDown(self):
        super(ThreadsModerationTests, self).tearDown()

    def reload_thread(self):
        self.thread = Thread.objects.get(pk=self.thread.pk)

    def test_change_thread_title(self):
        """change_thread_title changes thread's title and slug"""
        self.assertTrue(
            moderation.change_thread_title(self.request, self.thread, "New title is here!")
        )

        self.reload_thread()
        self.assertEqual(self.thread.title, "New title is here!")
        self.assertEqual(self.thread.slug, 'new-title-is-here')

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'changed_title')

    def test_pin_globally_thread(self):
        """pin_thread_globally makes thread pinned globally"""
        self.assertEqual(self.thread.weight, 0)
        self.assertTrue(moderation.pin_thread_globally(self.request, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 2)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'pinned_globally')

    def test_pin_globally_invalid_thread(self):
        """
        pin_thread_globally returns false for already globally pinned thread
        """
        self.thread.weight = 2

        self.assertFalse(moderation.pin_thread_globally(self.request, self.thread))
        self.assertEqual(self.thread.weight, 2)

    def test_pin_thread_locally(self):
        """pin_thread_locally makes thread pinned locally"""
        self.assertEqual(self.thread.weight, 0)
        self.assertTrue(moderation.pin_thread_locally(self.request, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 1)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'pinned_locally')

    def test_pin_invalid_thread(self):
        """pin_thread_locally returns false for already locally pinned thread"""
        self.thread.weight = 1

        self.assertFalse(moderation.pin_thread_locally(self.request, self.thread))
        self.assertEqual(self.thread.weight, 1)

    def test_unpin_globally_pinned_thread(self):
        """unpin_thread unpins globally pinned thread"""
        moderation.pin_thread_globally(self.request, self.thread)

        self.assertEqual(self.thread.weight, 2)
        self.assertTrue(moderation.unpin_thread(self.request, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 0)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'unpinned')

    def test_unpin_locally_pinned_thread(self):
        """unpin_thread unpins locally pinned thread"""
        moderation.pin_thread_locally(self.request, self.thread)

        self.assertEqual(self.thread.weight, 1)
        self.assertTrue(moderation.unpin_thread(self.request, self.thread))

        self.reload_thread()
        self.assertEqual(self.thread.weight, 0)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'unpinned')

    def test_unpin_weightless_thread(self):
        """unpin_thread returns false for already weightless thread"""
        self.assertFalse(moderation.unpin_thread(self.request, self.thread))
        self.assertEqual(self.thread.weight, 0)

    def test_approve_thread(self):
        """approve_thread approves unapproved thread"""
        self.thread = testutils.post_thread(self.category, is_unapproved=True)

        self.assertTrue(self.thread.is_unapproved)
        self.assertTrue(self.thread.first_post.is_unapproved)
        self.assertTrue(moderation.approve_thread(self.request, self.thread))

        self.reload_thread()
        self.assertFalse(self.thread.is_unapproved)
        self.assertFalse(self.thread.first_post.is_unapproved)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'approved')

    def test_move_thread(self):
        """moves_thread moves unapproved thread to other category"""
        root_category = Category.objects.root_category()
        Category(
            name='New Category',
            slug='new-category',
        ).insert_at(
            root_category,
            position='last-child',
            save=True,
        )
        new_category = Category.objects.get(slug='new-category')

        self.assertEqual(self.thread.category, self.category)
        self.assertTrue(moderation.move_thread(self.request, self.thread, new_category))

        self.reload_thread()
        self.assertEqual(self.thread.category, new_category)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'moved')

    def test_move_thread_to_same_category(self):
        """moves_thread does not move thread to same category it is in"""
        self.assertEqual(self.thread.category, self.category)
        self.assertFalse(moderation.move_thread(self.request, self.thread, self.category))

        self.reload_thread()
        self.assertEqual(self.thread.category, self.category)

    def test_close_thread(self):
        """close_thread closes thread"""
        self.assertFalse(self.thread.is_closed)
        self.assertTrue(moderation.close_thread(self.request, self.thread))

        self.reload_thread()
        self.assertTrue(self.thread.is_closed)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'closed')

    def test_close_invalid_thread(self):
        """close_thread fails gracefully for opened thread"""
        moderation.close_thread(self.request, self.thread)
        self.reload_thread()

        self.assertTrue(self.thread.is_closed)
        self.assertFalse(moderation.close_thread(self.request, self.thread))

    def test_open_thread(self):
        """open_thread closes thread"""
        moderation.close_thread(self.request, self.thread)
        self.reload_thread()

        self.assertTrue(self.thread.is_closed)
        self.assertTrue(moderation.open_thread(self.request, self.thread))

        self.reload_thread()
        self.assertFalse(self.thread.is_closed)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'opened')

    def test_open_invalid_thread(self):
        """open_thread fails gracefully for opened thread"""
        self.assertFalse(self.thread.is_closed)
        self.assertFalse(moderation.open_thread(self.request, self.thread))

    def test_hide_thread(self):
        """hide_thread hides thread"""
        self.assertFalse(self.thread.is_hidden)
        self.assertTrue(moderation.hide_thread(self.request, self.thread))

        self.reload_thread()
        self.assertTrue(self.thread.is_hidden)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'hid')

    def test_hide_hidden_thread(self):
        """hide_thread fails gracefully for hidden thread"""
        self.thread.is_hidden = True
        self.assertFalse(moderation.hide_thread(self.request, self.thread))

    def test_unhide_thread(self):
        """unhide_thread unhides thread"""
        moderation.hide_thread(self.request, self.thread)
        self.reload_thread()

        self.assertTrue(self.thread.is_hidden)
        self.assertTrue(moderation.unhide_thread(self.request, self.thread))

        self.reload_thread()
        self.assertFalse(self.thread.is_hidden)

        event = self.thread.last_post

        self.assertTrue(event.is_event)
        self.assertEqual(event.event_type, 'unhid')

    def test_unhide_visible_thread(self):
        """unhide_thread fails gracefully for visible thread"""
        self.assertFalse(moderation.unhide_thread(self.request, self.thread))

    def test_delete_thread(self):
        """delete_thread deletes thread"""
        self.assertTrue(moderation.delete_thread(self.request, self.thread))
        with self.assertRaises(Thread.DoesNotExist):
            self.reload_thread()
