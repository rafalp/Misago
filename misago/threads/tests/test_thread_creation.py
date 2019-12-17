from datetime import datetime
from unittest.mock import Mock

import pytest

from ..create import create_post, create_thread
from ..get import get_thread_by_id


@pytest.mark.asyncio
async def test_thread_is_created_in_db(category):
    thread = await create_thread(category, "Test thread", starter_name="User")
    assert thread.id
    assert thread == await get_thread_by_id(thread.id)


@pytest.mark.asyncio
async def test_thread_is_created_with_slug(category):
    thread = await create_thread(category, "Test thread", starter_name="User")
    assert thread.slug == "test-thread"


@pytest.mark.asyncio
async def test_thread_is_created_with_category_id(category):
    thread = await create_thread(category, "Test thread", starter_name="User")
    assert thread.category_id == category.id


@pytest.mark.asyncio
async def test_thread_is_created_with_default_start_and_last_posted_date(category):
    thread = await create_thread(category, "Test thread", starter_name="User")
    assert thread.started_at
    assert thread.last_posted_at
    assert thread.started_at == thread.last_posted_at


@pytest.mark.asyncio
async def test_thread_is_created_with_explicit_start_and_last_posted_date(category):
    started_at = datetime.utcnow()
    thread = await create_thread(
        category, "Test thread", starter_name="User", started_at=started_at
    )
    assert thread.started_at == started_at
    assert thread.last_posted_at == started_at


@pytest.mark.asyncio
async def test_thread_is_created_with_removed_starter_user(category):
    thread = await create_thread(
        category, "Test thread", starter_name="User", started_at=datetime.utcnow()
    )
    assert thread.starter_id is None
    assert thread.starter_name == "User"
    assert thread.last_poster_id is None
    assert thread.last_poster_name == "User"


@pytest.mark.asyncio
async def test_thread_is_created_with_starter_user(category, user):
    thread = await create_thread(category, "Test thread", starter=user)
    assert thread.starter_id == user.id
    assert thread.starter_name == user.name
    assert thread.last_poster_id == user.id
    assert thread.last_poster_name == user.name


@pytest.mark.asyncio
async def test_creating_thread_with_both_starter_and_starter_name_raises_value_error(
    category, user
):
    with pytest.raises(ValueError):
        await create_thread(
            category, "Test thread", starter=user, starter_name=user.name
        )


@pytest.mark.asyncio
async def test_creating_thread_without_first_post_or_starter_raises_value_error(
    category,
):
    with pytest.raises(ValueError):
        await create_thread(category, "Test thread")


@pytest.mark.asyncio
async def test_creating_thread_with_first_post_and_starter_raises_value_error(
    category, user
):
    with pytest.raises(ValueError):
        await create_thread(category, "Test thread", first_post=Mock(), starter=user)


@pytest.mark.asyncio
async def test_creating_thread_with_first_post_and_starter_name_raises_value_error(
    category,
):
    with pytest.raises(ValueError):
        await create_thread(
            category, "Test thread", first_post=Mock(), starter_name="User"
        )


@pytest.mark.asyncio
async def test_creating_thread_with_first_post_and_started_at_raises_value_error(
    category,
):
    with pytest.raises(ValueError):
        await create_thread(
            category, "Test thread", first_post=Mock(), started_at=datetime.utcnow()
        )


@pytest.mark.asyncio
async def test_thread_is_created_with_first_id(category):
    other_thread = await create_thread(category, "Other thread", starter_name="User")
    post = await create_post(other_thread, {}, poster_name="User")
    thread = await create_thread(category, "Test thread", first_post=post)
    assert thread.first_post_id == post.id
    assert thread.last_post_id == post.id


@pytest.mark.asyncio
async def test_thread_is_created_with_first_post_poster_as_starter(category, user):
    post = Mock(
        id=None, poster_id=user.id, poster_name=user.name, posted_at=datetime.utcnow()
    )
    thread = await create_thread(category, "Test thread", first_post=post)
    assert thread.starter_id == user.id
    assert thread.starter_name == user.name
    assert thread.last_poster_id == user.id
    assert thread.last_poster_name == user.name


@pytest.mark.asyncio
async def test_thread_is_created_with_first_post_removed_poster_as_starter(category):
    post = Mock(
        id=None, poster_id=None, poster_name="User", posted_at=datetime.utcnow()
    )
    thread = await create_thread(category, "Test thread", first_post=post)
    assert thread.starter_id is None
    assert thread.starter_name == "User"
    assert thread.last_poster_id is None
    assert thread.last_poster_name == "User"


@pytest.mark.asyncio
async def test_thread_is_created_with_first_post_posted_at_date(category):
    posted_at = datetime.utcnow()
    post = Mock(id=None, poster_id=None, poster_name="User", posted_at=posted_at)
    thread = await create_thread(category, "Test thread", first_post=post)
    assert thread.started_at == posted_at
    assert thread.last_posted_at == posted_at


@pytest.mark.asyncio
async def test_thread_is_created_with_ordering(category):
    thread = await create_thread(category, "Test thread", starter_name="User")
    assert thread.ordering


@pytest.mark.asyncio
async def test_thread_is_created_with_zero_replies(category):
    thread = await create_thread(category, "Test thread", starter_name="User")
    assert thread.replies == 0


@pytest.mark.asyncio
async def test_thread_is_created_with_explicit_replies_count(category):
    thread = await create_thread(
        category, "Test thread", starter_name="User", replies=10
    )
    assert thread.replies == 10


@pytest.mark.asyncio
async def test_thread_is_created_open(category):
    thread = await create_thread(category, "Test thread", starter_name="User")
    assert not thread.is_closed


@pytest.mark.asyncio
async def test_thread_is_created_closed(category):
    thread = await create_thread(
        category, "Test thread", starter_name="User", is_closed=True
    )
    assert thread.is_closed
