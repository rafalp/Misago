from django.core.exceptions import ValidationError
from django.test import TestCase
from misago.forums.models import Forum


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

        all_forums = [root, test_forum_a, test_forum_b]
        no_root = [test_forum_a, test_forum_b]

        self.assertEqual(Forum.objects.all_forums(True).count(),
                         len(all_forums))

        self.assertEqual(Forum.objects.all_forums().count(),
                         len(no_root))

        all_forums_from_db = [f for f in Forum.objects.all_forums(True)]
        no_root_from_db = [f for f in Forum.objects.all_forums()]

        self.assertEqual(len(all_forums_from_db),
                         len(all_forums))

        self.assertEqual(len(no_root),
                         len(no_root_from_db))
