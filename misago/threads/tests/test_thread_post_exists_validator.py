import pytest

from ..errors import PostNotFoundError
from ..validators import ThreadPostExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_reply_if_id_given_exists_in_db(thread, reply):
    validator = ThreadPostExistsValidator({}, thread)
    assert await validator(reply.id) == reply


@pytest.mark.asyncio
async def test_validator_raises_post_not_exists_error_if_reply_not_exists(thread):
    validator = ThreadPostExistsValidator({}, thread)
    with pytest.raises(PostNotFoundError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_raises_post_not_exists_error_if_reply_belongs_to_other_thread(
    user_thread, reply
):
    validator = ThreadPostExistsValidator({}, user_thread)
    with pytest.raises(PostNotFoundError):
        await validator(reply.id)
