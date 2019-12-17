from dataclasses import replace
from datetime import datetime

import pytest

from ..create import create_post, create_thread
from ..update import update_thread


@pytest.fixture
async def thread(category):
    return await create_thread(category, "Test thread", starter_name="User")


@pytest.mark.asyncio
async def test_thread_category_can_be_updated(thread, child_category):
    updated_thread = await update_thread(thread, category=child_category)
    assert updated_thread.category_id == child_category.id


@pytest.mark.asyncio
async def test_thread_first_post_can_be_updated(category, thread):
    post = await create_post(category, thread, {}, poster_name="User")
    updated_thread = await update_thread(thread, first_post=post)
    assert updated_thread.first_post_id == post.id


@pytest.mark.asyncio
async def test_thread_starter_can_be_updated(thread, other_user):
    updated_thread = await update_thread(thread, starter=other_user)
    assert updated_thread.starter_id == other_user.id
    assert updated_thread.starter_name == other_user.name


@pytest.mark.asyncio
async def test_thread_starter_name_can_be_updated(category, user):
    thread = await create_thread(category, "Test thread", starter=user)
    renamed_user = replace(user, name="Renamed")
    updated_thread = await update_thread(thread, starter=renamed_user)
    assert updated_thread.starter_id == renamed_user.id
    assert updated_thread.starter_name == renamed_user.name


@pytest.mark.asyncio
async def test_thread_last_poster_can_be_updated(thread, other_user):
    updated_thread = await update_thread(thread, last_poster=other_user)
    assert updated_thread.last_poster_id == other_user.id
    assert updated_thread.last_poster_name == other_user.name


@pytest.mark.asyncio
async def test_thread_last_poster_name_can_be_updated(category, user):
    thread = await create_thread(category, "Test thread", starter=user)
    renamed_user = replace(user, name="Renamed")
    updated_thread = await update_thread(thread, last_poster=renamed_user)
    assert updated_thread.last_poster_id == renamed_user.id
    assert updated_thread.last_poster_name == renamed_user.name


@pytest.mark.asyncio
async def test_thread_title_can_be_updated(thread):
    updated_thread = await update_thread(thread, title="New title")
    assert updated_thread.title == "New title"
    assert updated_thread.slug == "new-title"


@pytest.mark.asyncio
async def test_thread_start_date_can_be_updated(thread):
    started_at = datetime.utcnow()
    updated_thread = await update_thread(thread, started_at=started_at)
    assert updated_thread.started_at == started_at


@pytest.mark.asyncio
async def test_thread_last_post_date_can_be_updated(thread):
    last_posted_at = datetime.utcnow()
    updated_thread = await update_thread(thread, last_posted_at=last_posted_at)
    assert updated_thread.last_posted_at == last_posted_at


@pytest.mark.asyncio
async def test_thread_replies_count_can_be_updated(thread):
    updated_thread = await update_thread(thread, replies=100)
    assert updated_thread.replies == 100


@pytest.mark.asyncio
async def test_thread_closed_status_can_be_updated(thread):
    updated_thread = await update_thread(thread, is_closed=True)
    assert updated_thread.is_closed


@pytest.mark.asyncio
async def test_thread_extra_can_be_updated(thread):
    extra = {"new": True}
    updated_thread = await update_thread(thread, extra=extra)
    assert updated_thread.extra == extra
