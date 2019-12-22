import pytest

from ..delete import delete_user
from ..get import get_user_by_id


@pytest.mark.asyncio
async def test_user_is_deleted(user):
    await delete_user(user)
    assert await get_user_by_id(user.id) is None
