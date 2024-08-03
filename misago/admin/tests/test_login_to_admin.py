from django.urls import reverse

from ...test import assert_contains
from ..auth import is_admin_authorized

admin_link = reverse("misago:admin:index")


def test_login_form_is_displayed(db, client):
    response = client.get(admin_link)
    assert response.status_code == 200
    assert_contains(response, "Administration")
    assert_contains(response, "Sign in")
    assert_contains(response, "Username or email")
    assert_contains(response, "Password")


def test_attempt_to_login_using_invalid_credentials_fails(db, client):
    response = client.post(admin_link, {"username": "no", "password": "no"})
    assert_contains(response, "Login or password is incorrect.")


def test_attempt_to_login_using_invalid_password_fails(client, admin):
    response = client.post(admin_link, {"username": admin.username, "password": "no"})
    assert_contains(response, "Login or password is incorrect.")


def test_attempt_to_login_without_admin_status_fails(client, user, user_password):
    response = client.post(
        admin_link, {"username": user.username, "password": user_password}
    )
    assert_contains(response, "Your account does not have admin privileges.")


def test_attempt_to_login_as_django_staff_user_fails(client, user, user_password):
    user.is_staff = True
    user.save()

    response = client.post(
        admin_link, {"username": user.username, "password": user_password}
    )
    assert_contains(response, "Your account does not have admin privileges.")


def test_attempt_to_login_as_django_superuser_user_fails(
    client, superuser, user_password
):
    response = client.post(
        admin_link, {"username": superuser.username, "password": user_password}
    )
    assert_contains(response, "Your account does not have admin privileges.")


def test_attempt_to_login_as_django_non_staff_superuser_user_fails(
    client, superuser, user_password
):
    superuser.is_staff = False
    superuser.save()

    response = client.post(
        admin_link, {"username": superuser.username, "password": user_password}
    )
    assert_contains(response, "Your account does not have admin privileges.")


def test_user_with_admin_status_is_logged_to_admin(client, admin, user_password):
    response = client.post(
        admin_link, {"username": admin.username, "password": user_password}
    )
    assert is_admin_authorized(response.wsgi_request)
    assert response.wsgi_request.user == admin


def test_user_with_root_admin_status_is_logged_to_admin(
    client, root_admin, user_password
):
    response = client.post(
        admin_link, {"username": root_admin.username, "password": user_password}
    )
    assert is_admin_authorized(response.wsgi_request)
    assert response.wsgi_request.user == root_admin


def test_login_form_redirects_user_to_admin_index_after_successful_login(
    client, admin, user_password
):
    response = client.post(
        admin_link, {"username": admin.username, "password": user_password}
    )
    assert response["location"] == admin_link
