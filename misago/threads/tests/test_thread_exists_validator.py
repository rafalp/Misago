import pytest

from ...categories.models import CategoryType
from ..errors import ThreadNotFoundError
from ..validators import ThreadExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_thread_if_id_given_exists_in_db(context, thread):
    validator = ThreadExistsValidator(context)
    assert await validator(thread.id) == thread


@pytest.mark.asyncio
async def test_validator_raises_thread_not_exists_error_if_thread_not_exists(context):
    validator = ThreadExistsValidator(context)
    with pytest.raises(ThreadNotFoundError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_returns_thread_if_given_id_and_type_exists_in_db(
    context, thread
):
    validator = ThreadExistsValidator(context, CategoryType.THREADS)
    assert await validator(thread.id) == thread


@pytest.mark.asyncio
async def test_validator_raises_thread_not_exists_error_for_wrong_category_type(
    context, thread
):
    validator = ThreadExistsValidator(context, CategoryType.PRIVATE_THREADS)
    with pytest.raises(ThreadNotFoundError):
        await validator(thread.id)
