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
    threads = await validator([thread.id, "1000"], errors, "threads")
    assert errors
    assert errors.get_errors_locations() == ["threads.1"]
    assert errors.get_errors_types() == ["value_error.thread.not_exists"]
    assert threads == [thread]
