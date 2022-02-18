import pytest

from ..errors import CategoryInvalidParentError
from ..validators import validate_category_parent


def test_validator_returns_category_parent_if_its_valid(
    category, child_category, context
):
    assert validate_category_parent(child_category, category) == category


def test_validator_raises_invalid_parent_error_if_new_parent_is_same_as_category(
    category, context
):
    with pytest.raises(CategoryInvalidParentError):
        validate_category_parent(category, category)


def test_validator_raises_invalid_parent_error_if_parent_own_is_child_category(
    category, child_category, context
):
    with pytest.raises(CategoryInvalidParentError):
        validate_category_parent(category, child_category)


def test_validator_raises_invalid_parent_error_if_parent_is_child_category(
    child_category, sibling_category, context
):
    with pytest.raises(CategoryInvalidParentError):
        validate_category_parent(sibling_category, child_category)


def test_validator_raises_invalid_parent_error_if_category_has_child_categories(
    category, sibling_category, context
):
    with pytest.raises(CategoryInvalidParentError):
        validate_category_parent(category, sibling_category)
