from django.test import TestCase

from .. import THREADS_ROOT_NAME
from ...threads import test
from ...threads.threadtypes import trees_map
from ..models import Category


class CategoryManagerTests(TestCase):
    def test_private_threads(self):
        """private_threads returns private threads category"""
        category = Category.objects.private_threads()

        self.assertEqual(category.special_role, "private_threads")

    def test_root_category(self):
        """root_category returns categories tree root"""
        category = Category.objects.root_category()

        self.assertEqual(category.special_role, "root_category")

    def test_all_categories(self):
        """all_categories returns queryset with categories tree"""
        root = Category.objects.root_category()

        test_category_a = Category(name="Test")
        test_category_a.insert_at(root, position="last-child", save=True)

        test_category_b = Category(name="Test 2")
        test_category_b.insert_at(root, position="last-child", save=True)

        all_categories_from_db = list(Category.objects.all_categories(True))

        self.assertIn(test_category_a, all_categories_from_db)
        self.assertIn(test_category_b, all_categories_from_db)

    def test_get_categories_dict_from_db(self):
        """get_categories_dict_from_db returns dict with categories"""
        test_dict = Category.objects.get_categories_dict_from_db()

        for category in Category.objects.all():
            threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
            if category.tree_id == threads_tree_id:
                self.assertIn(category.id, test_dict)
            else:
                self.assertNotIn(category.id, test_dict)


class CategoryModelTests(TestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.all_categories()[:1][0]

    def create_thread(self):
        return test.post_thread(self.category)

    def assertCategoryIsEmpty(self):
        self.assertIsNone(self.category.last_post_on)
        self.assertIsNone(self.category.last_thread)
        self.assertIsNone(self.category.last_thread_title)
        self.assertIsNone(self.category.last_thread_slug)
        self.assertIsNone(self.category.last_poster)
        self.assertIsNone(self.category.last_poster_name)
        self.assertIsNone(self.category.last_poster_slug)

    def test_synchronize(self):
        """category synchronization works"""
        self.category.synchronize()

        self.assertEqual(self.category.threads, 0)
        self.assertEqual(self.category.posts, 0)

        thread = self.create_thread()
        hidden = self.create_thread()
        unapproved = self.create_thread()

        self.category.synchronize()
        self.assertEqual(self.category.threads, 3)
        self.assertEqual(self.category.posts, 3)
        self.assertEqual(self.category.last_thread, unapproved)

        unapproved.is_unapproved = True
        unapproved.post_set.update(is_unapproved=True)
        unapproved.save()

        self.category.synchronize()
        self.assertEqual(self.category.threads, 2)
        self.assertEqual(self.category.posts, 2)
        self.assertEqual(self.category.last_thread, hidden)

        hidden.is_hidden = True
        hidden.post_set.update(is_hidden=True)
        hidden.save()

        self.category.synchronize()
        self.assertEqual(self.category.threads, 1)
        self.assertEqual(self.category.posts, 1)
        self.assertEqual(self.category.last_thread, thread)

        unapproved.is_unapproved = False
        unapproved.post_set.update(is_unapproved=False)
        unapproved.save()

        self.category.synchronize()
        self.assertEqual(self.category.threads, 2)
        self.assertEqual(self.category.posts, 2)
        self.assertEqual(self.category.last_thread, unapproved)

    def test_delete_content(self):
        """delete_content empties category"""
        for _ in range(10):
            self.create_thread()

        self.category.synchronize()
        self.assertEqual(self.category.threads, 10)
        self.assertEqual(self.category.posts, 10)

        self.category.delete_content()

        self.category.synchronize()
        self.assertEqual(self.category.threads, 0)
        self.assertEqual(self.category.posts, 0)

        self.assertCategoryIsEmpty()

    def test_move_content(self):
        """move_content moves category threads and posts to other category"""
        for _ in range(10):
            self.create_thread()
        self.category.synchronize()

        # we are using category so we don't have to fake another category
        new_category = Category.objects.create(
            lft=7, rght=8, tree_id=2, level=0, name="Archive", slug="archive"
        )
        self.category.move_content(new_category)

        self.category.synchronize()
        new_category.synchronize()

        self.assertEqual(self.category.threads, 0)
        self.assertEqual(self.category.posts, 0)
        self.assertCategoryIsEmpty()
        self.assertEqual(new_category.threads, 10)
        self.assertEqual(new_category.posts, 10)

    def test_set_last_thread(self):
        """set_last_thread changes category's last thread"""
        self.category.synchronize()

        new_thread = self.create_thread()
        self.category.set_last_thread(new_thread)

        self.assertEqual(self.category.last_post_on, new_thread.last_post_on)
        self.assertEqual(self.category.last_thread, new_thread)
        self.assertEqual(self.category.last_thread_title, new_thread.title)
        self.assertEqual(self.category.last_thread_slug, new_thread.slug)
        self.assertEqual(self.category.last_poster, new_thread.last_poster)
        self.assertEqual(self.category.last_poster_name, new_thread.last_poster_name)
        self.assertEqual(self.category.last_poster_slug, new_thread.last_poster_slug)

    def test_empty_last_thread(self):
        """empty_last_thread empties last category thread"""
        self.create_thread()
        self.category.synchronize()
        self.category.empty_last_thread()

        self.assertCategoryIsEmpty()
