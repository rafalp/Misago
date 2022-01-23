import pytest

from ..users.models import User


@pytest.fixture
def user_password():
    return "t3st+p4ssw0rd!"


@pytest.fixture
async def user(db, user_password):
    return await User.create("User", "user@example.com", password=user_password)


@pytest.fixture
async def other_user(db, user_password):
    return await User.create(
        "OtherUser", "other-user@example.com", password=user_password
    )


@pytest.fixture
async def inactive_user(db, user_password):
    return await User.create(
        "User", "inactive@example.com", password=user_password, is_active=False
    )


@pytest.fixture
async def no_password_user(db):
    return await User.create("NopassUser", "nopass-user@example.com")


@pytest.fixture
async def moderator(db, user_password):
    return await User.create(
        "Moderator", "moderator@example.com", password=user_password, is_moderator=True
    )


@pytest.fixture
async def admin(db, user_password):
    return await User.create(
        "Admin", "admin@example.com", password=user_password, is_admin=True
    )
