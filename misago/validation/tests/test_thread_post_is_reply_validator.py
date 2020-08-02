import pytest

from ...errors import ThreadFirstPostError
from ..validators import ThreadPostIsReplyValidator


@pytest.mark.asyncio
async def test_validator_returns_post_if_its_thread_reply(thread, reply):
    validator = ThreadPostIsReplyValidator(thread)
    assert await validator(reply) == reply


@pytest.mark.asyncio
async def test_validator_raises_first_post_error_if_post_is_original_message(
    thread, post
):
    validator = ThreadPostIsReplyValidator(thread)
    with pytest.raises(ThreadFirstPostError):
        await validator(post)
