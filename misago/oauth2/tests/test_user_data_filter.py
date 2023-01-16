from unittest.mock import patch

from ..validation import filter_user_data


def test_new_user_data_is_filtered_using_default_filters(db, request):
    filtered_data = filter_user_data(
        request,
        None,
        {
            "id": "242132",
            "name": "New User",
            "email": "oauth2@example.com",
            "avatar": None,
        },
    )

    assert filtered_data == {
        "id": "242132",
        "name": "New_User",
        "email": "oauth2@example.com",
        "avatar": None,
    }


def test_existing_user_data_is_filtered_using_default_filters(user, request):
    filtered_data = filter_user_data(
        request,
        user,
        {
            "id": "242132",
            "name": user.username,
            "email": user.email,
            "avatar": None,
        },
    )

    assert filtered_data == {
        "id": "242132",
        "name": user.username,
        "email": user.email,
        "avatar": None,
    }


def user_request_filter(request, user, user_data):
    assert request


def user_id_filter(request, user, user_data):
    return {
        "id": "".join(reversed(user_data["id"])),
        "name": user_data["name"],
        "email": user_data["email"],
        "avatar": user_data["avatar"],
    }


def user_name_filter(request, user, user_data):
    return {
        "id": user_data["id"],
        "name": "".join(reversed(user_data["name"])),
        "email": user_data["email"],
        "avatar": user_data["avatar"],
    }


def user_email_filter(request, user, user_data):
    return {
        "id": user_data["id"],
        "name": user_data["name"],
        "email": "filtered_%s" % user_data["email"],
        "avatar": user_data["avatar"],
    }


def test_new_user_data_is_filtered_using_custom_filters(db, request):
    def user_is_none_filter(request, user, user_data):
        assert user is None

    with patch(
        "misago.oauth2.validation.oauth2_user_data_filters",
        [
            user_request_filter,
            user_is_none_filter,
            user_id_filter,
            user_name_filter,
            user_email_filter,
        ],
    ):
        filtered_data = filter_user_data(
            request,
            None,
            {
                "id": "1234",
                "name": "New User",
                "email": "oauth2@example.com",
                "avatar": None,
            },
        )

        assert filtered_data == {
            "id": "4321",
            "name": "resU weN",
            "email": "filtered_oauth2@example.com",
            "avatar": None,
        }


def test_existing_user_data_is_filtered_using_custom_filters(user, request):
    def user_is_set_filter(request, user_obj, user_data):
        assert user_obj == user
        return {
            "id": str(user_obj.id),
            "name": user_data["name"],
            "email": user_data["email"],
            "avatar": user_data["avatar"],
        }

    with patch(
        "misago.oauth2.validation.oauth2_user_data_filters",
        [
            user_request_filter,
            user_is_set_filter,
            user_id_filter,
            user_name_filter,
            user_email_filter,
        ],
    ):
        filtered_data = filter_user_data(
            request,
            user,
            {
                "id": "1234",
                "name": "New User",
                "email": "oauth2@example.com",
                "avatar": None,
            },
        )

        assert filtered_data == {
            "id": "".join(reversed(str(user.id))),
            "name": "resU weN",
            "email": "filtered_oauth2@example.com",
            "avatar": None,
        }
