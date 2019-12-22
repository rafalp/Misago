import pytest

from ...errors import NotModeratorError
from ..validators import IsCategoryModeratorValidator


@pytest.mark.asyncio
async def test_validator_returns_category_if_user_is_moderator(
    moderator_graphql_context, category
):
    validator = IsCategoryModeratorValidator(moderator_graphql_context)
    assert await validator(category) == category


@pytest.mark.asyncio
async def test_validator_raises_not_moderator_error_if_user_is_not_moderator(
    user_graphql_context, category
):
    validator = IsCategoryModeratorValidator(user_graphql_context)
    with pytest.raises(NotModeratorError):
        await validator(category)


@pytest.mark.asyncio
async def test_validator_raises_not_moderator_error_if_user_is_not_authenticated(
    graphql_context, category
):
    validator = IsCategoryModeratorValidator(graphql_context)
    with pytest.raises(NotModeratorError):
        await validator(category)
