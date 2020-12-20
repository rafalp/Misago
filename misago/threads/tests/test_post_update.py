import pytest

from ...utils import timezone
from ..create import create_post, create_thread
from ..get import get_post_by_id
from ..update import update_post


@pytest.fixture
async def thread(category):
    return await create_thread(category, "Test thread", starter_name="Guest")


@pytest.fixture
async def post(thread):
    return await create_post(thread, poster_name="Guest")


@pytest.mark.asyncio
async def test_post_category_can_be_updated(post, child_category):
    updated_post = await update_post(post, category=child_category)
    assert updated_post.category_id == child_category.id


@pytest.mark.asyncio
async def test_post_thread_can_be_updated(post, child_category):
    other_thread = await create_thread(
        child_category, "Test thread", starter_name="Guest"
    )
    updated_post = await update_post(post, thread=other_thread)
    assert updated_post.category_id == other_thread.category_id
    assert updated_post.thread_id == other_thread.id


@pytest.mark.asyncio
async def test_updating_post_thread_and_category_raises_value_error(
    post, child_category
):
    other_thread = await create_thread(
        child_category, "Test thread", starter_name="Guest"
    )
    with pytest.raises(ValueError):
        await update_post(post, category=child_category, thread=other_thread)


@pytest.mark.asyncio
async def test_post_markup_can_be_updated(post):
    new_markup = "Hello"
    updated_post = await update_post(post, markup=new_markup)
    assert updated_post.markup == new_markup


@pytest.mark.asyncio
async def test_post_rich_text_can_be_updated(post):
    new_rich_text = {"new": True}
    updated_post = await update_post(post, rich_text=new_rich_text)
    assert updated_post.rich_text == new_rich_text


@pytest.mark.asyncio
async def test_post_poster_can_be_updated(post, user):
    updated_post = await update_post(post, poster=user)
    assert updated_post.poster_id == user.id
    assert updated_post.poster_name == user.name


@pytest.mark.asyncio
async def test_post_poster_name_can_be_updated(post):
    updated_post = await update_post(post, poster_name="User")
    assert updated_post.poster_id is None
    assert updated_post.poster_name == "User"


@pytest.mark.asyncio
async def test_post_poster_can_be_removed(post, user):
    post = await update_post(post, poster=user)
    updated_post = await update_post(post, poster_name="Guest")
    assert updated_post.poster_id is None
    assert updated_post.poster_name == "Guest"


@pytest.mark.asyncio
async def test_updating_post_poster_and_poster_name_raises_value_error(post, user):
    with pytest.raises(ValueError):
        await update_post(post, poster=user, poster_name=user.name)


@pytest.mark.asyncio
async def test_post_edits_count_can_be_updated(post):
    updated_post = await update_post(post, edits=5)
    assert updated_post.edits == 5


@pytest.mark.asyncio
async def test_post_edits_count_can_be_incremented(post):
    updated_post = await update_post(post, increment_edits=True)
    assert updated_post.edits == 1

    post_from_db = await get_post_by_id(post.id)
    assert post_from_db.edits == 1


@pytest.mark.asyncio
async def test_updating_and_incrementing_post_edits_raises_value_error(post):
    with pytest.raises(ValueError):
        await update_post(post, edits=5, increment_edits=True)


@pytest.mark.asyncio
async def test_post_date_can_be_updated(post):
    posted_at = timezone.now()
    updated_post = await update_post(post, posted_at=posted_at)
    assert updated_post.posted_at == posted_at


@pytest.mark.asyncio
async def test_post_extra_can_be_updated(post):
    new_extra = {"new": True}
    updated_post = await update_post(post, extra=new_extra)
    assert updated_post.extra == new_extra
