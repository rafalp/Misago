import pytest

from ...errors import PostDoesNotExistError
from ..validators import validate_post_exists


@pytest.mark.asyncio
async def test_validator_returns_post_if_id_given_exists_in_db(post):
    validator = validate_post_exists({})
    assert await validator(post.id) == post


@pytest.mark.asyncio
async def test_validator_raises_post_does_not_exist_error_if_post_not_exists(db):
    validator = validate_post_exists({})
    with pytest.raises(PostDoesNotExistError):
        await validator(100)
