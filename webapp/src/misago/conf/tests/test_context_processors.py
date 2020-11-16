from unittest.mock import Mock

from ..context_processors import conf


def test_request_settings_are_included_in_template_context(db, dynamic_settings):
    mock_request = Mock(settings=dynamic_settings)
    context_settings = conf(mock_request)["settings"]
    assert context_settings == mock_request.settings


def test_settings_are_included_in_frontend_context(db, client):
    response = client.get("/")
    assert response.status_code == 200
    assert '"SETTINGS": {"' in response.content.decode("utf-8")
