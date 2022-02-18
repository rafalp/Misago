import pytest

from ..errors import CategoryIsClosedError
from ..validators import CategoryIsOpenValidator


@pytest.mark.asyncio
async def test_validator_returns_category_if_its_open(category, context):
    validator = CategoryIsOpenValidator(context)
    assert await validator(category) == category


@pytest.mark.asyncio
async def test_validator_raises_category_closed_error_if_category_is_closed(
    closed_category, context
):
    validator = CategoryIsOpenValidator(context)
    with pytest.raises(CategoryIsClosedError):
        await validator(closed_category)


@pytest.mark.asyncio
async def test_validator_returns_category_if_its_closed_but_user_is_moderator(
    closed_category, moderator_context
):
    validator = CategoryIsOpenValidator(moderator_context)
    assert await validator(closed_category) == closed_category
