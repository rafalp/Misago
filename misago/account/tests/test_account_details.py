from django.urls import reverse

from ...test import assert_contains, assert_has_success_message


def test_account_details_displays_login_required_page_to_anonymous_user(db, client):
    response = client.get(reverse("misago:account-details"))
    assert_contains(response, "Sign in to change your settings", status_code=401)


def test_account_details_renders_form(user_client):
    response = user_client.get(reverse("misago:account-details"))
    assert_contains(response, "Update profile details")


def test_account_details_form_clears_user_profile_fields(user, user_client):
    response = user_client.post(reverse("misago:account-details"))
    assert response.status_code == 302
    assert_has_success_message(response, "Profile updated")

    user.refresh_from_db()
    assert user.profile_fields == {}


def test_account_details_form_sets_user_profile_fields(user, user_client):
    response = user_client.post(
        reverse("misago:account-details"),
        {
            "real_name": "John Doe",
            "gender": "female",
            "bio": "Bio history",
            "twitter": "@example",
            "skype": "skype",
            "website": "http://example.com",
        },
    )
    assert response.status_code == 302
    assert_has_success_message(response, "Profile updated")

    user.refresh_from_db()
    assert user.profile_fields == {
        "real_name": "John Doe",
        "gender": "female",
        "bio": "Bio history",
        "twitter": "example",
        "skype": "skype",
        "website": "http://example.com",
    }


def test_account_details_form_validates_profile_fields(user, user_client):
    response = user_client.post(
        reverse("misago:account-details"),
        {
            "real_name": "John Doe",
            "gender": "female",
            "bio": "",
            "twitter": "invalid!",
            "skype": "skype",
            "extra": "skipped",
        },
    )
    assert response.status_code == 200
    assert_contains(response, "This is not a valid X handle.")


def test_account_details_form_skips_empty_profile_fields(user, user_client):
    response = user_client.post(
        reverse("misago:account-details"),
        {
            "real_name": "John Doe",
            "gender": "female",
            "bio": "",
            "twitter": "@example",
            "skype": "skype",
        },
    )
    assert response.status_code == 302
    assert_has_success_message(response, "Profile updated")

    user.refresh_from_db()
    assert user.profile_fields == {
        "real_name": "John Doe",
        "gender": "female",
        "twitter": "example",
        "skype": "skype",
    }


def test_account_details_form_skips_extra_profile_fields(user, user_client):
    response = user_client.post(
        reverse("misago:account-details"),
        {
            "real_name": "John Doe",
            "gender": "female",
            "bio": "",
            "twitter": "@example",
            "skype": "skype",
            "extra": "skipped",
        },
    )
    assert response.status_code == 302
    assert_has_success_message(response, "Profile updated")

    user.refresh_from_db()
    assert user.profile_fields == {
        "real_name": "John Doe",
        "gender": "female",
        "twitter": "example",
        "skype": "skype",
    }


def test_account_details_form_sets_user_profile_fields_in_htmx(user, user_client):
    response = user_client.post(
        reverse("misago:account-details"),
        {
            "real_name": "John Doe",
            "gender": "female",
            "bio": "",
            "twitter": "@example",
            "skype": "skype",
            "extra": "skipped",
        },
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Profile updated")

    user.refresh_from_db()
    assert user.profile_fields == {
        "real_name": "John Doe",
        "gender": "female",
        "twitter": "example",
        "skype": "skype",
    }
