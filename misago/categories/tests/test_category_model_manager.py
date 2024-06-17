from ..models import Category


def test_category_manager_returns_private_threads(private_threads_category):
    category = Category.objects.private_threads()

    assert category == private_threads_category
    assert category.special_role == "private_threads"


def test_category_manager_returns_root_category(root_category):
    category = Category.objects.root_category()

    assert category == root_category
    assert category.special_role == "root_category"


def test_category_manager_returns_all_categories(root_category):
    test_category_a = Category(name="Test")
    test_category_a.insert_at(root_category, position="last-child", save=True)

    test_category_b = Category(name="Test 2")
    test_category_b.insert_at(root_category, position="last-child", save=True)

    all_categories_from_db = list(Category.objects.all_categories(True))

    assert root_category in all_categories_from_db
    assert test_category_a in all_categories_from_db
    assert test_category_b in all_categories_from_db
