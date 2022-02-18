import pytest

from ..errors import PostNotAuthorError
from ..validators import PostAuthorValidator


@pytest.mark.asyncio
async def test_validator_returns_user_post_if_current_user_is_its_author(
    user_context, user_post
):
    validator = PostAuthorValidator(user_context)
    assert await validator(user_post) == user_post


@pytest.mark.asyncio
async def test_validator_returns_user_post_if_current_user_is_moderator(
    moderator_context, user_post
):
    validator = PostAuthorValidator(moderator_context)
    assert await validator(user_post) == user_post


@pytest.mark.asyncio
async def test_validator_returns_guest_post_if_current_user_is_moderator(
    moderator_context, post
):
    validator = PostAuthorValidator(moderator_context)
    assert await validator(post) == post


@pytest.mark.asyncio
async def test_validator_raises_not_author_error_if_user_is_not_authenticated(
    context, user_post
):
    validator = PostAuthorValidator(context)
    with pytest.raises(PostNotAuthorError):
        assert await validator(user_post)


@pytest.mark.asyncio
async def test_validator_raises_not_author_error_if_user_is_not_other_user_post_owner(
    context, other_user_post
):
    validator = PostAuthorValidator(context)
    with pytest.raises(PostNotAuthorError):
        assert await validator(other_user_post)


@pytest.mark.asyncio
async def test_validator_raises_not_author_error_if_user_is_not_guest_post_owner(
    context, post
):
    validator = PostAuthorValidator(context)
    with pytest.raises(PostNotAuthorError):
        assert await validator(post)
