import pytest

from ..delete import delete_category
from ..models import Category


def test_delete_category_deletes_category(default_category):
    delete_category(default_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()


def test_delete_category_updates_category_tree(root_category, default_category):
    Category.objects.filter(id=root_category.id).update(lft=1, rght=8)
    root_category.refresh_from_db()

    previous_category = Category.objects.create(
        name="Previous Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=2,
        rght=3,
    )

    Category.objects.filter(id=default_category.id).update(lft=4, rght=5)
    default_category.refresh_from_db()

    next_category = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=6,
        rght=7,
    )

    delete_category(default_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    root_category.refresh_from_db()
    assert root_category.parent_id is None
    assert root_category.level == 0
    assert root_category.lft == 1
    assert root_category.rght == 6

    previous_category.refresh_from_db()
    assert previous_category.parent_id == root_category.id
    assert previous_category.level == 1
    assert previous_category.lft == 2
    assert previous_category.rght == 3

    next_category.refresh_from_db()
    assert next_category.parent_id == root_category.id
    assert next_category.level == 1
    assert next_category.lft == 4
    assert next_category.rght == 5


def test_delete_category_deletes_category_child(root_category, default_category):
    Category.objects.filter(id=root_category.id).update(lft=1, rght=10)
    root_category.refresh_from_db()

    previous_category = Category.objects.create(
        name="Previous Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=2,
        rght=3,
    )

    Category.objects.filter(id=default_category.id).update(lft=4, rght=7)
    default_category.refresh_from_db()

    child_category = Category.objects.create(
        name="Child Category",
        slug="category",
        parent=default_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=5,
        rght=6,
    )

    next_category = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=8,
        rght=9,
    )

    delete_category(default_category, move_children_to=None)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    with pytest.raises(Category.DoesNotExist):
        child_category.refresh_from_db()

    root_category.refresh_from_db()
    assert root_category.parent_id is None
    assert root_category.level == 0
    assert root_category.lft == 1
    assert root_category.rght == 6

    previous_category.refresh_from_db()
    assert previous_category.parent_id == root_category.id
    assert previous_category.level == 1
    assert previous_category.lft == 2
    assert previous_category.rght == 3

    next_category.refresh_from_db()
    assert next_category.parent_id == root_category.id
    assert next_category.level == 1
    assert next_category.lft == 4
    assert next_category.rght == 5


def test_delete_category_moves_category_child_to_end_of_root(
    root_category, default_category
):
    Category.objects.filter(id=root_category.id).update(lft=1, rght=10)
    root_category.refresh_from_db()

    previous_category = Category.objects.create(
        name="Previous Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=2,
        rght=3,
    )

    Category.objects.filter(id=default_category.id).update(lft=4, rght=7)
    default_category.refresh_from_db()

    child_category = Category.objects.create(
        name="Child Category",
        slug="category",
        parent=default_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=5,
        rght=6,
    )

    next_category = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=8,
        rght=9,
    )

    delete_category(default_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    root_category.refresh_from_db()
    assert root_category.parent_id is None
    assert root_category.level == 0
    assert root_category.lft == 1
    assert root_category.rght == 8

    previous_category.refresh_from_db()
    assert previous_category.parent_id == root_category.id
    assert previous_category.level == 1
    assert previous_category.lft == 2
    assert previous_category.rght == 3

    next_category.refresh_from_db()
    assert next_category.parent_id == root_category.id
    assert next_category.level == 1
    assert next_category.lft == 4
    assert next_category.rght == 5

    child_category.refresh_from_db()
    assert child_category.parent_id == root_category.id
    assert child_category.level == 1
    assert child_category.lft == 6
    assert child_category.rght == 7


def test_delete_category_moves_category_child_to_next_category(
    root_category, default_category
):
    Category.objects.filter(id=root_category.id).update(lft=1, rght=12)
    root_category.refresh_from_db()

    previous_category = Category.objects.create(
        name="Previous Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=2,
        rght=3,
    )

    Category.objects.filter(id=default_category.id).update(lft=4, rght=7)
    default_category.refresh_from_db()

    child_category = Category.objects.create(
        name="Child Category",
        slug="category",
        parent=default_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=5,
        rght=6,
    )

    next_category = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=8,
        rght=9,
    )

    last_category = Category.objects.create(
        name="Last Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=10,
        rght=11,
    )

    delete_category(default_category, move_children_to=next_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    root_category.refresh_from_db()
    assert root_category.parent_id is None
    assert root_category.level == 0
    assert root_category.lft == 1
    assert root_category.rght == 10

    previous_category.refresh_from_db()
    assert previous_category.parent_id == root_category.id
    assert previous_category.level == 1
    assert previous_category.lft == 2
    assert previous_category.rght == 3

    next_category.refresh_from_db()
    assert next_category.parent_id == root_category.id
    assert next_category.level == 1
    assert next_category.lft == 4
    assert next_category.rght == 7

    child_category.refresh_from_db()
    assert child_category.parent_id == next_category.id
    assert child_category.level == 2
    assert child_category.lft == 5
    assert child_category.rght == 6

    last_category.refresh_from_db()
    assert last_category.parent_id == root_category.id
    assert last_category.level == 1
    assert last_category.lft == 8
    assert last_category.rght == 9


def test_delete_category_moves_category_child_to_next_category_child(
    root_category, default_category
):
    Category.objects.filter(id=root_category.id).update(lft=1, rght=14)
    root_category.refresh_from_db()

    previous_category = Category.objects.create(
        name="Previous Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=2,
        rght=3,
    )

    Category.objects.filter(id=default_category.id).update(lft=4, rght=7)
    default_category.refresh_from_db()

    child_category = Category.objects.create(
        name="Child Category",
        slug="category",
        parent=default_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=5,
        rght=6,
    )

    next_category = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=8,
        rght=11,
    )

    next_category_child = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=next_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=9,
        rght=10,
    )

    last_category = Category.objects.create(
        name="Last Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=12,
        rght=13,
    )

    delete_category(default_category, move_children_to=next_category_child)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    root_category.refresh_from_db()
    assert root_category.parent_id is None
    assert root_category.level == 0
    assert root_category.lft == 1
    assert root_category.rght == 12

    previous_category.refresh_from_db()
    assert previous_category.parent_id == root_category.id
    assert previous_category.level == 1
    assert previous_category.lft == 2
    assert previous_category.rght == 3

    next_category.refresh_from_db()
    assert next_category.parent_id == root_category.id
    assert next_category.level == 1
    assert next_category.lft == 4
    assert next_category.rght == 9

    next_category_child.refresh_from_db()
    assert next_category_child.parent_id == next_category.id
    assert next_category_child.level == 2
    assert next_category_child.lft == 5
    assert next_category_child.rght == 8

    child_category.refresh_from_db()
    assert child_category.parent_id == next_category_child.id
    assert child_category.level == 3
    assert child_category.lft == 6
    assert child_category.rght == 7

    last_category.refresh_from_db()
    assert last_category.parent_id == root_category.id
    assert last_category.level == 1
    assert last_category.lft == 10
    assert last_category.rght == 11


def test_delete_category_deletes_category_child_with_descendants(
    root_category, default_category
):
    Category.objects.filter(id=root_category.id).update(lft=1, rght=18)
    root_category.refresh_from_db()

    previous_category = Category.objects.create(
        name="Previous Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=2,
        rght=3,
    )

    Category.objects.filter(id=default_category.id).update(lft=4, rght=11)
    default_category.refresh_from_db()

    child_category = Category.objects.create(
        name="Child Category",
        slug="category",
        parent=default_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=5,
        rght=10,
    )

    first_descendant = Category.objects.create(
        name="First Descendant",
        slug="category",
        parent=child_category,
        tree_id=root_category.tree_id,
        level=3,
        lft=6,
        rght=7,
    )

    second_descendant = Category.objects.create(
        name="First Descendant",
        slug="category",
        parent=child_category,
        tree_id=root_category.tree_id,
        level=3,
        lft=8,
        rght=9,
    )

    next_category = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=12,
        rght=15,
    )

    next_category_child = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=next_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=13,
        rght=14,
    )

    last_category = Category.objects.create(
        name="Last Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=16,
        rght=17,
    )

    delete_category(default_category, move_children_to=None)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    with pytest.raises(Category.DoesNotExist):
        child_category.refresh_from_db()

    with pytest.raises(Category.DoesNotExist):
        first_descendant.refresh_from_db()

    with pytest.raises(Category.DoesNotExist):
        second_descendant.refresh_from_db()

    root_category.refresh_from_db()
    assert root_category.parent_id is None
    assert root_category.level == 0
    assert root_category.lft == 1
    assert root_category.rght == 10

    previous_category.refresh_from_db()
    assert previous_category.parent_id == root_category.id
    assert previous_category.level == 1
    assert previous_category.lft == 2
    assert previous_category.rght == 3

    next_category.refresh_from_db()
    assert next_category.parent_id == root_category.id
    assert next_category.level == 1
    assert next_category.lft == 4
    assert next_category.rght == 7

    next_category_child.refresh_from_db()
    assert next_category_child.parent_id == next_category.id
    assert next_category_child.level == 2
    assert next_category_child.lft == 5
    assert next_category_child.rght == 6

    last_category.refresh_from_db()
    assert last_category.parent_id == root_category.id
    assert last_category.level == 1
    assert last_category.lft == 8
    assert last_category.rght == 9


def test_delete_category_moves_category_child_with_descendants_to_end_of_root(
    root_category, default_category
):
    Category.objects.filter(id=root_category.id).update(lft=1, rght=18)
    root_category.refresh_from_db()

    previous_category = Category.objects.create(
        name="Previous Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=2,
        rght=3,
    )

    Category.objects.filter(id=default_category.id).update(lft=4, rght=11)
    default_category.refresh_from_db()

    child_category = Category.objects.create(
        name="Child Category",
        slug="category",
        parent=default_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=5,
        rght=10,
    )

    first_descendant = Category.objects.create(
        name="First Descendant",
        slug="category",
        parent=child_category,
        tree_id=root_category.tree_id,
        level=3,
        lft=6,
        rght=7,
    )

    second_descendant = Category.objects.create(
        name="First Descendant",
        slug="category",
        parent=child_category,
        tree_id=root_category.tree_id,
        level=3,
        lft=8,
        rght=9,
    )

    next_category = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=12,
        rght=15,
    )

    next_category_child = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=next_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=13,
        rght=14,
    )

    last_category = Category.objects.create(
        name="Last Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=16,
        rght=17,
    )

    delete_category(default_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    root_category.refresh_from_db()
    assert root_category.parent_id is None
    assert root_category.level == 0
    assert root_category.lft == 1
    assert root_category.rght == 16

    previous_category.refresh_from_db()
    assert previous_category.parent_id == root_category.id
    assert previous_category.level == 1
    assert previous_category.lft == 2
    assert previous_category.rght == 3

    next_category.refresh_from_db()
    assert next_category.parent_id == root_category.id
    assert next_category.level == 1
    assert next_category.lft == 4
    assert next_category.rght == 7

    next_category_child.refresh_from_db()
    assert next_category_child.parent_id == next_category.id
    assert next_category_child.level == 2
    assert next_category_child.lft == 5
    assert next_category_child.rght == 6

    last_category.refresh_from_db()
    assert last_category.parent_id == root_category.id
    assert last_category.level == 1
    assert last_category.lft == 8
    assert last_category.rght == 9

    child_category.refresh_from_db()
    assert child_category.parent_id == root_category.id
    assert child_category.level == 1
    assert child_category.lft == 10
    assert child_category.rght == 15

    first_descendant.refresh_from_db()
    assert first_descendant.parent_id == child_category.id
    assert first_descendant.level == 2
    assert first_descendant.lft == 11
    assert first_descendant.rght == 12

    second_descendant.refresh_from_db()
    assert second_descendant.parent_id == child_category.id
    assert second_descendant.level == 2
    assert second_descendant.lft == 13
    assert second_descendant.rght == 14


def test_delete_category_moves_category_child_with_descendants_under_previous_category(
    root_category, default_category
):
    Category.objects.filter(id=root_category.id).update(lft=1, rght=18)
    root_category.refresh_from_db()

    previous_category = Category.objects.create(
        name="Previous Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=2,
        rght=3,
    )

    Category.objects.filter(id=default_category.id).update(lft=4, rght=11)
    default_category.refresh_from_db()

    child_category = Category.objects.create(
        name="Child Category",
        slug="category",
        parent=default_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=5,
        rght=10,
    )

    first_descendant = Category.objects.create(
        name="First Descendant",
        slug="category",
        parent=child_category,
        tree_id=root_category.tree_id,
        level=3,
        lft=6,
        rght=7,
    )

    second_descendant = Category.objects.create(
        name="First Descendant",
        slug="category",
        parent=child_category,
        tree_id=root_category.tree_id,
        level=3,
        lft=8,
        rght=9,
    )

    next_category = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=12,
        rght=15,
    )

    next_category_child = Category.objects.create(
        name="Next Category",
        slug="category",
        parent=next_category,
        tree_id=root_category.tree_id,
        level=2,
        lft=13,
        rght=14,
    )

    last_category = Category.objects.create(
        name="Last Category",
        slug="category",
        parent=root_category,
        tree_id=root_category.tree_id,
        level=1,
        lft=16,
        rght=17,
    )

    delete_category(default_category, move_children_to=previous_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    root_category.refresh_from_db()
    assert root_category.parent_id is None
    assert root_category.level == 0
    assert root_category.lft == 1
    assert root_category.rght == 16

    previous_category.refresh_from_db()
    assert previous_category.parent_id == root_category.id
    assert previous_category.level == 1
    assert previous_category.lft == 2
    assert previous_category.rght == 9

    child_category.refresh_from_db()
    assert child_category.parent_id == previous_category.id
    assert child_category.level == 2
    assert child_category.lft == 3
    assert child_category.rght == 8

    first_descendant.refresh_from_db()
    assert first_descendant.parent_id == child_category.id
    assert first_descendant.level == 3
    assert first_descendant.lft == 4
    assert first_descendant.rght == 5

    second_descendant.refresh_from_db()
    assert second_descendant.parent_id == child_category.id
    assert second_descendant.level == 3
    assert second_descendant.lft == 6
    assert second_descendant.rght == 7

    next_category.refresh_from_db()
    assert next_category.parent_id == root_category.id
    assert next_category.level == 1
    assert next_category.lft == 10
    assert next_category.rght == 13

    next_category_child.refresh_from_db()
    assert next_category_child.parent_id == next_category.id
    assert next_category_child.level == 2
    assert next_category_child.lft == 11
    assert next_category_child.rght == 12

    last_category.refresh_from_db()
    assert last_category.parent_id == root_category.id
    assert last_category.level == 1
    assert last_category.lft == 14
    assert last_category.rght == 15
