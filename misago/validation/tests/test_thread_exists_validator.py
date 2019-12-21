import pytest

from ...categories import CategoryTypes
from ...errors import ThreadDoesNotExistError
from ..validators import ThreadExistsValidator


@pytest.mark.asyncio
async def test_validator_returns_thread_if_id_given_exists_in_db(thread):
    validator = ThreadExistsValidator({})
    assert await validator(thread.id) == thread


@pytest.mark.asyncio
async def test_validator_raises_thread_does_not_exist_error_if_thread_not_exists(db):
    validator = ThreadExistsValidator({})
    with pytest.raises(ThreadDoesNotExistError):
        await validator(100)


@pytest.mark.asyncio
async def test_validator_returns_thread_if_given_id_and_type_exists_in_db(thread):
    validator = ThreadExistsValidator({}, CategoryTypes.THREADS)
    assert await validator(thread.id) == thread


@pytest.mark.asyncio
async def test_validator_raises_thread_does_not_exist_error_for_wrong_category_type(
    thread,
):
    validator = ThreadExistsValidator({}, CategoryTypes.PRIVATE_THREADS)
    with pytest.raises(ThreadDoesNotExistError):
        await validator(thread.id)
