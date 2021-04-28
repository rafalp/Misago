import pytest

from ..models import Category
from ..tree import CategoryTree


def category_factory(*, id, left=0, right=0):  # pylint: disable=redefined-builtin
    return Category(
        name="T",
        slug="t",
        color="#000000",
        type=0,
        id=id,
        left=left,
        right=right,
        extra={},
    )


@pytest.fixture
def tree():
    return CategoryTree([])


def tree_to_list(tree):
    tree_list = []
    for node in tree.get_list():
        tree_list.append((node.id, node.parent_id, node.left, node.right, node.depth))
    return tree_list


def test_category_is_added_to_empty_tree(tree):
    node = category_factory(id=1)
    tree.insert_node(node)
    assert tree_to_list(tree) == [(1, None, 1, 2, 0)]


def test_tree_raises_value_error_if_parent_arg_is_used_for_empty_tree(tree):
    with pytest.raises(ValueError):
        tree.insert_node(category_factory(id=1), category_factory(id=2))


def test_tree_raises_value_error_if_parent_arg_is_not_already_present_in_tree(tree):
    tree.insert_node(category_factory(id=1))
    with pytest.raises(ValueError):
        tree.insert_node(category_factory(id=3), category_factory(id=2))


def test_node_is_added_after_previous_one_in_tree(tree):
    tree.insert_node(category_factory(id=1))
    tree.insert_node(category_factory(id=2))
    assert tree_to_list(tree) == [(1, None, 1, 2, 0), (2, None, 3, 4, 0)]


def test_child_node_is_inserted_under_parent_one(tree):
    parent = category_factory(id=1)
    tree.insert_node(parent)
    tree.insert_node(category_factory(id=2), parent)
    assert tree_to_list(tree) == [(1, None, 1, 4, 0), (2, 1, 2, 3, 1)]


def test_next_child_node_is_inserted_after_previous_one(tree):
    parent = category_factory(id=1)
    tree.insert_node(parent)
    tree.insert_node(category_factory(id=2), parent)
    tree.insert_node(category_factory(id=3), parent)
    assert tree_to_list(tree) == [(1, None, 1, 6, 0), (2, 1, 2, 3, 1), (3, 1, 4, 5, 1)]


def test_node_is_added_after_previous_root_node_in_tree(tree):
    parent = category_factory(id=1)
    tree.insert_node(parent)
    tree.insert_node(category_factory(id=2), parent)
    tree.insert_node(category_factory(id=3))
    assert tree_to_list(tree) == [
        (1, None, 1, 4, 0),
        (2, 1, 2, 3, 1),
        (3, None, 5, 6, 0),
    ]


def test_inserting_child_node_updates_parent_siblings(tree):
    parent = category_factory(id=1)
    tree.insert_node(parent)
    tree.insert_node(category_factory(id=2))
    tree.insert_node(category_factory(id=3))
    tree.insert_node(category_factory(id=4), parent)
    assert tree_to_list(tree) == [
        (1, None, 1, 4, 0),
        (4, 1, 2, 3, 1),
        (2, None, 5, 6, 0),
        (3, None, 7, 8, 0),
    ]


def test_category_tree_returns_top_level_category_by_id(categories, category):
    tree = CategoryTree(categories)
    assert tree.get_category(category.id) == category


def test_category_tree_returns_child_category_by_id(categories, child_category):
    tree = CategoryTree(categories)
    assert tree.get_category(child_category.id) == child_category


def test_category_tree_returns_none_if_category_is_not_found(categories, category):
    tree = CategoryTree(categories)
    assert tree.get_category(0) is None
