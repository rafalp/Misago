from urllib.parse import urlparse

from itsdangerous.timed import TimestampSigner
from requests import Response
from requests.sessions import Session

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import override_settings, TestCase
from django.utils.timezone import now

from ..conf.test import override_dynamic_settings

User = get_user_model()

TEST_SSO_SETTINGS = {
    "enable_sso": True,
    "sso_private_key": "priv1",
    "sso_public_key": "fakeSsoPublicKey",
    "sso_server": "http://example.com/server/",
}

SSO_USER_EMAIL = "jkowalski@example.com"


class ConnectionMock:
    def __init__(self):
        self.session = Session

    def __enter__(self):
        self.origin_post = Session.post

        def mocked_post(*args, **kwargs):
            mocked_response = Response()
            requested_url = args[1]
            if "/server/request-token/" == urlparse(requested_url).path:
                # token generated for private key settings.SSO_PRIVATE_KEY = 'priv1'
                mocked_response._content = (
                    b'{"request_token": "XcHtuemqcjnIT6J2WHTFswLQP0W07nI96XfxqGkm6b1zFToF0YGEoIYu3'
                    b'7QOajkc"}.XTd9sA.quRsXFxqMk-ufwSc79q-_YLDNzg'
                )
            elif "/server/verify/" == urlparse(requested_url).path:
                mocked_response._content = (
                    (
                        '{"username": "jkowalski", "email": "%s", "first_name": '
                        '"Jan", "last_name": "Kowalski", "is_staff": false, "is_superuser": false, '
                        '"is_active": true}.XTg4IQ._cANZR5jHvtwhNzcnNYDfE1nLHE'
                    )
                    % SSO_USER_EMAIL
                ).encode("utf-8")

            mocked_response.status_code = 200
            return mocked_response

        setattr(self.session, "post", mocked_post)
        return self.session

    def __exit__(self, type, value, traceback):
        setattr(self.session, "post", self.origin_post)


class TimestampSignerMock:
    def __init__(self):
        self.TimestampSigner = TimestampSigner

    def __enter__(self):
        self.origin_unsign = TimestampSigner.unsign

        def mocked_unsign(*args, **kwargs):
            s = args[1]
            if b'"username": "jkowalski"' in s:
                value = s[:166]  # {...}
                timestamp_to_datetime = now()
                return value, timestamp_to_datetime
            else:
                return self.origin_unsign(*args, **kwargs)

        setattr(self.TimestampSigner, "unsign", mocked_unsign)
        return self.TimestampSigner

    def __exit__(self, type, value, traceback):
        setattr(self.TimestampSigner, "unsign", self.origin_unsign)


@override_dynamic_settings(enable_sso=False)
def test_sso_login_view_returns_404_if_sso_is_disabled(db, client):
    url_to_external_logging = reverse("simple-sso-login")
    assert url_to_external_logging == "/sso/client/"

    response = client.get(url_to_external_logging)
    assert response.status_code == 404


@override_dynamic_settings(**TEST_SSO_SETTINGS)
def test_sso_login_view_initiates_auth_flow(db, client):
    url_to_external_logging = reverse("simple-sso-login")
    assert url_to_external_logging == "/sso/client/"

    with ConnectionMock():
        response = client.get(url_to_external_logging)

    assert response.status_code == 302

    url_parsed = urlparse(response.url)
    assert url_parsed.path == "/server/authorize/"
    assert url_parsed.query == (
        "token=XcHtuemqcjnIT6J2WHTFswLQP0W07nI96XfxqGkm6b1zFToF0YGEoIYu37QOajkc"
    )


@override_dynamic_settings(enable_sso=False)
def test_sso_auth_view_returns_404_if_sso_is_disabled(db, client):
    url_to_authenticate = reverse("simple-sso-authenticate")
    assert url_to_authenticate == "/sso/client/authenticate/"

    response = client.get(url_to_authenticate)
    assert response.status_code == 404


@override_dynamic_settings(**TEST_SSO_SETTINGS)
def test_sso_auth_view_creates_new_user(db, client):
    url_to_authenticate = reverse("simple-sso-authenticate")
    assert url_to_authenticate == "/sso/client/authenticate/"

    query = (
        "next=%2F&access_token=InBBMjllMlNla2ZWdDdJMnR0c3R3QWIxcjQwRzV6TmphZDRSaEprbjlMbnR0TnF"
        "Ka3Q2d1dNR1lVYkhzVThvZU0i.XTeRVQ.3XiIMg0AFcJKDFCekse6s43uNLI"
    )
    url_to_authenticate += "?" + query

    with ConnectionMock():
        with TimestampSignerMock():
            response = client.get(url_to_authenticate)

    assert response.status_code == 302
    assert response.url == "/"

    user = User.objects.first()
    assert user.username == "jkowalski"


@override_dynamic_settings(**TEST_SSO_SETTINGS)
def test_sso_auth_view_authenticates_existing_user(user, client):
    user.set_email(SSO_USER_EMAIL)
    user.save()

    url_to_authenticate = reverse("simple-sso-authenticate")
    assert url_to_authenticate == "/sso/client/authenticate/"

    query = (
        "next=%2F&access_token=InBBMjllMlNla2ZWdDdJMnR0c3R3QWIxcjQwRzV6TmphZDRSaEprbjlMbnR0TnF"
        "Ka3Q2d1dNR1lVYkhzVThvZU0i.XTeRVQ.3XiIMg0AFcJKDFCekse6s43uNLI"
    )
    url_to_authenticate += "?" + query

    with ConnectionMock():
        with TimestampSignerMock():
            response = client.get(url_to_authenticate)

    assert response.status_code == 302
    assert response.url == "/"

    assert User.objects.count() == 1
