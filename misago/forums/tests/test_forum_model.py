from django.test import TestCase
from django.utils import timezone

from misago.threads import testutils

from misago.forums.models import FORUMS_TREE_ID, Forum


class ForumManagerTests(TestCase):
    def test_private_threads(self):
        """private_threads returns private threads forum"""
        forum = Forum.objects.private_threads()

        self.assertEqual(forum.special_role, 'private_threads')

    def test_root_category(self):
        """root_category returns forums tree root"""
        forum = Forum.objects.root_category()

        self.assertEqual(forum.special_role, 'root_category')

    def test_all_forums(self):
        """all_forums returns queryset with forums tree"""
        root = Forum.objects.root_category()

        test_forum_a = Forum(name='Test', role='category')
        test_forum_a.insert_at(root,
                               position='last-child',
                               save=True)

        test_forum_b = Forum(name='Test 2', role='category')
        test_forum_b.insert_at(root,
                               position='last-child',
                               save=True)

        all_forums_from_db = [f for f in Forum.objects.all_forums(True)]

        self.assertIn(test_forum_a, all_forums_from_db)
        self.assertIn(test_forum_b, all_forums_from_db)

    def test_get_forums_dict_from_db(self):
        """get_forums_dict_from_db returns dict with forums"""
        test_dict = Forum.objects.get_forums_dict_from_db()

        for forum in Forum.objects.all():
            if forum.tree_id == FORUMS_TREE_ID:
                self.assertIn(forum.id, test_dict)
            else:
                self.assertNotIn(forum.id, test_dict)


class ForumModelTests(TestCase):
    def setUp(self):
        self.forum = Forum.objects.filter(role="forum")[:1][0]

    def create_thread(self):
        datetime = timezone.now()

        thread = testutils.post_thread(self.forum)

        return thread

    def assertForumIsEmpty(self):
        self.assertIsNone(self.forum.last_post_on)
        self.assertIsNone(self.forum.last_thread)
        self.assertIsNone(self.forum.last_thread_title)
        self.assertIsNone(self.forum.last_thread_slug)
        self.assertIsNone(self.forum.last_poster)
        self.assertIsNone(self.forum.last_poster_name)
        self.assertIsNone(self.forum.last_poster_slug)

    def test_synchronize(self):
        """forum synchronization works"""
        self.forum.synchronize()

        self.assertEqual(self.forum.threads, 0)
        self.assertEqual(self.forum.posts, 0)

        thread = self.create_thread()
        hidden = self.create_thread()
        moderated = self.create_thread()

        self.forum.synchronize()
        self.assertEqual(self.forum.threads, 3)
        self.assertEqual(self.forum.posts, 3)
        self.assertEqual(self.forum.last_thread, moderated)

        moderated.is_moderated = True
        moderated.post_set.update(is_moderated=True)
        moderated.save()

        self.forum.synchronize()
        self.assertEqual(self.forum.threads, 2)
        self.assertEqual(self.forum.posts, 2)
        self.assertEqual(self.forum.last_thread, hidden)

        hidden.is_hidden = True
        hidden.post_set.update(is_hidden=True)
        hidden.save()

        self.forum.synchronize()
        self.assertEqual(self.forum.threads, 2)
        self.assertEqual(self.forum.posts, 2)
        self.assertEqual(self.forum.last_thread, hidden)

        moderated.is_moderated = False
        moderated.post_set.update(is_moderated=False)
        moderated.save()

        self.forum.synchronize()
        self.assertEqual(self.forum.threads, 3)
        self.assertEqual(self.forum.posts, 3)
        self.assertEqual(self.forum.last_thread, moderated)

    def test_delete_content(self):
        """delete_content empties forum"""
        for i in xrange(10):
            self.create_thread()

        self.forum.synchronize()
        self.assertEqual(self.forum.threads, 10)
        self.assertEqual(self.forum.posts, 10)

        self.forum.delete_content()

        self.forum.synchronize()
        self.assertEqual(self.forum.threads, 0)
        self.assertEqual(self.forum.posts, 0)

        self.assertForumIsEmpty()

    def test_move_content(self):
        """move_content moves forum threads and posts to other forum"""
        for i in xrange(10):
            self.create_thread()
        self.forum.synchronize()

        # we are using category so we don't have to fake another forum
        new_forum = Forum.objects.filter(role="category")[:1][0]
        self.forum.move_content(new_forum)

        self.forum.synchronize()
        new_forum.synchronize()

        self.assertEqual(self.forum.threads, 0)
        self.assertEqual(self.forum.posts, 0)
        self.assertForumIsEmpty()
        self.assertEqual(new_forum.threads, 10)
        self.assertEqual(new_forum.posts, 10)

    def test_set_last_thread(self):
        """set_last_thread changes forum's last thread"""
        self.forum.synchronize()

        new_thread = self.create_thread()
        self.forum.set_last_thread(new_thread)

        self.assertEqual(self.forum.last_post_on, new_thread.last_post_on)
        self.assertEqual(self.forum.last_thread, new_thread)
        self.assertEqual(self.forum.last_thread_title, new_thread.title)
        self.assertEqual(self.forum.last_thread_slug, new_thread.slug)
        self.assertEqual(self.forum.last_poster, new_thread.last_poster)
        self.assertEqual(self.forum.last_poster_name,
                         new_thread.last_poster_name)
        self.assertEqual(self.forum.last_poster_slug,
                         new_thread.last_poster_slug)

    def test_empty_last_thread(self):
        """empty_last_thread empties last forum thread"""
        self.create_thread()
        self.forum.synchronize()
        self.forum.empty_last_thread()

        self.assertForumIsEmpty()
