import pytest

from ..randomrow import get_random_thread, get_random_user


@pytest.mark.asyncio
async def test_random_thread_can_be_retrieved(thread):
    assert await get_random_thread() == thread


@pytest.mark.asyncio
async def test_none_is_returned_for_random_thread_if_no_threads_exist(db):
    assert await get_random_thread() is None


@pytest.mark.asyncio
async def test_random_user_can_be_retrieved(user):
    assert await get_random_user() == user


@pytest.mark.asyncio
async def test_none_is_returned_for_random_user_if_no_users_exist(db):
    assert await get_random_user() is None
