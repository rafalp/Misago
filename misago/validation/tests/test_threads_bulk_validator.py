import pytest

from ...errors import ErrorsList
from ..validators import ThreadExistsValidator, ThreadsBulkValidator


@pytest.mark.asyncio
async def test_bulk_threads_validator_validates_threads(thread, user_thread):
    errors = ErrorsList()
    context = {}
    validator = ThreadsBulkValidator([ThreadExistsValidator(context)])
    threads = await validator([thread.id, user_thread.id], errors, "threads")
    assert not errors
    assert threads == [thread, user_thread]


@pytest.mark.asyncio
async def test_bulk_threads_validator_partially_validates_threads(thread):
    errors = ErrorsList()
    context = {}
    validator = ThreadsBulkValidator([ThreadExistsValidator(context)])
    threads = await validator([thread.id, thread.id + 1], errors, "threads")
    assert errors == [
        {
            "loc": "threads.1",
            "type": "value_error.thread.not_exists",
            "msg": f"thread with id '{thread.id + 1}' does not exist",
        },
    ]
    assert threads == [thread]
