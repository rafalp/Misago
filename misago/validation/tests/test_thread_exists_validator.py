import pytest

from ...errors import ThreadDoesNotExistError
from ..validators import validate_thread_exists


@pytest.mark.asyncio
async def test_validator_returns_thread_if_id_given_exists_in_db(thread):
    validator = validate_thread_exists({})
    assert await validator(thread.id) == thread


@pytest.mark.asyncio
async def test_validator_raises_thread_does_not_exist_error_if_thread_not_exists(db):
    validator = validate_thread_exists({})
    with pytest.raises(ThreadDoesNotExistError):
        await validator(100)
