import pytest

from ...errors import PostsThreadsDifferError
from ..validators import PostsInSameThreadBulkValidator


@pytest.mark.asyncio
async def test_validator_allows_single_post(post):
    validator = PostsInSameThreadBulkValidator({})
    assert await validator([post]) == [post]


@pytest.mark.asyncio
async def test_validator_allows_empty_posts_list():
    validator = PostsInSameThreadBulkValidator({})
    assert await validator([]) == []


@pytest.mark.asyncio
async def test_validator_allows_multiple_posts_in_same_thread(post, reply):
    context = {}
    validator = PostsInSameThreadBulkValidator(context)
    assert await validator([post, reply]) == [post, reply]


@pytest.mark.asyncio
async def test_validator_raises_different_threads_error_if_posts_threads_differ(
    post, closed_thread_post
):
    context = {}
    validator = PostsInSameThreadBulkValidator(context)
    with pytest.raises(PostsThreadsDifferError):
        await validator([post, closed_thread_post])
