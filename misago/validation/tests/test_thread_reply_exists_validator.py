import pytest

from ...errors import PostDoesNotExistError, ThreadFirstPostError
from ..validators import ThreadReplyExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_reply_if_id_given_exists_in_db(thread, reply):
    validator = ThreadReplyExistsValidator({}, thread)
    assert await validator(reply.id) == reply


@pytest.mark.asyncio
async def test_validator_raises_post_not_exists_error_if_reply_not_exists(thread):
    validator = ThreadReplyExistsValidator({}, thread)
    with pytest.raises(PostDoesNotExistError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_raises_post_not_exists_error_if_reply_belongs_to_other_thread(
    user_thread, reply
):
    validator = ThreadReplyExistsValidator({}, user_thread)
    with pytest.raises(PostDoesNotExistError):
        await validator(reply.id)


@pytest.mark.asyncio
async def test_validator_raises_first_post_error_if_post_is_not_thread_reply(
    thread, post
):
    validator = ThreadReplyExistsValidator({}, thread)
    with pytest.raises(ThreadFirstPostError):
        await validator(post.id)
