import pytest

from ...utils import timezone
from ..models import Post, Thread


@pytest.fixture
async def thread(category):
    return await Thread.create(category, "Test thread", starter_name="Guest")


@pytest.fixture
async def post(thread):
    return await Post.create(thread, poster_name="Guest")


@pytest.mark.asyncio
async def test_post_category_is_updated(post, child_category):
    updated_post = await post.update(category=child_category)
    assert updated_post.category_id == child_category.id


@pytest.mark.asyncio
async def test_post_thread_is_updated(post, child_category):
    other_thread = await Thread.create(
        child_category, "Test thread", starter_name="Guest"
    )
    updated_post = await post.update(thread=other_thread)
    assert updated_post.category_id == other_thread.category_id
    assert updated_post.thread_id == other_thread.id


@pytest.mark.asyncio
async def test_updating_post_thread_and_category_raises_value_error(
    post, child_category
):
    other_thread = await Thread.create(
        child_category, "Test thread", starter_name="Guest"
    )
    with pytest.raises(ValueError):
        await post.update(category=child_category, thread=other_thread)


@pytest.mark.asyncio
async def test_post_markup_is_updated(post):
    new_markup = "Hello"
    updated_post = await post.update(markup=new_markup)
    assert updated_post.markup == new_markup


@pytest.mark.asyncio
async def test_post_rich_text_is_updated(post):
    new_rich_text = {"new": True}
    updated_post = await post.update(rich_text=new_rich_text)
    assert updated_post.rich_text == new_rich_text


@pytest.mark.asyncio
async def test_post_poster_is_updated(post, user):
    updated_post = await post.update(poster=user)
    assert updated_post.poster_id == user.id
    assert updated_post.poster_name == user.name


@pytest.mark.asyncio
async def test_post_poster_name_is_updated(post):
    updated_post = await post.update(poster_name="User")
    assert updated_post.poster_id is None
    assert updated_post.poster_name == "User"


@pytest.mark.asyncio
async def test_post_poster_can_be_removed(post, user):
    post = await post.update(poster=user)
    updated_post = await post.update(poster_name="Guest")
    assert updated_post.poster_id is None
    assert updated_post.poster_name == "Guest"


@pytest.mark.asyncio
async def test_updating_post_poster_and_poster_name_raises_value_error(post, user):
    with pytest.raises(ValueError):
        await post.update(poster=user, poster_name=user.name)


@pytest.mark.asyncio
async def test_post_edits_count_is_updated(post):
    updated_post = await post.update(edits=5)
    assert updated_post.edits == 5


@pytest.mark.asyncio
async def test_post_edits_count_can_be_incremented(post):
    updated_post = await post.update(increment_edits=True)
    assert updated_post.edits == 1

    post_from_db = await post.fetch_from_db()
    assert post_from_db.edits == 1


@pytest.mark.asyncio
async def test_updating_and_incrementing_post_edits_raises_value_error(post):
    with pytest.raises(ValueError):
        await post.update(edits=5, increment_edits=True)


@pytest.mark.asyncio
async def test_post_date_is_updated(post):
    posted_at = timezone.now()
    updated_post = await post.update(posted_at=posted_at)
    assert updated_post.posted_at == posted_at


@pytest.mark.asyncio
async def test_post_extra_is_updated(post):
    new_extra = {"new": True}
    updated_post = await post.update(extra=new_extra)
    assert updated_post.extra == new_extra
