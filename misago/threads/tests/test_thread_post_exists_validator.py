import pytest

from ..errors import PostNotFoundError
from ..validators import ThreadPostExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_reply_if_id_given_exists_in_db(context, thread, reply):
    validator = ThreadPostExistsValidator(context, thread)
    assert await validator(reply.id) == reply


@pytest.mark.asyncio
async def test_validator_raises_post_not_found_error_if_reply_not_exists(
    context, thread
):
    validator = ThreadPostExistsValidator(context, thread)
    with pytest.raises(PostNotFoundError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_raises_post_not_found_error_if_reply_belongs_to_other_thread(
    context, user_thread, reply
):
    validator = ThreadPostExistsValidator(context, user_thread)
    with pytest.raises(PostNotFoundError):
        await validator(reply.id)
