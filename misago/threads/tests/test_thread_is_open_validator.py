import pytest

from ..errors import ThreadIsClosedError
from ..validators import ThreadIsOpenValidator


@pytest.mark.asyncio
async def test_validator_returns_thread_if_its_open(graphql_context, thread):
    validator = ThreadIsOpenValidator(graphql_context)
    assert await validator(thread) == thread


@pytest.mark.asyncio
async def test_validator_raises_thread_closed_error_if_thread_is_closed(
    graphql_context, closed_thread
):
    validator = ThreadIsOpenValidator(graphql_context)
    with pytest.raises(ThreadIsClosedError):
        await validator(closed_thread)


@pytest.mark.asyncio
async def test_validator_returns_thread_if_its_closed_but_user_is_moderator(
    moderator_graphql_context, closed_thread
):
    validator = ThreadIsOpenValidator(moderator_graphql_context)
    assert await validator(closed_thread) == closed_thread
