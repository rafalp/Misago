import pytest

from misago.threads.models import Post, Thread
from misago.users.models import User

from ..history import create_fake_forum_history


@pytest.mark.asyncio
async def test_fake_forum_history_is_created(db, faker):
    async for action in create_fake_forum_history(faker, 10, 10):
        assert isinstance(action, (Post, Thread, User))


@pytest.mark.asyncio
async def test_pre_existing_users_are_moved_to_past_by_history_creator(user, faker):
    async for _ in create_fake_forum_history(faker, 1, 1):
        pass

    updated_user = await User.query.one(id=user.id)
    assert updated_user.joined_at < user.joined_at
