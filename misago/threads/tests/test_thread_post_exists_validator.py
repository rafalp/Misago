import pytest

from ..errors import PostNotFoundError
from ..validators import ThreadPostExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_reply_if_id_given_exists_in_db(
    loaders_context, thread, reply
):
    validator = ThreadPostExistsValidator(loaders_context, thread)
    assert await validator(reply.id) == reply


@pytest.mark.asyncio
async def test_validator_raises_post_not_found_error_if_reply_not_exists(
    loaders_context, thread
):
    validator = ThreadPostExistsValidator(loaders_context, thread)
    with pytest.raises(PostNotFoundError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_raises_post_not_found_error_if_reply_belongs_to_other_thread(
    loaders_context, user_thread, reply
):
    validator = ThreadPostExistsValidator(loaders_context, user_thread)
    with pytest.raises(PostNotFoundError):
        await validator(reply.id)
