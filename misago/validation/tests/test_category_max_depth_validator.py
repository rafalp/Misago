import pytest

from ...errors import CategoryMaxDepthError
from ..validators import CategoryMaxDepthValidator


@pytest.mark.asyncio
async def test_validator_returns_category_if_it_has_valid_depth(
    graphql_context, category
):
    validator = CategoryMaxDepthValidator(graphql_context, max_depth=0)
    assert await validator(category) == category


@pytest.mark.asyncio
async def test_validator_returns_category_if_it_has_depth_lower_than_limit(
    graphql_context, category
):
    validator = CategoryMaxDepthValidator(graphql_context, max_depth=2)
    assert await validator(category) == category


@pytest.mark.asyncio
async def test_validator_raises_category_max_depth_error_if_category_exceeds_depth(
    graphql_context, child_category
):
    validator = CategoryMaxDepthValidator(graphql_context, max_depth=0)
    with pytest.raises(CategoryMaxDepthError):
        await validator(child_category)
