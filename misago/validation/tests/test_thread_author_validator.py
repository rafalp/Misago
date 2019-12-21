import pytest

from ...errors import NotThreadAuthorError
from ..validators import IsThreadAuthorValidator


@pytest.mark.asyncio
async def test_validator_returns_user_thread_if_current_user_is_its_author(
    user_graphql_context, user_thread
):
    validator = IsThreadAuthorValidator(user_graphql_context)
    assert await validator(user_thread) == user_thread


@pytest.mark.asyncio
async def test_validator_returns_user_thread_if_current_user_is_moderator(
    moderator_graphql_context, user_thread
):
    validator = IsThreadAuthorValidator(moderator_graphql_context)
    assert await validator(user_thread) == user_thread


@pytest.mark.asyncio
async def test_validator_returns_guest_thread_if_current_user_is_moderator(
    moderator_graphql_context, thread
):
    validator = IsThreadAuthorValidator(moderator_graphql_context)
    assert await validator(thread) == thread


@pytest.mark.asyncio
async def test_validator_raises_not_author_error_if_user_is_not_authenticated(
    graphql_context, user_thread
):
    validator = IsThreadAuthorValidator(graphql_context)
    with pytest.raises(NotThreadAuthorError):
        assert await validator(user_thread)


@pytest.mark.asyncio
async def test_validator_raises_not_author_error_if_user_is_not_other_user_thread_owner(
    graphql_context, other_user_thread
):
    validator = IsThreadAuthorValidator(graphql_context)
    with pytest.raises(NotThreadAuthorError):
        assert await validator(other_user_thread)


@pytest.mark.asyncio
async def test_validator_raises_not_author_error_if_user_is_not_guest_thread_owner(
    graphql_context, thread
):
    validator = IsThreadAuthorValidator(graphql_context)
    with pytest.raises(NotThreadAuthorError):
        assert await validator(thread)
