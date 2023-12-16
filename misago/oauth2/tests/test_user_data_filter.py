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


def test_empty_user_name_is_replaced_with_placeholder_one(db, request):
    filtered_data = filter_user_data(
        request,
        None,
        {
            "id": "242132",
            "name": None,
            "email": "oauth2@example.com",
            "avatar": None,
        },
    )

    assert filtered_data["name"].strip()


def test_missing_user_name_is_replaced_with_placeholder_one(db, request):
    filtered_data = filter_user_data(
        request,
        None,
        {
            "id": "242132",
            "name": None,
            "email": "oauth2@example.com",
            "avatar": None,
        },
    )

    assert filtered_data["name"].strip()


def test_missing_user_email_is_set_as_empty_str(db, request):
    filtered_data = filter_user_data(
        request,
        None,
        {
            "id": "242132",
            "name": "New User",
            "email": None,
            "avatar": None,
        },
    )

    assert filtered_data == {
        "id": "242132",
        "name": "New_User",
        "email": "",
        "avatar": None,
    }


def test_original_user_data_is_not_mutated_by_default_filters(user, request):
    user_data = {
        "id": "1234",
        "name": "New User",
        "email": "oauth2@example.com",
        "avatar": None,
    }

    filtered_data = filter_user_data(request, user, user_data)
    assert filtered_data == {
        "id": "1234",
        "name": "New_User",
        "email": "oauth2@example.com",
        "avatar": None,
    }

    assert user_data == {
        "id": "1234",
        "name": "New User",
        "email": "oauth2@example.com",
        "avatar": None,
    }
