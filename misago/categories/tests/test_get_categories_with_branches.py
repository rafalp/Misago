from ..display import get_categories_with_branches
from ..models import Category


def test_get_categories_with_branches_returns_empty_list_for_no_categories():
    assert get_categories_with_branches([]) == []


def test_get_categories_with_branches_returns_list_with_only_top_level_categories(
    root_category,
):
    top_category_1 = Category(name="Category", slug="category")
    top_category_1.insert_at(root_category, position="last-child", save=True)

    top_category_2 = Category(name="Category", slug="category")
    top_category_2.insert_at(root_category, position="last-child", save=True)

    assert get_categories_with_branches(
        [
            top_category_1,
            top_category_2,
        ]
    ) == [
        ("", top_category_1),
        ("", top_category_2),
    ]


def test_get_categories_with_branches_returns_list_with_top_level_category_with_child(
    root_category,
):
    top_category = Category(name="Category", slug="category")
    top_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Category", slug="category")
    child_category.insert_at(top_category, position="last-child", save=True)

    assert get_categories_with_branches(
        [
            top_category,
            child_category,
        ]
    ) == [
        ("", top_category),
        ("L", child_category),
    ]


def test_get_categories_with_branches_returns_list_with_top_level_category_with_multiple_children(
    root_category,
):
    top_category = Category(name="Category", slug="category")
    top_category.insert_at(root_category, position="last-child", save=True)

    child_category_1 = Category(name="Category", slug="category")
    child_category_1.insert_at(top_category, position="last-child", save=True)

    child_category_2 = Category(name="Category", slug="category")
    child_category_2.insert_at(top_category, position="last-child", save=True)

    assert get_categories_with_branches(
        [
            top_category,
            child_category_1,
            child_category_2,
        ]
    ) == [
        ("", top_category),
        ("T", child_category_1),
        ("L", child_category_2),
    ]


def test_get_categories_with_branches_returns_list_with_top_level_category_with_multiple_children_and_sibling_category(
    root_category,
):
    top_category_1 = Category(name="Category", slug="category")
    top_category_1.insert_at(root_category, position="last-child", save=True)

    child_category_1 = Category(name="Category", slug="category")
    child_category_1.insert_at(top_category_1, position="last-child", save=True)

    child_category_2 = Category(name="Category", slug="category")
    child_category_2.insert_at(top_category_1, position="last-child", save=True)

    top_category_2 = Category(name="Category", slug="category")
    top_category_2.insert_at(root_category, position="last-child", save=True)

    assert get_categories_with_branches(
        [
            top_category_1,
            child_category_1,
            child_category_2,
            top_category_2,
        ]
    ) == [
        ("", top_category_1),
        ("T", child_category_1),
        ("L", child_category_2),
        ("", top_category_2),
    ]


def test_get_categories_with_branches_returns_list_with_top_level_category_with_children_two_levels_deep(
    root_category,
):
    top_category = Category(name="Category", slug="category")
    top_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Category", slug="category")
    child_category.insert_at(top_category, position="last-child", save=True)

    child_child_category = Category(name="Category", slug="category")
    child_child_category.insert_at(child_category, position="last-child", save=True)

    assert get_categories_with_branches(
        [
            top_category,
            child_category,
            child_child_category,
        ]
    ) == [
        ("", top_category),
        ("L", child_category),
        ("SL", child_child_category),
    ]


def test_get_categories_with_branches_returns_list_with_top_level_category_with_middle_child_with_child(
    root_category,
):
    top_category = Category(name="Category", slug="category")
    top_category.insert_at(root_category, position="last-child", save=True)

    child_category_1 = Category(name="Category", slug="category")
    child_category_1.insert_at(top_category, position="last-child", save=True)

    child_child_category = Category(name="Category", slug="category")
    child_child_category.insert_at(child_category_1, position="last-child", save=True)

    child_category_2 = Category(name="Category", slug="category")
    child_category_2.insert_at(top_category, position="last-child", save=True)

    assert get_categories_with_branches(
        [
            top_category,
            child_category_1,
            child_child_category,
            child_category_2,
        ]
    ) == [
        ("", top_category),
        ("T", child_category_1),
        ("IL", child_child_category),
        ("L", child_category_2),
    ]


def test_get_categories_with_branches_returns_list_with_top_level_category_with_middle_child_with_child_with_child(
    root_category,
):
    top_category = Category(name="Category", slug="category")
    top_category.insert_at(root_category, position="last-child", save=True)

    child_category_1 = Category(name="Category", slug="category")
    child_category_1.insert_at(top_category, position="last-child", save=True)

    child_child_category = Category(name="Category", slug="category")
    child_child_category.insert_at(child_category_1, position="last-child", save=True)

    child_child_child_category = Category(name="Category", slug="category")
    child_child_child_category.insert_at(
        child_child_category, position="last-child", save=True
    )

    child_category_2 = Category(name="Category", slug="category")
    child_category_2.insert_at(top_category, position="last-child", save=True)

    assert get_categories_with_branches(
        [
            top_category,
            child_category_1,
            child_child_category,
            child_child_child_category,
            child_category_2,
        ]
    ) == [
        ("", top_category),
        ("T", child_category_1),
        ("IL", child_child_category),
        ("ISL", child_child_child_category),
        ("L", child_category_2),
    ]
