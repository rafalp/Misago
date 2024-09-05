import pytest

from ..delete import delete_category
from ..models import Category
from ..mptt import heal_category_trees


@pytest.fixture
def clear_categories(db):
    for category in Category.objects.order_by("-lft"):
        delete_category(category)


def create_category(
    tree_id: int,
    level: int,
    lft: int,
    rght: int,
    parent_id: int | None = None,
) -> Category:
    category = Category.objects.create(
        name="Test",
        slug="test",
        tree_id=0,
        level=0,
        lft=1,
        rght=2,
    )

    Category.objects.filter(id=category.id).update(
        parent_id=parent_id,
        tree_id=tree_id,
        level=level,
        lft=lft,
        rght=rght,
    )

    category.parent_id = parent_id
    category.tree_id = tree_id
    category.level = level
    category.lft = lft
    category.rght = rght

    return category


def repr_mptt(category: Category):
    return (category.tree_id, category.level, category.lft, category.rght)


def test_heal_category_trees_fixes_top_leaf_category(clear_categories):
    category = create_category(0, 10, 12, 0)

    heal_category_trees()

    category.refresh_from_db()
    assert repr_mptt(category) == (0, 0, 1, 2)


def test_heal_category_trees_fixes_separate_trees(clear_categories):
    category = create_category(0, 10, 12, 0)
    other_category = create_category(1, 15, 4, 10)

    heal_category_trees()

    category.refresh_from_db()
    assert repr_mptt(category) == (0, 0, 1, 2)

    other_category.refresh_from_db()
    assert repr_mptt(other_category) == (1, 0, 1, 2)


def test_heal_category_trees_fixes_overlapping_categories(clear_categories):
    category = create_category(0, 10, 5, 10)
    other_category = create_category(0, 15, 10, 15)

    heal_category_trees()

    category.refresh_from_db()
    assert repr_mptt(category) == (0, 0, 1, 2)

    other_category.refresh_from_db()
    assert repr_mptt(other_category) == (0, 0, 3, 4)


def test_heal_category_trees_fixes_parents_children(clear_categories):
    category = create_category(0, 10, 5, 10)
    child_category = create_category(0, 15, 10, 15, category.id)

    heal_category_trees()

    category.refresh_from_db()
    assert repr_mptt(category) == (0, 0, 1, 4)

    child_category.refresh_from_db()
    assert repr_mptt(child_category) == (0, 1, 2, 3)


def test_heal_category_trees_fixes_parents_children_siblings(clear_categories):
    category = create_category(0, 10, 5, 10)
    sibling_category = create_category(0, 15, 10, 15)
    child_category = create_category(0, 15, 10, 15, category.id)

    heal_category_trees()

    category.refresh_from_db()
    assert repr_mptt(category) == (0, 0, 1, 4)

    child_category.refresh_from_db()
    assert repr_mptt(child_category) == (0, 1, 2, 3)

    sibling_category.refresh_from_db()
    assert repr_mptt(sibling_category) == (0, 0, 5, 6)


def test_heal_category_trees_fixes_complex_tree(clear_categories):
    category = create_category(0, 10, 5, 10)
    sibling_category = create_category(0, 15, 10, 15)
    child_category = create_category(0, 15, 10, 15, category.id)
    deep_child_category = create_category(0, 15, 10, 15, child_category.id)
    other_child_category = create_category(0, 15, 11, 18, category.id)
    sibling_child_category = create_category(0, 15, 10, 15, sibling_category.id)

    heal_category_trees()

    category.refresh_from_db()
    assert repr_mptt(category) == (0, 0, 1, 8)

    child_category.refresh_from_db()
    assert repr_mptt(child_category) == (0, 1, 2, 5)

    deep_child_category.refresh_from_db()
    assert repr_mptt(deep_child_category) == (0, 2, 3, 4)

    other_child_category.refresh_from_db()
    assert repr_mptt(other_child_category) == (0, 1, 6, 7)

    sibling_category.refresh_from_db()
    assert repr_mptt(sibling_category) == (0, 0, 9, 12)

    sibling_child_category.refresh_from_db()
    assert repr_mptt(sibling_child_category) == (0, 1, 10, 11)
