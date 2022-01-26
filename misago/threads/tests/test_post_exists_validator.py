import pytest

from ...categories import CategoryType
from ..errors import PostNotFoundError
from ..validators import PostExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_post_if_id_given_exists_in_db(post):
    validator = PostExistsValidator({})
    assert await validator(post.id) == post


@pytest.mark.asyncio
async def test_validator_raises_post_not_exists_error_if_post_not_exists(db):
    validator = PostExistsValidator({})
    with pytest.raises(PostNotFoundError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_returns_post_if_given_id_and_type_exists_in_db(post):
    validator = PostExistsValidator({}, CategoryType.THREADS)
    assert await validator(post.id) == post


@pytest.mark.asyncio
async def test_validator_raises_post_not_exists_error_for_wrong_category_type(post):
    validator = PostExistsValidator({}, CategoryType.PRIVATE_THREADS)
    with pytest.raises(PostNotFoundError):
        await validator(post.id)
