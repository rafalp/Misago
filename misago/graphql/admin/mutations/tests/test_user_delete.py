import pytest

from .....threads.models import Post, Thread
from .....users.models import User

USER_DELETE_MUTATION = """
    mutation UserDelete($id: ID!, $deleteContent: Boolean) {
        userDelete(user: $id, deleteContent: $deleteContent) {
            deleted
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_user_delete_mutation_deletes_user(query_admin_api, user):
    result = await query_admin_api(
        USER_DELETE_MUTATION,
        {
            "id": str(user.id),
        },
    )

    assert result["data"]["userDelete"] == {
        "deleted": True,
        "errors": None,
    }

    with pytest.raises(User.DoesNotExist):
        await user.refresh_from_db()


@pytest.mark.asyncio
async def test_user_delete_mutation_leaves_user_content(
    query_admin_api, user, user_thread, user_post
):
    result = await query_admin_api(
        USER_DELETE_MUTATION,
        {
            "id": str(user.id),
        },
    )

    assert result["data"]["userDelete"] == {
        "deleted": True,
        "errors": None,
    }

    with pytest.raises(User.DoesNotExist):
        await user.refresh_from_db()

    await user_thread.refresh_from_db()
    await user_post.refresh_from_db()


@pytest.mark.asyncio
async def test_user_delete_mutation_deletes_user_content(
    query_admin_api, user, user_thread, user_post
):
    result = await query_admin_api(
        USER_DELETE_MUTATION,
        {
            "id": str(user.id),
            "deleteContent": True,
        },
    )

    assert result["data"]["userDelete"] == {
        "deleted": True,
        "errors": None,
    }

    with pytest.raises(User.DoesNotExist):
        await user.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        await user_thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        await user_post.refresh_from_db()


@pytest.mark.asyncio
async def test_user_delete_mutation_fails_if_user_id_is_invalid(query_admin_api):
    result = await query_admin_api(
        USER_DELETE_MUTATION,
        {
            "id": "invalid",
        },
    )

    assert result["data"]["userDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "user",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_delete_mutation_fails_if_user_tries_to_delete_non_existing_user(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_DELETE_MUTATION,
        {
            "id": str(user.id + 100),
        },
    )

    assert result["data"]["userDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "user",
                "type": "value_error.user.not_found",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_delete_mutation_fails_if_user_tries_to_delete_self(
    query_admin_api, admin
):
    result = await query_admin_api(
        USER_DELETE_MUTATION,
        {
            "id": str(admin.id),
        },
    )

    assert result["data"]["userDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "user",
                "type": "value_error.user.delete_self",
            },
        ],
    }

    await admin.refresh_from_db()


@pytest.mark.asyncio
async def test_user_delete_mutation_fails_if_user_tries_to_delete_admin(
    query_admin_api, user
):
    await user.update(is_admin=True)

    result = await query_admin_api(
        USER_DELETE_MUTATION,
        {
            "id": str(user.id),
        },
    )

    assert result["data"]["userDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "user",
                "type": "value_error.user.is_protected",
            },
        ],
    }

    await user.refresh_from_db()


@pytest.mark.asyncio
async def test_user_delete_mutation_requires_admin_auth(query_admin_api, user):
    result = await query_admin_api(
        USER_DELETE_MUTATION,
        {
            "id": str(user.id),
        },
        include_auth=False,
        expect_error=True,
    )

    assert result["data"] is None
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
