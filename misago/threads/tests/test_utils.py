from misago.categories.models import Category
from misago.core.testutils import MisagoTestCase

from .. import testutils
from ..utils import add_categories_to_threads


class AddCategoriesToThreadsTests(MisagoTestCase):
    def setUp(self):
        super(AddCategoriesToThreadsTests, self).setUp()

        self.root = Category.objects.root_category()

        """
        Create categories tree for test cases:

        First category (created by migration)

        Category A
          + Category B
            + Subcategory C
            + Subcategory D

        Category E
          + Subcategory F
        """
        Category(
            name='Category A',
            slug='category-a',
            css_class='showing-category-a',
        ).insert_at(self.root, position='last-child', save=True)
        Category(
            name='Category E',
            slug='category-e',
            css_class='showing-category-e',
        ).insert_at(self.root, position='last-child', save=True)

        self.root = Category.objects.root_category()

        self.category_a = Category.objects.get(slug='category-a')
        Category(
            name='Category B',
            slug='category-b',
            css_class='showing-category-b',
        ).insert_at(self.category_a, position='last-child', save=True)

        self.category_b = Category.objects.get(slug='category-b')
        Category(
            name='Category C',
            slug='category-c',
            css_class='showing-category-c',
        ).insert_at(self.category_b, position='last-child', save=True)
        Category(
            name='Category D',
            slug='category-d',
            css_class='showing-category-d',
        ).insert_at(self.category_b, position='last-child', save=True)

        self.category_c = Category.objects.get(slug='category-c')
        self.category_d = Category.objects.get(slug='category-d')

        self.category_e = Category.objects.get(slug='category-e')
        Category(
            name='Category F',
            slug='category-f',
            css_class='showing-category-f',
        ).insert_at(self.category_e, position='last-child', save=True)

        self.clear_state()

        Category.objects.partial_rebuild(self.root.tree_id)

        self.root = Category.objects.root_category()
        self.category_a = Category.objects.get(slug='category-a')
        self.category_b = Category.objects.get(slug='category-b')
        self.category_c = Category.objects.get(slug='category-c')
        self.category_d = Category.objects.get(slug='category-d')
        self.category_e = Category.objects.get(slug='category-e')
        self.category_f = Category.objects.get(slug='category-f')

        self.categories = list(Category.objects.all_categories(
            include_root=True))

    def test_root_thread_from_root(self):
        """thread in root category is handled"""
        thread = testutils.post_thread(category=self.root)
        add_categories_to_threads(self.root, self.categories, [thread])

        self.assertIsNone(thread.top_category)
        self.assertEqual(thread.category, self.root)

    def test_root_thread_from_elsewhere(self):
        """thread in root category is handled"""
        thread = testutils.post_thread(category=self.root)
        add_categories_to_threads(self.category_e, self.categories, [thread])

        self.assertIsNone(thread.top_category)
        self.assertEqual(thread.category, self.root)

    def test_direct_child_thread_from_parent(self):
        """thread in direct child category is handled"""
        thread = testutils.post_thread(category=self.category_e)
        add_categories_to_threads(self.root, self.categories, [thread])

        self.assertEqual(thread.top_category, self.category_e)
        self.assertEqual(thread.category, self.category_e)

    def test_direct_child_thread_from_elsewhere(self):
        """thread in direct child category is handled"""
        thread = testutils.post_thread(category=self.category_e)
        add_categories_to_threads(self.category_b, self.categories, [thread])

        self.assertEqual(thread.top_category, self.category_e)
        self.assertEqual(thread.category, self.category_e)

    def test_child_thread_from_root(self):
        """thread in child category is handled"""
        thread = testutils.post_thread(category=self.category_d)
        add_categories_to_threads(self.root, self.categories, [thread])

        self.assertEqual(thread.top_category, self.category_a)
        self.assertEqual(thread.category, self.category_d)

    def test_child_thread_from_parent(self):
        """thread in child category is handled"""
        thread = testutils.post_thread(category=self.category_d)
        add_categories_to_threads(self.category_a, self.categories, [thread])

        self.assertEqual(thread.top_category, self.category_b)
        self.assertEqual(thread.category, self.category_d)

    def test_child_thread_from_category(self):
        """thread in child category is handled"""
        thread = testutils.post_thread(category=self.category_d)
        add_categories_to_threads(self.category_d, self.categories, [thread])

        self.assertIsNone(thread.top_category)
        self.assertEqual(thread.category, self.category_d)

    def test_child_thread_from_elsewhere(self):
        """thread in child category is handled"""
        thread = testutils.post_thread(category=self.category_d)
        add_categories_to_threads(self.category_f, self.categories, [thread])

        self.assertEqual(thread.top_category, self.category_a)
        self.assertEqual(thread.category, self.category_d)
