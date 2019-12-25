import pytest

from ...errors import ThreadFirstPostError
from ..validators import PostIsReplyValidator


@pytest.mark.asyncio
async def test_validator_returns_post_if_its_reply(graphql_context, reply):
    validator = PostIsReplyValidator(graphql_context)
    assert await validator(reply) == reply


@pytest.mark.asyncio
async def test_validator_raises_first_post_error_if_post_is_not_reply(
    graphql_context, post
):
    validator = PostIsReplyValidator(graphql_context)
    with pytest.raises(ThreadFirstPostError):
        await validator(post)
