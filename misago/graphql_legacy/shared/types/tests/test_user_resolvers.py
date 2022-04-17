from unittest.mock import ANY

import pytest

from .....conf import settings


@pytest.mark.asyncio
async def test_user_avatars_list_is_resolved(query_public_api, user):
    query = """
        query GetUser($user: ID!) {
            user(id: $user) {
                id
                avatars {
                    size
                    url
                }
            }
        }
    """

    result = await query_public_api(query, {"user": str(user.id)})
    assert result["data"]["user"] == {
        "id": str(user.id),
        "avatars": [
            {
                "size": 400,
                "url": ANY,
            },
            {
                "size": 200,
                "url": ANY,
            },
            {
                "size": 150,
                "url": ANY,
            },
            {
                "size": 100,
                "url": ANY,
            },
            {
                "size": 64,
                "url": ANY,
            },
            {
                "size": 50,
                "url": ANY,
            },
            {
                "size": 30,
                "url": ANY,
            },
        ],
    }


USER_AVATAR_QUERY = """
    query GetUser($user: ID!, $size: Int) {
        user(id: $user) {
            id
            avatar(size: $size) {
                size
                url
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_user_avatar_is_resolved_to_largest_avatar_by_default(
    query_public_api, user
):
    result = await query_public_api(USER_AVATAR_QUERY, {"user": str(user.id)})
    assert result["data"]["user"] == {
        "id": str(user.id),
        "avatar": {
            "size": max(settings.avatar_sizes),
            "url": ANY,
        },
    }


@pytest.mark.asyncio
async def test_user_avatar_is_resolved_to_specified_size(query_public_api, user):
    result = await query_public_api(
        USER_AVATAR_QUERY, {"user": str(user.id), "size": 100}
    )
    assert result["data"]["user"] == {
        "id": str(user.id),
        "avatar": {
            "size": 100,
            "url": ANY,
        },
    }
