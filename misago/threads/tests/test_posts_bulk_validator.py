import pytest

from ...validation import ErrorsList
from ..validators import PostExistsValidator, PostsBulkValidator


@pytest.mark.asyncio
async def test_bulk_posts_validator_validates_posts(graphql_context, post, user_post):
    errors = ErrorsList()
    validator = PostsBulkValidator([PostExistsValidator(graphql_context)])
    posts = await validator([post.id, user_post.id], errors, "posts")

    assert not errors
    assert posts == [post, user_post]


@pytest.mark.asyncio
async def test_bulk_posts_validator_partially_validates_posts(graphql_context, post):
    errors = ErrorsList()
    validator = PostsBulkValidator([PostExistsValidator(graphql_context)])
    posts = await validator([post.id, post.id + 1], errors, "posts")

    assert errors == [
        {
            "loc": "posts.1",
            "type": "post_error.not_found",
            "msg": f"post with id '{post.id + 1}' could not be found",
        },
    ]
    assert posts == [post]
