from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from ...acl import ACL_CACHE
from ...cache.test import assert_invalidates_cache
from ..management.commands import fixcategoriestree
from ..models import Category


def run_command():
    """Run the management command"""
    command = fixcategoriestree.Command()
    out = StringIO()
    call_command(command, stdout=out)


class FixCategoriesTreeTests(TestCase):
    """
    The purpose is the verify that the management command
    fixes the lft/rght values of the thread category tree.
    """

    def setUp(self):
        Category.objects.create(
            name="Test", slug="test", parent=Category.objects.root_category()
        )
        self.fetch_categories()

    def assertValidTree(self, expected_tree):
        root = Category.objects.root_category()
        queryset = Category.objects.filter(tree_id=root.tree_id).order_by("lft")

        current_tree = []
        for category in queryset:
            current_tree.append(
                (category, category.get_level(), category.lft, category.rght)
            )

        for i, category in enumerate(expected_tree):
            _category = current_tree[i]
            if category[0] != _category[0]:
                self.fail(
                    ("expected category at index #%s to be %s, " "found %s instead")
                    % (i, category[0], _category[0])
                )
            if category[1] != _category[1]:
                self.fail(
                    ("expected level at index #%s to be %s, " "found %s instead")
                    % (i, category[1], _category[1])
                )
            if category[2] != _category[2]:
                self.fail(
                    ("expected lft at index #%s to be %s, " "found %s instead")
                    % (i, category[2], _category[2])
                )
            if category[3] != _category[3]:
                self.fail(
                    ("expected lft at index #%s to be %s, " "found %s instead")
                    % (i, category[3], _category[3])
                )

    def fetch_categories(self):
        """gets a fresh version from the database"""
        self.root = Category.objects.root_category()
        self.first_category = Category.objects.get(slug="first-category")
        self.test_category = Category.objects.get(slug="test")

    def test_fix_categories_tree_unaffected(self):
        """Command should not affect a healthy three"""
        tree_id = self.root.tree_id
        run_command()

        self.fetch_categories()

        self.assertValidTree(
            [
                (self.root, 0, 1, 6),
                (self.first_category, 1, 2, 3),
                (self.test_category, 1, 4, 5),
            ]
        )

        self.assertEqual(self.root.tree_id, tree_id, msg="tree_id changed by command")

    def test_fix_categories_tree_affected(self):
        """Command should fix a broken tree"""
        # Root node with too narrow lft/rght range
        Category.objects.filter(id=self.root.id).update(lft=1, rght=4)
        # Make conflicting/identical lft/rght range
        Category.objects.filter(id=self.test_category.id).update(lft=2, rght=3)

        run_command()
        self.fetch_categories()

        self.assertValidTree(
            [
                (self.root, 0, 1, 6),
                (self.test_category, 1, 2, 3),
                (self.first_category, 1, 4, 5),
            ]
        )

    def test_fixing_categories_tree_invalidates_acl_cache(self):
        with assert_invalidates_cache(ACL_CACHE):
            run_command()
