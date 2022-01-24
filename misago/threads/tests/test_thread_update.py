from dataclasses import replace

import pytest

from ...utils import timezone
from ..models import Post, Thread


@pytest.fixture
async def thread(category):
    return await Thread.create(category, "Test thread", starter_name="Guest")


@pytest.mark.asyncio
async def test_thread_category_is_updated(thread, child_category):
    updated_thread = await thread.update(category=child_category)
    assert updated_thread.category_id == child_category.id


@pytest.mark.asyncio
async def test_thread_first_post_is_updated(thread):
    post = await Post.create(thread, poster_name="Guest")
    updated_thread = await thread.update(first_post=post)
    assert updated_thread.first_post_id == post.id


@pytest.mark.asyncio
async def test_thread_starter_is_updated(thread, other_user):
    updated_thread = await thread.update(starter=other_user)
    assert updated_thread.starter_id == other_user.id
    assert updated_thread.starter_name == other_user.name


@pytest.mark.asyncio
async def test_thread_starter_name_is_updated(category, user):
    thread = await Thread.create(category, "Test thread", starter=user)
    renamed_user = replace(user, name="Renamed")
    updated_thread = await thread.update(starter=renamed_user)
    assert updated_thread.starter_id == renamed_user.id
    assert updated_thread.starter_name == renamed_user.name


@pytest.mark.asyncio
async def test_thread_starter_id_can_be_removed(thread, user):
    thread = await thread.update(starter=user)
    updated_thread = await thread.update(starter_name="Guest")
    assert updated_thread.starter_id is None
    assert updated_thread.starter_name == "Guest"


@pytest.mark.asyncio
async def test_thread_last_post_is_updated(thread):
    post = await Post.create(thread, poster_name="Guest")
    updated_thread = await thread.update(last_post=post)
    assert updated_thread.last_post_id == post.id


@pytest.mark.asyncio
async def test_thread_last_poster_is_updated(thread, other_user):
    updated_thread = await thread.update(last_poster=other_user)
    assert updated_thread.last_poster_id == other_user.id
    assert updated_thread.last_poster_name == other_user.name


@pytest.mark.asyncio
async def test_thread_last_poster_name_is_updated(category, user):
    thread = await Thread.create(category, "Test thread", starter=user)
    renamed_user = replace(user, name="Renamed")
    updated_thread = await thread.update(last_poster=renamed_user)
    assert updated_thread.last_poster_id == renamed_user.id
    assert updated_thread.last_poster_name == renamed_user.name


@pytest.mark.asyncio
async def test_thread_last_poster_id_can_be_removed(thread, user):
    thread = await thread.update(last_poster=user)
    updated_thread = await thread.update(last_poster_name="Guest")
    assert updated_thread.last_poster_id is None
    assert updated_thread.last_poster_name == "Guest"


@pytest.mark.asyncio
async def test_thread_title_is_updated(thread):
    updated_thread = await thread.update(title="New title")
    assert updated_thread.title == "New title"
    assert updated_thread.slug == "new-title"


@pytest.mark.asyncio
async def test_thread_start_date_is_updated(thread):
    started_at = timezone.now()
    updated_thread = await thread.update(started_at=started_at)
    assert updated_thread.started_at == started_at


@pytest.mark.asyncio
async def test_thread_last_post_date_is_updated(thread):
    last_posted_at = timezone.now()
    updated_thread = await thread.update(last_posted_at=last_posted_at)
    assert updated_thread.last_posted_at == last_posted_at


@pytest.mark.asyncio
async def test_thread_replies_count_is_updated(thread):
    updated_thread = await thread.update(replies=100)
    assert updated_thread.replies == 100


@pytest.mark.asyncio
async def test_thread_replies_count_can_be_incremented(thread):
    updated_thread = await thread.update(increment_replies=True)
    assert updated_thread.replies == 1

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.replies == 1


@pytest.mark.asyncio
async def test_updating_and_incrementing_thread_replies_raises_value_error(thread):
    with pytest.raises(ValueError):
        await thread.update(replies=1, increment_replies=True)


@pytest.mark.asyncio
async def test_open_thread_can_be_closed(thread):
    updated_thread = await thread.update(is_closed=True)
    assert updated_thread.is_closed


@pytest.mark.asyncio
async def test_closed_thread_can_be_opened(thread):
    thread = replace(thread, is_closed=True)
    updated_thread = await thread.update(is_closed=False)
    assert not updated_thread.is_closed


@pytest.mark.asyncio
async def test_thread_extra_is_updated(thread):
    extra = {"new": True}
    updated_thread = await thread.update(extra=extra)
    assert updated_thread.extra == extra


@pytest.mark.asyncio
async def test_updating_thread_first_post_and_starter_raises_value_error(thread, user):
    post = await Post.create(thread, poster_name="Guest")
    with pytest.raises(ValueError):
        await thread.update(first_post=post, starter=user)


@pytest.mark.asyncio
async def test_updating_thread_starter_and_starter_name_raises_value_error(
    thread, user
):
    with pytest.raises(ValueError):
        await thread.update(starter=user, starter_name="Guest")


@pytest.mark.asyncio
async def test_updating_thread_first_post_and_starter_name_raises_value_error(thread):
    post = await Post.create(thread, poster_name="Guest")
    with pytest.raises(ValueError):
        await thread.update(first_post=post, starter_name="User")


@pytest.mark.asyncio
async def test_updating_thread_first_post_and_start_date_raises_value_error(
    thread, user
):
    started_at = timezone.now()
    post = await Post.create(thread, poster_name="Guest")
    with pytest.raises(ValueError):
        await thread.update(first_post=post, started_at=started_at)


@pytest.mark.asyncio
async def test_updating_thread_last_post_and_last_poster_raises_value_error(
    thread, user
):
    post = await Post.create(thread, poster_name="Guest")
    with pytest.raises(ValueError):
        await thread.update(last_post=post, last_poster=user)


@pytest.mark.asyncio
async def test_updating_thread_last_poster_and_last_poster_name_raises_value_error(
    thread, user
):
    with pytest.raises(ValueError):
        await thread.update(last_poster=user, last_poster_name="User")


@pytest.mark.asyncio
async def test_updating_thread_last_post_and_last_poster_name_raises_value_error(
    thread,
):
    post = await Post.create(thread, poster_name="Guest")
    with pytest.raises(ValueError):
        await thread.update(last_post=post, last_poster_name="User")


@pytest.mark.asyncio
async def test_updating_thread_last_post_and_last_post_date_raises_value_error(
    thread, user
):
    started_at = timezone.now()
    post = await Post.create(thread, poster_name="Guest")
    with pytest.raises(ValueError):
        await thread.update(last_post=post, last_posted_at=started_at)
