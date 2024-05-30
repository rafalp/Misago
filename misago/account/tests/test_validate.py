import json

from django.urls import reverse


def test_validate_views_return_400_if_method_is_not_post(db, client):
    response = client.get(reverse("misago:account-validate-username"))
    assert response.status_code == 400


def test_validate_views_return_400_if_value_is_missing(db, client):
    response = client.post(reverse("misago:account-validate-username"))
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": ["'value' can't be empty."],
    }


def test_validate_views_return_400_if_value_is_empty(db, client):
    response = client.post(reverse("misago:account-validate-username"), {"value": ""})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": ["'value' can't be empty."],
    }


def test_validate_views_return_400_if_user_is_not_valid_int(db, client):
    response = client.post(
        reverse("misago:account-validate-username"), {"value": "Joh", "user": "invalid"}
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": ["'user' must be a positive integer."],
    }


def test_validate_views_return_400_if_user_is_not_positive_int(db, client):
    response = client.post(
        reverse("misago:account-validate-username"), {"value": "Joh", "user": "-5"}
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": ["'user' must be a positive integer."],
    }


def test_validate_username_view_returns_validation_errors(db, client):
    response = client.post(
        reverse("misago:account-validate-username"), {"value": "Jo!"}
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": [
            "Username can only contain Latin alphabet letters, digits, and an underscore sign."
        ],
    }


def test_validate_username_view_returns_no_errors_for_valid_name(db, client):
    response = client.post(
        reverse("misago:account-validate-username"), {"value": "Valid"}
    )
    assert response.status_code == 200
    assert json.loads(response.content) == {"errors": []}


def test_validate_username_view_validates_username_availability(db, client, user):
    response = client.post(
        reverse("misago:account-validate-username"), {"value": user.username}
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": ["This username is not available."]
    }


def test_validate_username_view_validates_username_availability_for_user(
    db, client, user
):
    response = client.post(
        reverse("misago:account-validate-username"),
        {"value": user.username, "user": str(user.id)},
    )
    assert response.status_code == 200
    assert json.loads(response.content) == {"errors": []}


def test_validate_email_view_returns_validation_errors(db, client):
    response = client.post(
        reverse("misago:account-validate-email"), {"value": "invalid"}
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": ["Enter a valid e-mail address."],
    }


def test_validate_email_view_returns_no_errors_for_valid_email(db, client):
    response = client.post(
        reverse("misago:account-validate-email"), {"value": "valid@example.com"}
    )
    assert response.status_code == 200
    assert json.loads(response.content) == {"errors": []}


def test_validate_email_view_validates_email_availability(db, client, user):
    response = client.post(
        reverse("misago:account-validate-email"), {"value": user.email}
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": ["This e-mail address is not available."]
    }


def test_validate_email_view_validates_email_availability_for_user(db, client, user):
    response = client.post(
        reverse("misago:account-validate-email"),
        {"value": user.email, "user": str(user.id)},
    )
    assert response.status_code == 200
    assert json.loads(response.content) == {"errors": []}


def test_validate_password_view_returns_validation_errors(db, client):
    response = client.post(reverse("misago:account-validate-password"), {"value": "p"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": [
            "This password is too short. It must contain at least 7 characters."
        ],
    }


def test_validate_password_view_returns_no_errors_for_valid_password(db, client):
    response = client.post(
        reverse("misago:account-validate-password"), {"value": "l0r3m1p5um"}
    )
    assert response.status_code == 200
    assert json.loads(response.content) == {"errors": []}
