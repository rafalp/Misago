import pytest

from ..enums import CategoryTree
from ..models import Category
from ..treeid import get_category_tree_id, _get_category_tree_id_from_db


def test_get_category_tree_id_returns_threads_tree_id_for_category(default_category):
    assert get_category_tree_id(default_category) == CategoryTree.THREADS


def test_get_category_tree_id_returns_threads_tree_id_for_category_id(default_category):
    assert get_category_tree_id(default_category.id) == CategoryTree.THREADS


def test_get_category_tree_id_returns_threads_tree_id_for_private_threads_category(
    private_threads_category,
):
    assert (
        get_category_tree_id(private_threads_category) == CategoryTree.PRIVATE_THREADS
    )


def test_get_category_tree_id_returns_threads_tree_id_for_private_threads_category_id(
    private_threads_category,
):
    assert (
        get_category_tree_id(private_threads_category.id)
        == CategoryTree.PRIVATE_THREADS
    )


def test_get_category_tree_id_memoizes_results(
    django_assert_num_queries, default_category
):
    _get_category_tree_id_from_db.cache_clear()

    with django_assert_num_queries(1):
        get_category_tree_id(default_category)
        get_category_tree_id(default_category.id)


def test_get_category_tree_id_raises_category_does_not_exists_error_for_invalid_id(db):
    with pytest.raises(Category.DoesNotExist):
        get_category_tree_id(2137)


def test_get_category_tree_id_raises_type_error_for_invalid_id_type(db):
    with pytest.raises(TypeError):
        get_category_tree_id("wop")
