import pytest

from ...errors import PostDoesNotExistError
from ..validators import PostExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_post_if_id_given_exists_in_db(post):
    validator = PostExistsValidator({})
    assert await validator(post.id) == post


@pytest.mark.asyncio
async def test_validator_raises_post_does_not_exist_error_if_post_not_exists(db):
    validator = PostExistsValidator({})
    with pytest.raises(PostDoesNotExistError):
        await validator(100)
