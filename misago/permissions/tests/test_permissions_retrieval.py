import pytest

from ..permissions import CategoryPermission
from ..users import get_user_permissions


@pytest.mark.asyncio
async def test_user_permissions_without_cache_are_retrieved_from_database(
    context, user
):
    assert await get_user_permissions(context, user)


@pytest.mark.asyncio
async def test_user_permissions_retrieved_from_database_are_cached(
    context, user, mocker
):
    cache_set_mock = mocker.patch("misago.permissions.cache.cache.set")
    await get_user_permissions(context, user)
    cache_set_mock.assert_called_once()


@pytest.mark.asyncio
async def test_user_permissions_with_cache_skip_database(context, user, mocker):
    perms = {
        "core": ["FROM_DB"],
        "category": {
            CategoryPermission.SEE: [],
            CategoryPermission.READ: [],
            CategoryPermission.START: [],
            CategoryPermission.REPLY: [],
            CategoryPermission.DOWNLOAD: [],
            CategoryPermission.MODERATOR: [],
        },
    }

    cache_get_mock = mocker.patch(
        "misago.permissions.cache.cache.get", return_value=perms
    )
    build_user_permissions_mock = mocker.patch(
        "misago.permissions.users.build_user_permissions"
    )

    returned_perms = await get_user_permissions(context, user)
    cache_get_mock.assert_called_once()
    assert returned_perms == perms

    build_user_permissions_mock.assert_not_called()
