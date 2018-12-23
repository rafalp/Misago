from django.test import TestCase

from ...categories.models import Category
from ..threadtypes.treesmap import TreesMap

THREAD_TYPE = "misago.threads.threadtypes.thread.Thread"


class TreesMapTests(TestCase):
    def test_load_types(self):
        """TreesMap().load_types() loads types modules"""
        trees_map = TreesMap(None)
        types = trees_map.load_types([THREAD_TYPE])

        self.assertEqual(len(types), 1, "expected to load only one thread type")
        self.assertIn("root_category", types, "invalid thread type was loaded")

    def test_load_trees(self):
        """TreesMap().load_trees() loads trees ids"""
        trees_map = TreesMap(None)
        types = trees_map.load_types([THREAD_TYPE])
        trees = trees_map.load_trees(types)

        tree_id = Category.objects.get(special_role="root_category").tree_id

        self.assertEqual(len(trees), 1, "expected to load only one tree")
        self.assertEqual(
            trees[tree_id].root_name, "root_category", "invalid tree was loaded"
        )

    def test_get_roots(self):
        """TreesMap().get_roots() returns roots to trees dict"""
        trees_map = TreesMap(None)
        types = trees_map.load_types([THREAD_TYPE])
        trees = trees_map.load_trees(types)
        roots = trees_map.get_roots(trees)

        tree_id = Category.objects.get(special_role="root_category").tree_id

        self.assertEqual(len(roots), 1, "expected to load only one root")
        self.assertIn("root_category", roots, "invalid root was loaded")
        self.assertEqual(roots["root_category"], tree_id, "invalid tree_id was loaded")

    def test_load(self):
        """TreesMap().load() populates trees map"""
        trees_map = TreesMap([THREAD_TYPE])

        self.assertFalse(
            trees_map.is_loaded, "trees map should be not loaded by default"
        )

        trees_map.load()

        self.assertTrue(
            trees_map.is_loaded, "trees map should be loaded after call to load()"
        )

        self.assertEqual(len(trees_map.types), 1, "expected to load one type")
        self.assertEqual(len(trees_map.trees), 1, "expected to load one tree")
        self.assertEqual(len(trees_map.roots), 1, "expected to load one root")

        tree_id = Category.objects.get(special_role="root_category").tree_id

        self.assertIn(
            "root_category", trees_map.types, "invalid thread type was loaded"
        )
        self.assertEqual(
            trees_map.trees[tree_id].root_name,
            "root_category",
            "invalid tree was loaded",
        )
        self.assertIn("root_category", trees_map.roots, "invalid root was loaded")

    def test_get_type_for_tree_id(self):
        """TreesMap().get_type_for_tree_id() returns type for valid id"""
        trees_map = TreesMap([THREAD_TYPE])
        trees_map.load()

        tree_id = Category.objects.get(special_role="root_category").tree_id
        thread_type = trees_map.get_type_for_tree_id(tree_id)

        self.assertEqual(
            thread_type.root_name,
            "root_category",
            "returned invalid thread type for given tree id",
        )

        try:
            trees_map.get_type_for_tree_id(tree_id + 1000)
            self.fail("invalid tree id should cause KeyError being raised")
        except KeyError as e:
            self.assertIn(
                "tree id has no type defined",
                str(e),
                "invalid exception message as given",
            )

    def test_get_tree_id_for_root(self):
        """TreesMap().get_tree_id_for_root() returns tree id for valid type name"""
        trees_map = TreesMap([THREAD_TYPE])
        trees_map.load()

        in_db_tree_id = Category.objects.get(special_role="root_category").tree_id
        tree_id = trees_map.get_tree_id_for_root("root_category")

        self.assertEqual(
            tree_id, in_db_tree_id, "root name didn't match one in database"
        )

        try:
            trees_map.get_tree_id_for_root("hurr_durr")
            self.fail("invalid root name should cause KeyError being raised")
        except KeyError as e:
            self.assertIn(
                '"hurr_durr" root has no tree defined',
                str(e),
                "invalid exception message as given",
            )
