import pytest

from ...errors import CategoryIsClosedError
from ..validators import CategoryIsOpenValidator


@pytest.mark.asyncio
async def test_validator_returns_category_if_its_open(user_graphql_context, category):
    validator = CategoryIsOpenValidator(user_graphql_context)
    assert await validator(category) == category


@pytest.mark.asyncio
async def test_validator_raises_category_is_closed_error_if_category_is_closed(
    user_graphql_context, closed_category
):
    validator = CategoryIsOpenValidator(user_graphql_context)
    with pytest.raises(CategoryIsClosedError):
        await validator(closed_category)


@pytest.mark.asyncio
async def test_validator_returns_category_if_its_closed_but_user_is_moderator(
    moderator_graphql_context, closed_category
):
    validator = CategoryIsOpenValidator(moderator_graphql_context)
    assert await validator(closed_category) == closed_category
