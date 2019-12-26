import pytest

from ...errors import NotPostAuthorError
from ..validators import PostAuthorValidator


@pytest.mark.asyncio
async def test_validator_returns_user_post_if_current_user_is_its_author(
    user_graphql_context, user_post
):
    validator = PostAuthorValidator(user_graphql_context)
    assert await validator(user_post) == user_post


@pytest.mark.asyncio
async def test_validator_returns_user_post_if_current_user_is_moderator(
    moderator_graphql_context, user_post
):
    validator = PostAuthorValidator(moderator_graphql_context)
    assert await validator(user_post) == user_post


@pytest.mark.asyncio
async def test_validator_returns_guest_post_if_current_user_is_moderator(
    moderator_graphql_context, post
):
    validator = PostAuthorValidator(moderator_graphql_context)
    assert await validator(post) == post


@pytest.mark.asyncio
async def test_validator_raises_not_author_error_if_user_is_not_authenticated(
    graphql_context, user_post
):
    validator = PostAuthorValidator(graphql_context)
    with pytest.raises(NotPostAuthorError):
        assert await validator(user_post)


@pytest.mark.asyncio
async def test_validator_raises_not_author_error_if_user_is_not_other_user_post_owner(
    graphql_context, other_user_post
):
    validator = PostAuthorValidator(graphql_context)
    with pytest.raises(NotPostAuthorError):
        assert await validator(other_user_post)


@pytest.mark.asyncio
async def test_validator_raises_not_author_error_if_user_is_not_guest_post_owner(
    graphql_context, post
):
    validator = PostAuthorValidator(graphql_context)
    with pytest.raises(NotPostAuthorError):
        assert await validator(post)
