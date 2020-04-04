import pytest

from ...users.create import create_user


@pytest.fixture
async def deactivated_admin(db, user_password):
    return await create_user(
        "AdminDeactivated",
        "admindeactivated@example.com",
        password=user_password,
        is_admin=True,
        is_deactivated=True,
    )


@pytest.fixture
async def no_password_admin(db):
    return await create_user("NopassAdmin", "nopass-admin@example.com", is_admin=True)
