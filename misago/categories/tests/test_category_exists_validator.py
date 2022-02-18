import pytest

from ..errors import CategoryNotFoundError
from ..validators import CategoryExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_category_from_index_if_id_given_exists_in_db(
    category, context
):
    validator = CategoryExistsValidator(context)
    result = await validator(category.id)
    assert result.id == category.id


@pytest.mark.asyncio
async def test_validator_raises_category_not_exists_error_if_category_not_exists(
    context,
):
    validator = CategoryExistsValidator(context)
    with pytest.raises(CategoryNotFoundError):
        await validator(100)
