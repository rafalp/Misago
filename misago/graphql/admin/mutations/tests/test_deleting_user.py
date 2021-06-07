import pytest

from .....users.models import User
from ..deleteuser import resolve_delete_user


@pytest.mark.asyncio
async def test_delete_user_mutation_deletes_user(admin_graphql_info, user):
    data = await resolve_delete_user(
        None,
        admin_graphql_info,
        user=str(user.id),
    )

    assert not data.get("errors")
    assert data["deleted"]

    with pytest.raises(User.DoesNotExist):
        await user.refresh_from_db()


@pytest.mark.asyncio
async def test_delete_user_mutation_leaves_user_content(admin_graphql_info, user):
    data = await resolve_delete_user(
        None,
        admin_graphql_info,
        user=str(user.id),
    )

    assert not data.get("errors")
    assert data["deleted"]

    with pytest.raises(User.DoesNotExist):
        await user.refresh_from_db()


@pytest.mark.asyncio
async def test_delete_user_mutation_fails_if_user_id_is_invalid(
    admin_graphql_info, user
):
    data = await resolve_delete_user(
        None,
        admin_graphql_info,
        user="invalid",
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["user"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_delete_user_mutation_fails_if_user_tries_to_delete_non_existing_user(
    admin_graphql_info, user
):
    data = await resolve_delete_user(
        None,
        admin_graphql_info,
        user=str(user.id + 100),
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["user"]
    assert data["errors"].get_errors_types() == ["value_error.user.not_exists"]


@pytest.mark.asyncio
async def test_delete_user_mutation_fails_if_user_tries_to_delete_self(
    admin_graphql_info, admin
):
    data = await resolve_delete_user(
        None,
        admin_graphql_info,
        user=str(admin.id),
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["user"]
    assert data["errors"].get_errors_types() == ["value_error.user.delete_self"]

    await admin.refresh_from_db()


@pytest.mark.asyncio
async def test_delete_user_mutation_fails_if_user_tries_to_delete_admin(
    admin_graphql_info, user
):
    await user.update(is_administrator=True)

    data = await resolve_delete_user(
        None,
        admin_graphql_info,
        user=str(user.id),
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["user"]
    assert data["errors"].get_errors_types() == ["value_error.user.is_protected"]

    await user.refresh_from_db()
