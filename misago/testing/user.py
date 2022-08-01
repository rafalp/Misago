import pytest
import pytest_asyncio

from ..users.models import User, UserGroup


@pytest.fixture
def user_password():
    return "t3st+p4ssw0rd!"


@pytest_asyncio.fixture
async def user(db, user_password):
    return await User.create(
        "User",
        "user@example.com",
        password=user_password,
    )


@pytest_asyncio.fixture
async def other_user(db, user_password):
    return await User.create(
        "OtherUser",
        "other-user@example.com",
        password=user_password,
    )


@pytest_asyncio.fixture
async def inactive_user(db, user_password):
    return await User.create(
        "InactiveUser",
        "inactive@example.com",
        password=user_password,
        is_active=False,
    )


@pytest_asyncio.fixture
async def no_password_user(db):
    return await User.create("NopassUser", "nopass-user@example.com")


@pytest_asyncio.fixture
async def moderator(db, user_password):
    return await User.create(
        "Moderator",
        "moderator@example.com",
        password=user_password,
        is_moderator=True,
    )


@pytest_asyncio.fixture
async def admin(db, user_password, admins):
    return await User.create(
        "Admin",
        "admin@example.com",
        password=user_password,
        group=admins,
        is_admin=True,
    )


@pytest_asyncio.fixture
async def admins(db):
    return await UserGroup.query.one(is_admin=True)


@pytest_asyncio.fixture
async def moderators(db):
    return await UserGroup.query.one(is_admin=False, is_moderator=True)


@pytest_asyncio.fixture
async def members(db):
    return await UserGroup.query.one(is_default=True)


@pytest_asyncio.fixture
async def guests(db):
    return await UserGroup.query.one(is_guest=True)
