import pytest

from ...auth.errors import NotModeratorError
from ..validators import CategoryModeratorValidator


@pytest.mark.asyncio
async def test_validator_returns_category_if_user_is_moderator(
    category, moderator_context
):
    validator = CategoryModeratorValidator(moderator_context)
    assert await validator(category) == category


@pytest.mark.asyncio
async def test_validator_raises_not_moderator_error_if_user_is_not_moderator(
    category, user_context
):
    validator = CategoryModeratorValidator(user_context)
    with pytest.raises(NotModeratorError):
        await validator(category)


@pytest.mark.asyncio
async def test_validator_raises_not_moderator_error_if_user_is_not_authenticated(
    category, context
):
    validator = CategoryModeratorValidator(context)
    with pytest.raises(NotModeratorError):
        await validator(category)
