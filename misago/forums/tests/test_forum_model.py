from django.test import TestCase
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
