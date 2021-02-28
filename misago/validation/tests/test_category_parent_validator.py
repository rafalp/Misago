import pytest

from ...errors import CategoryInvalidParentError
from ..validators import CategoryParentValidator


@pytest.mark.asyncio
async def test_validator_returns_category_parent_if_its_valid(
    graphql_context, category, child_category
):
    validator = CategoryParentValidator(graphql_context, child_category)
    assert await validator(category) == category


@pytest.mark.asyncio
async def test_validator_raises_invalid_parent_error_if_new_parent_is_same_as_category(
    graphql_context, category
):
    validator = CategoryParentValidator(graphql_context, category)
    with pytest.raises(CategoryInvalidParentError):
        await validator(category)


@pytest.mark.asyncio
async def test_validator_raises_invalid_parent_error_if_parent_own_is_child_category(
    graphql_context, category, child_category
):
    validator = CategoryParentValidator(graphql_context, category)
    with pytest.raises(CategoryInvalidParentError):
        await validator(child_category)


@pytest.mark.asyncio
async def test_validator_raises_invalid_parent_error_if_parent_is_child_category(
    graphql_context, child_category, sibling_category
):
    validator = CategoryParentValidator(graphql_context, sibling_category)
    with pytest.raises(CategoryInvalidParentError):
        await validator(child_category)


@pytest.mark.asyncio
async def test_validator_raises_invalid_parent_error_if_category_has_child_categories(
    graphql_context, category, sibling_category
):
    validator = CategoryParentValidator(graphql_context, category)
    with pytest.raises(CategoryInvalidParentError):
        await validator(sibling_category)


@pytest.mark.asyncio
async def test_validator_raises_error_for_new_category_if_parent_is_child_category(
    graphql_context, child_category, sibling_category
):
    validator = CategoryParentValidator(graphql_context)
    with pytest.raises(CategoryInvalidParentError):
        await validator(child_category)
