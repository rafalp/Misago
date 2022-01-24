import pytest

from ...threads.models import Post, Thread
from ..contents import delete_categories_contents


@pytest.mark.asyncio
async def test_category_threads_and_posts_are_deleted(category, thread, post):
    assert thread.category_id == category.id
    assert post.category_id == category.id

    await delete_categories_contents([category])

    with pytest.raises(Thread.DoesNotExist):
        await thread.fetch_from_db()

    with pytest.raises(Post.DoesNotExist):
        await post.fetch_from_db()


@pytest.mark.asyncio
async def test_other_categories_threads_and_posts_are_excluded_from_delete(
    category,
    closed_category,
    closed_category_thread,
    closed_category_post,
):
    assert closed_category_thread.category_id == closed_category.id
    assert closed_category_post.category_id == closed_category.id

    await delete_categories_contents([category])

    assert await closed_category_thread.fetch_from_db()
    assert await closed_category_post.fetch_from_db()
