from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.categories.utils import get_categories_tree, get_category_path
from misago.core import threadstore
from misago.users.testutils import AuthenticatedUserTestCase


class CategoriesUtilsTests(AuthenticatedUserTestCase):
    def setUp(self):
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

        super(CategoriesUtilsTests, self).setUp()
        threadstore.clear()

        self.root = Category.objects.root_category()
        self.first_category = Category.objects.get(slug='first-category')

        Category(
            name='Category A',
            slug='category-a',
        ).insert_at(
            self.root,
            position='last-child',
            save=True,
        )
        Category(
            name='Category E',
            slug='category-e',
        ).insert_at(
            self.root,
            position='last-child',
            save=True,
        )

        self.category_a = Category.objects.get(slug='category-a')

        Category(
            name='Category B',
            slug='category-b',
        ).insert_at(
            self.category_a,
            position='last-child',
            save=True,
        )

        self.category_b = Category.objects.get(slug='category-b')

        Category(
            name='Subcategory C',
            slug='subcategory-c',
        ).insert_at(
            self.category_b,
            position='last-child',
            save=True,
        )
        Category(
            name='Subcategory D',
            slug='subcategory-d',
        ).insert_at(
            self.category_b,
            position='last-child',
            save=True,
        )

        self.category_e = Category.objects.get(slug='category-e')
        Category(
            name='Subcategory F',
            slug='subcategory-f',
        ).insert_at(
            self.category_e,
            position='last-child',
            save=True,
        )

        categories_acl = {'categories': {}, 'visible_categories': []}
        for category in Category.objects.all_categories():
            categories_acl['visible_categories'].append(category.pk)
            categories_acl['categories'][category.pk] = {'can_see': 1, 'can_browse': 1}
        override_acl(self.user, categories_acl)

    def test_root_categories_tree_no_parent(self):
        """get_categories_tree returns all children of root nodes"""
        categories_tree = get_categories_tree(self.user)
        self.assertEqual(len(categories_tree), 3)

        self.assertEqual(categories_tree[0], Category.objects.get(slug='first-category'))
        self.assertEqual(categories_tree[1], Category.objects.get(slug='category-a'))
        self.assertEqual(categories_tree[2], Category.objects.get(slug='category-e'))

    def test_root_categories_tree_with_parent(self):
        """get_categories_tree returns all children of given node"""
        categories_tree = get_categories_tree(self.user, self.category_a)
        self.assertEqual(len(categories_tree), 1)
        self.assertEqual(categories_tree[0], Category.objects.get(slug='category-b'))

    def test_root_categories_tree_with_leaf(self):
        """get_categories_tree returns all children of given node"""
        categories_tree = get_categories_tree(
            self.user, Category.objects.get(slug='subcategory-f')
        )
        self.assertEqual(len(categories_tree), 0)

    def test_get_category_path(self):
        """get_categories_tree returns all children of root nodes"""
        for node in get_categories_tree(self.user):
            parent_nodes = len(get_category_path(node))
            self.assertEqual(parent_nodes, node.level)
