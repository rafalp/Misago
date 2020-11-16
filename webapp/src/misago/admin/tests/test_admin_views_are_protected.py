from django.urls import reverse

from ...test import assert_contains, assert_not_contains
from ..auth import is_admin_authorized

admin_link = reverse("misago:admin:index")


def assert_requires_admin_login(response):
    assert response.status_code == 200
    assert_contains(response, "Administration")
    assert_contains(response, "Sign in")


def test_anonymous_user_is_asked_to_login_to_access_admin_view(db, client):
    response = client.get(admin_link)
    assert_requires_admin_login(response)


def test_authenticated_user_is_asked_to_login_to_access_admin_view(client, user):
    client.force_login(user)
    response = client.get(admin_link)
    assert_requires_admin_login(response)


def test_unathorized_admin_is_asked_to_login_to_access_admin_view(client, superuser):
    client.force_login(superuser)
    response = client.get(admin_link)
    assert_requires_admin_login(response)


def test_authorized_admin_is_allowed_to_access_admin_view(admin_client):
    response = admin_client.get(admin_link)
    assert is_admin_authorized(response.wsgi_request)
    assert_not_contains(response, "Sign in")


def test_admin_authorization_is_checked_on_admin_view_access(mocker, client, user):
    admin_authorization = mocker.patch(
        "misago.admin.middleware.is_admin_authorized", return_value=False
    )
    response = client.get(admin_link)
    admin_authorization.assert_called_once_with(response.wsgi_request)
