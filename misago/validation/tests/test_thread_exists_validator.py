import pytest

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
