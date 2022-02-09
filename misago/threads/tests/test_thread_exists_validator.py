import pytest

from ...categories.models import CategoryType
from ..errors import ThreadNotFoundError
from ..loaders import threads_loader
from ..validators import ThreadExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_thread_if_id_given_exists_in_db(
    loaders_context, thread
):
    validator = ThreadExistsValidator(loaders_context)
    assert await validator(thread.id) == thread


@pytest.mark.asyncio
async def test_validator_raises_thread_not_exists_error_if_thread_not_exists(
    db, loaders_context
):
    validator = ThreadExistsValidator(loaders_context)
    with pytest.raises(ThreadNotFoundError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_returns_thread_if_given_id_and_type_exists_in_db(
    loaders_context, thread
):
    validator = ThreadExistsValidator(loaders_context, CategoryType.THREADS)
    assert await validator(thread.id) == thread


@pytest.mark.asyncio
async def test_validator_raises_thread_not_exists_error_for_wrong_category_type(
    loaders_context, thread
):
    validator = ThreadExistsValidator(loaders_context, CategoryType.PRIVATE_THREADS)
    with pytest.raises(ThreadNotFoundError):
        await validator(thread.id)
