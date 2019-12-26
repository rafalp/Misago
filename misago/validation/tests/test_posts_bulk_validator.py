import pytest

from ...errors import ErrorsList
from ..validators import PostExistsValidator, PostsBulkValidator


@pytest.mark.asyncio
async def test_bulk_posts_validator_validates_posts(post, user_post):
    errors = ErrorsList()
    context = {}
    validator = PostsBulkValidator([PostExistsValidator(context)])
    posts = await validator([post.id, user_post.id], errors, "posts")
    assert not errors
    assert posts == [post, user_post]


@pytest.mark.asyncio
async def test_bulk_posts_validator_partially_validates_posts(post):
    errors = ErrorsList()
    context = {}
    validator = PostsBulkValidator([PostExistsValidator(context)])
    posts = await validator([post.id, "1000"], errors, "posts")
    assert errors
    assert errors.get_errors_locations() == ["posts.1"]
    assert errors.get_errors_types() == ["value_error.post.not_exists"]
    assert posts == [post]
