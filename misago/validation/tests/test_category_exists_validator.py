import pytest

from ...errors import CategoryDoesNotExistError
from ..validators import validate_category_exists


@pytest.mark.asyncio
async def test_validator_returns_category_if_id_given_exists_in_db(category):
    validator = validate_category_exists({})
    assert await validator(category.id) == category


@pytest.mark.asyncio
async def test_validator_raises_category_does_not_exist_error_if_category_not_exists(
    db,
):
    validator = validate_category_exists({})
    with pytest.raises(CategoryDoesNotExistError):
        await validator(100)
