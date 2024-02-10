from unittest.mock import Mock, patch
from urllib.parse import parse_qsl, urlparse

from ...conf.test import override_dynamic_settings
from ..client import (
    SESSION_CODE_VERIFIER,
    SESSION_STATE,
    create_login_url,
)


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


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="some scopes",
    oauth2_login_url="https://example.com/oauth2/login",
    oauth2_enable_pkce=True,
)
def test_oauth2_login_url_is_created_with_pkce(dynamic_settings):
    code_verifier = "SF01jh"
    code_challenge = "eemb2YInusdSF01jhCXpzV_juX3_xdAQnVU1oCvFBA"

    request = Mock(
        session={},
        settings=dynamic_settings,
        build_absolute_uri=lambda url: f"http://mysite.com{url or ''}",
    )

    with patch(
        "misago.oauth2.client.get_code_challenge", return_value=code_challenge
    ), patch("misago.oauth2.client.token_urlsafe", return_value=code_verifier):
        login_url = create_login_url(request)

    # State set in session?
    assert request.session.get(SESSION_STATE)
    assert request.session.get(SESSION_CODE_VERIFIER) == code_verifier

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
        ("code_challenge", code_challenge),
        ("code_challenge_method", "S256"),
    ]
