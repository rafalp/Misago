from misago.categories.models import Category
from misago.threads import moderation, testutils
from misago.threads.models import Post, Thread
from misago.users.testutils import AuthenticatedUserTestCase


class PostsModerationTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(PostsModerationTests, self).setUp()

        self.category = Category.objects.all_categories()[:1][0]
        self.thread = testutils.post_thread(self.category)
        self.post = testutils.reply_thread(self.thread)

    def reload_thread(self):
        self.thread = Thread.objects.get(pk=self.thread.pk)

    def reload_post(self):
        self.post = Post.objects.get(pk=self.post.pk)

    def test_hide_original_post(self):
        """hide_post fails for first post in thread"""
        with self.assertRaises(moderation.ModerationError):
            moderation.hide_post(self.user, self.thread.first_post)

    def test_protect_post(self):
        """protect_post protects post"""
        self.assertFalse(self.post.is_protected)
        self.assertTrue(moderation.protect_post(self.user, self.post))

        self.reload_post()
        self.assertTrue(self.post.is_protected)

    def test_protect_protected_post(self):
        """protect_post fails to protect protected post gracefully"""
        self.post.is_protected = True
        self.assertFalse(moderation.protect_post(self.user, self.post))

    def test_unprotect_post(self):
        """unprotect_post releases post protection"""
        self.post.is_protected = True
        self.assertTrue(moderation.unprotect_post(self.user, self.post))

        self.reload_post()
        self.assertFalse(self.post.is_protected)

    def test_unprotect_protected_post(self):
        """unprotect_post fails to unprotect unprotected post gracefully"""
        self.assertFalse(moderation.unprotect_post(self.user, self.post))

    def test_hide_post(self):
        """hide_post hides post"""
        self.assertFalse(self.post.is_hidden)
        self.assertTrue(moderation.hide_post(self.user, self.post))

        self.reload_post()
        self.assertTrue(self.post.is_hidden)
        self.assertEqual(self.post.hidden_by, self.user)
        self.assertEqual(self.post.hidden_by_name, self.user.username)
        self.assertEqual(self.post.hidden_by_slug, self.user.slug)
        self.assertIsNotNone(self.post.hidden_on)

    def test_hide_hidden_post(self):
        """hide_post fails to hide hidden post gracefully"""
        self.post.is_hidden = True
        self.assertFalse(moderation.hide_post(self.user, self.post))

    def test_unhide_original_post(self):
        """unhide_post fails for first post in thread"""
        with self.assertRaises(moderation.ModerationError):
            moderation.unhide_post(self.user, self.thread.first_post)

    def test_unhide_post(self):
        """unhide_post reveals post"""
        self.post.is_hidden = True

        self.assertTrue(self.post.is_hidden)
        self.assertTrue(moderation.unhide_post(self.user, self.post))

        self.reload_post()
        self.assertFalse(self.post.is_hidden)

    def test_unhide_visible_post(self):
        """unhide_post fails to reveal visible post gracefully"""
        self.assertFalse(moderation.unhide_post(self.user, self.post))

    def test_delete_original_post(self):
        """delete_post fails for first post in thread"""
        with self.assertRaises(moderation.ModerationError):
            moderation.delete_post(self.user, self.thread.first_post)

    def test_delete_post(self):
        """delete_post deletes thread post"""
        self.assertTrue(moderation.delete_post(self.user, self.post))
        with self.assertRaises(Post.DoesNotExist):
            self.reload_post()

        self.thread.synchronize()
        self.assertEqual(self.thread.replies, 0)
