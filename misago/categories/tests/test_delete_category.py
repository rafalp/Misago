import pytest

from ...test import CategoryRelationsFactory
from ..delete import delete_category
from ..models import Category
from ..mptt import heal_category_trees


def test_delete_category_raises_value_error_if_contents_will_be_moved_to_deleted_category(
    default_category,
):
    with pytest.raises(ValueError) as exc_info:
        delete_category(default_category, move_contents_to=default_category)

    assert str(exc_info.value) == "Category from 'move_contents_to' will be deleted."


def test_delete_category_raises_value_error_if_contents_will_be_moved_to_deleted_child_category(
    default_category,
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    default_category.refresh_from_db()

    with pytest.raises(ValueError) as exc_info:
        delete_category(
            default_category,
            move_children_to=None,
            move_contents_to=child_category,
        )

    assert str(exc_info.value) == "Category from 'move_contents_to' will be deleted."


def test_delete_category_raises_value_error_if_child_categories_will_be_moved_to_deleted_category(
    default_category,
):
    with pytest.raises(ValueError) as exc_info:
        delete_category(default_category, move_children_to=default_category)

    assert str(exc_info.value) == "Category from 'move_children_to' will be deleted."


def test_delete_category_raises_value_error_if_child_categories_will_be_moved_to_deleted_child_category(
    default_category,
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    default_category.refresh_from_db()

    with pytest.raises(ValueError) as exc_info:
        delete_category(default_category, move_children_to=child_category)

    assert str(exc_info.value) == "Category from 'move_children_to' will be deleted."


def test_delete_category_deletes_category(default_category):
    delete_category(default_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()


def test_delete_category_deletes_category_contents(
    user, other_user, members_group, default_category
):
    category_contents = CategoryRelationsFactory(
        category=default_category,
        user=user,
        other_user=other_user,
        group=members_group,
    )

    delete_category(default_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    category_contents.assert_relations_are_deleted()


def test_delete_category_deletes_child_category_contents(
    user, other_user, members_group, default_category
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    category_contents = CategoryRelationsFactory(
        category=child_category,
        user=user,
        other_user=other_user,
        group=members_group,
    )

    delete_category(default_category, move_children_to=None)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    with pytest.raises(Category.DoesNotExist):
        child_category.refresh_from_db()

    category_contents.assert_relations_are_deleted()


def test_delete_category_moves_category_contents(
    user, other_user, members_group, default_category, sibling_category
):
    category_contents = CategoryRelationsFactory(
        category=default_category,
        user=user,
        other_user=other_user,
        group=members_group,
    )

    delete_category(default_category, move_contents_to=sibling_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    category_contents.assert_relations_are_moved(sibling_category)


def test_delete_category_moves_deleted_child_category_contents(
    user, other_user, members_group, default_category, sibling_category
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    category_contents = CategoryRelationsFactory(
        category=child_category,
        user=user,
        other_user=other_user,
        group=members_group,
    )

    delete_category(
        default_category,
        move_children_to=None,
        move_contents_to=sibling_category,
    )

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    with pytest.raises(Category.DoesNotExist):
        child_category.refresh_from_db()

    category_contents.assert_relations_are_moved(sibling_category)


# A list of parametrized test params for category deletion
DELETE_CATEGORY_TEST_CASES = {
    "case-1": (
        {
            0: None,
            1: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 2),
        ],
    ),
    "case-2": (
        {
            0: None,
            1: 0,
            2: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 4),
            (2, 0, 1, 2, 3),
        ],
    ),
    "case-3": (
        {
            0: None,
            1: 0,
            2: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 4),
            (1, 0, 1, 2, 3),
        ],
    ),
    "case-4": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 6),
            (2, 0, 1, 2, 3),
            (3, 0, 1, 4, 5),
        ],
    ),
    "case-5": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (3, 0, 1, 4, 5),
        ],
    ),
    "case-6": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 0,
        },
        3,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (2, 0, 1, 4, 5),
        ],
    ),
    "case-7": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 4),
            (3, 0, 1, 2, 3),
        ],
    ),
    "case-8": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
        },
        1,
        True,
        [
            (0, None, 0, 1, 6),
            (3, 0, 1, 2, 3),
            (2, 0, 1, 4, 5),
        ],
    ),
    "case-9": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
        },
        1,
        3,
        [
            (0, None, 0, 1, 6),
            (3, 0, 1, 2, 5),
            (2, 3, 2, 3, 4),
        ],
    ),
    "case-10": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
            4: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 6),
            (3, 0, 1, 2, 3),
            (4, 0, 1, 4, 5),
        ],
    ),
    "case-11": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
            4: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (3, 0, 1, 4, 5),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-12": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
            4: 0,
        },
        3,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 5),
            (2, 1, 2, 3, 4),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-13": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
            4: 0,
        },
        4,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 5),
            (2, 1, 2, 3, 4),
            (3, 0, 1, 6, 7),
        ],
    ),
    "case-14": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 2,
            4: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 8),
            (2, 0, 1, 2, 5),
            (3, 2, 2, 3, 4),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-15": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 2,
            4: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (4, 0, 1, 4, 5),
        ],
    ),
    "case-16": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 2,
            4: 0,
        },
        3,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (2, 0, 1, 4, 5),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-17": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 2,
            4: 0,
        },
        4,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (2, 0, 1, 4, 7),
            (3, 2, 2, 5, 6),
        ],
    ),
    "case-18": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (4, 0, 1, 4, 5),
        ],
    ),
    "case-19": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 0,
        },
        2,
        True,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (4, 0, 1, 4, 5),
            (3, 0, 1, 6, 7),
        ],
    ),
    "case-20": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 0,
        },
        2,
        1,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 5),
            (3, 1, 2, 3, 4),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-21": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 0,
        },
        2,
        4,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (4, 0, 1, 4, 7),
            (3, 4, 2, 5, 6),
        ],
    ),
    "case-22": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (5, 0, 1, 4, 5),
        ],
    ),
    "case-23": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 0,
        },
        2,
        True,
        [
            (0, None, 0, 1, 10),
            (1, 0, 1, 2, 3),
            (5, 0, 1, 4, 5),
            (3, 0, 1, 6, 9),
            (4, 3, 2, 7, 8),
        ],
    ),
    "case-24": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 0,
        },
        2,
        1,
        [
            (0, None, 0, 1, 10),
            (1, 0, 1, 2, 7),
            (3, 1, 2, 3, 6),
            (4, 3, 3, 4, 5),
            (5, 0, 1, 8, 9),
        ],
    ),
}


@pytest.mark.parametrize(
    "tree,delete,move_to,valid_tree",
    DELETE_CATEGORY_TEST_CASES.values(),
    ids=DELETE_CATEGORY_TEST_CASES,
)
def test_delete_category_maintains_valid_category_tree(
    root_category, tree, delete, move_to, valid_tree
):
    Category.objects.filter(tree_id=root_category.tree_id, level__gt=0).delete()
    categories = generate_categories_tree(root_category, tree)
    indexes = {category.id: index for index, category in categories.items()}

    if move_to is True or move_to is None:
        move_children_to = move_to
    else:
        move_children_to = categories[move_to]

    delete_category(
        categories.pop(delete),
        move_children_to=move_children_to,
    )

    tree_db = [
        (indexes[c.id], indexes.get(c.parent_id), c.level, c.lft, c.rght)
        for c in Category.objects.filter(tree_id=root_category.tree_id).order_by("lft")
    ]

    assert tree_db == valid_tree


def generate_categories_tree(
    root_category: Category, tree: dict[int, int]
) -> dict[int, Category]:
    categories: dict[int, Category] = {0: root_category}
    for category_id, category_parent in tree.items():
        if category_id == 0:
            continue

        parent = categories[category_parent]
        categories[category_id] = Category.objects.create(
            name=f"Category #{category_id}",
            slug=f"category-{category_id}",
            parent=parent,
            tree_id=parent.tree_id,
            level=parent.level + 1,
        )

    heal_category_trees()

    queryset = Category.objects.filter(tree_id=root_category.tree_id).order_by("lft")
    return {i: category for i, category in enumerate(queryset)}
