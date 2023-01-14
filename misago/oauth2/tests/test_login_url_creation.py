from unittest.mock import Mock
from urllib.parse import parse_qsl, urlparse

from ...conf.test import override_dynamic_settings
from ..client import SESSION_STATE, create_login_url


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="some scopes",
    oauth2_login_url="https://example.com/oauth2/login",
)
def test_oauth2_login_url_is_created(dynamic_settings):
    request = Mock(
        session={},
        settings=dynamic_settings,
        build_absolute_uri=lambda url: f"http://mysite.com{url or ''}",
    )

    login_url = create_login_url(request)

    # State set in session?
    assert request.session.get(SESSION_STATE)

    # Redirect url is valid?
    redirect_to = urlparse(login_url)
    assert redirect_to.netloc == "example.com"
    assert redirect_to.path == "/oauth2/login"
    assert parse_qsl(redirect_to.query) == [
        ("response_type", "code"),
        ("client_id", "clientid123"),
        ("redirect_uri", "http://mysite.com/oauth2/complete/"),
        ("scope", "some scopes"),
        ("state", request.session[SESSION_STATE]),
    ]
