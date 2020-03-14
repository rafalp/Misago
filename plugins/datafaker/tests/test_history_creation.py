import pytest
from misago.users.get import get_user_by_id
from misago.types import Post, Thread, User

from ..history import create_fake_forum_history


@pytest.mark.asyncio
async def test_fake_forum_history_is_created(db, faker):
    async for action in create_fake_forum_history(faker, 10, 10):
        assert isinstance(action, (Post, Thread, User))


@pytest.mark.asyncio
async def test_pre_existing_users_are_moved_to_past_by_history_creator(user, faker):
    async for _ in create_fake_forum_history(faker, 1, 1):
        pass

    updated_user = await get_user_by_id(user.id)
    assert updated_user.joined_at < user.joined_at
