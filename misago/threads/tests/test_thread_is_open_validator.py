import pytest

from ..errors import ThreadIsClosedError
from ..validators import ThreadIsOpenValidator


@pytest.mark.asyncio
async def test_validator_returns_thread_if_its_open(thread, context):
    validator = ThreadIsOpenValidator(context)
    assert await validator(thread) == thread


@pytest.mark.asyncio
async def test_validator_raises_thread_closed_error_if_thread_is_closed(
    closed_thread, context
):
    validator = ThreadIsOpenValidator(context)
    with pytest.raises(ThreadIsClosedError):
        await validator(closed_thread)


@pytest.mark.asyncio
async def test_validator_returns_thread_if_its_closed_but_user_is_moderator(
    closed_thread, moderator_context
):
    validator = ThreadIsOpenValidator(moderator_context)
    assert await validator(closed_thread) == closed_thread
