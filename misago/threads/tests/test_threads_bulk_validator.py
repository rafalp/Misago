import pytest

from ...validation import ErrorsList
from ..validators import ThreadExistsValidator, ThreadsBulkValidator


@pytest.mark.asyncio
async def test_bulk_threads_validator_validates_threads(
    loaders_context, thread, user_thread
):
    errors = ErrorsList()
    validator = ThreadsBulkValidator([ThreadExistsValidator(loaders_context)])
    threads = await validator([thread.id, user_thread.id], errors, "threads")

    assert not errors
    assert threads == [thread, user_thread]


@pytest.mark.asyncio
async def test_bulk_threads_validator_partially_validates_threads(
    loaders_context, thread
):
    errors = ErrorsList()
    validator = ThreadsBulkValidator([ThreadExistsValidator(loaders_context)])
    threads = await validator([thread.id, thread.id + 1], errors, "threads")

    assert errors == [
        {
            "loc": "threads.1",
            "type": "thread_error.not_found",
            "msg": f"thread with id '{thread.id + 1}' could not be found",
        },
    ]
    assert threads == [thread]
