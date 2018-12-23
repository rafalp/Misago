from ...acl.useracl import get_user_acl
from ...conftest import get_cache_versions
from ...users.test import AuthenticatedUserTestCase
from ..models import Category
from ..utils import get_categories_tree, get_category_path

cache_versions = get_cache_versions()


def get_patched_user_acl(user):
    user_acl = get_user_acl(user, cache_versions)
    categories_acl = {"categories": {}, "visible_categories": []}
    for category in Category.objects.all_categories():
        categories_acl["visible_categories"].append(category.id)
        categories_acl["categories"][category.id] = {"can_see": 1, "can_browse": 1}
    user_acl.update(categories_acl)
    return user_acl


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
        super().setUp()

        self.root = Category.objects.root_category()
        self.first_category = Category.objects.get(slug="first-category")

        Category(name="Category A", slug="category-a").insert_at(
            self.root, position="last-child", save=True
        )
        Category(name="Category E", slug="category-e").insert_at(
            self.root, position="last-child", save=True
        )

        self.category_a = Category.objects.get(slug="category-a")

        Category(name="Category B", slug="category-b").insert_at(
            self.category_a, position="last-child", save=True
        )

        self.category_b = Category.objects.get(slug="category-b")

        Category(name="Subcategory C", slug="subcategory-c").insert_at(
            self.category_b, position="last-child", save=True
        )
        Category(name="Subcategory D", slug="subcategory-d").insert_at(
            self.category_b, position="last-child", save=True
        )

        self.category_e = Category.objects.get(slug="category-e")
        Category(name="Subcategory F", slug="subcategory-f").insert_at(
            self.category_e, position="last-child", save=True
        )

        self.user_acl = get_patched_user_acl(self.user)

    def test_root_categories_tree_no_parent(self):
        """get_categories_tree returns all children of root nodes"""
        categories_tree = get_categories_tree(self.user, self.user_acl)
        self.assertEqual(len(categories_tree), 3)

        self.assertEqual(
            categories_tree[0], Category.objects.get(slug="first-category")
        )
        self.assertEqual(categories_tree[1], Category.objects.get(slug="category-a"))
        self.assertEqual(categories_tree[2], Category.objects.get(slug="category-e"))

    def test_root_categories_tree_with_parent(self):
        """get_categories_tree returns all children of given node"""
        categories_tree = get_categories_tree(self.user, self.user_acl, self.category_a)
        self.assertEqual(len(categories_tree), 1)
        self.assertEqual(categories_tree[0], Category.objects.get(slug="category-b"))

    def test_root_categories_tree_with_leaf(self):
        """get_categories_tree returns all children of given node"""
        categories_tree = get_categories_tree(
            self.user, self.user_acl, Category.objects.get(slug="subcategory-f")
        )
        self.assertEqual(len(categories_tree), 0)

    def test_get_category_path(self):
        """get_categories_tree returns all children of root nodes"""
        for node in get_categories_tree(self.user, self.user_acl):
            parent_nodes = len(get_category_path(node))
            self.assertEqual(parent_nodes, node.level)
