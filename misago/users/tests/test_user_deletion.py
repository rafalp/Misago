import pytest

from ..models import User


@pytest.mark.asyncio
async def test_user_is_deleted(user):
    await user.delete()

    with pytest.raises(User.DoesNotExist):
        await User.query.one(id=user.id)
