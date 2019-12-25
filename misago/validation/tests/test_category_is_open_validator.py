import pytest

from ...errors import CategoryClosedError
from ..validators import CategoryIsOpenValidator


@pytest.mark.asyncio
async def test_validator_returns_category_if_its_open(graphql_context, category):
    validator = CategoryIsOpenValidator(graphql_context)
    assert await validator(category) == category


@pytest.mark.asyncio
async def test_validator_raises_category_closed_error_if_category_is_closed(
    graphql_context, closed_category
):
    validator = CategoryIsOpenValidator(graphql_context)
    with pytest.raises(CategoryClosedError):
        await validator(closed_category)


@pytest.mark.asyncio
async def test_validator_returns_category_if_its_closed_but_user_is_moderator(
    moderator_graphql_context, closed_category
):
    validator = CategoryIsOpenValidator(moderator_graphql_context)
    assert await validator(closed_category) == closed_category
