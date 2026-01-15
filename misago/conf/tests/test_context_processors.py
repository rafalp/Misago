from unittest.mock import Mock

from ..context_processors import conf
from ..test import override_dynamic_settings


def test_request_settings_are_included_in_template_context(db, dynamic_settings):
    mock_request = Mock(settings=dynamic_settings)
    context_settings = conf(mock_request)["settings"]
    assert context_settings == mock_request.settings


def test_settings_are_included_in_frontend_context(db, client):
    response = client.get("/")
    assert response.status_code == 200
    assert '"SETTINGS": {"' in response.content.decode("utf-8")


def test_admin_panel_link_is_included_in_frontend_context_for_admins(admin_client):
    response = admin_client.get("/")
    assert response.status_code == 200
    assert '"ADMIN_URL": "' in response.content.decode("utf-8")


@override_dynamic_settings(show_admin_panel_link_in_ui=False)
def test_admin_panel_link_is_excluded_from_frontend_context_for_admins_if_disabled(
    admin_client,
):
    response = admin_client.get("/")
    assert response.status_code == 200
    assert '"ADMIN_URL": "' not in response.content.decode("utf-8")


def test_admin_panel_link_is_excluded_from_frontend_context_for_staff_users(
    staff_client,
):
    response = staff_client.get("/")
    assert response.status_code == 200
    assert '"ADMIN_URL": "' not in response.content.decode("utf-8")


def test_admin_panel_link_is_excluded_from_frontend_context_for_users(user_client):
    response = user_client.get("/")
    assert response.status_code == 200
    assert '"ADMIN_URL": "' not in response.content.decode("utf-8")


def test_admin_panel_link_is_excluded_from_frontend_context_for_anonymous_users(
    db, client
):
    response = client.get("/")
    assert response.status_code == 200
    assert '"ADMIN_URL": "' not in response.content.decode("utf-8")
