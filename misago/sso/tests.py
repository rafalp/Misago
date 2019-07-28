from itsdangerous.timed import TimestampSigner
from requests import Response
from requests.sessions import Session
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import override_settings, TestCase
from django.utils.timezone import now

User = get_user_model()


class ConnectionMock:
    def __init__(self):
        self.Session = Session

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
                    b'{"username": "jkowalski", "email": "jkowalski@example.com", "first_name": '
                    b'"Jan", "last_name": "Kowalski", "is_staff": false, "is_superuser": false, '
                    b'"is_active": true}.XTg4IQ._cANZR5jHvtwhNzcnNYDfE1nLHE'
                )

            mocked_response.status_code = 200
            return mocked_response

        setattr(self.Session, "post", mocked_post)
        return self.Session

    def __exit__(self, type, value, traceback):
        setattr(self.Session, "post", self.origin_post)


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


class SsoModuleTestCase(TestCase):
    def test_sso_client(self):
        url_to_external_logging = reverse("simple-sso-login")
        self.assertEqual("/sso/client/", url_to_external_logging)

        with ConnectionMock():
            response = self.client.get(url_to_external_logging)

        self.assertEqual(302, response.status_code)

        url_parsed = urlparse(response.url)
        self.assertEqual("/server/authorize/", url_parsed.path)
        self.assertEqual(
            "token=XcHtuemqcjnIT6J2WHTFswLQP0W07nI96XfxqGkm6b1zFToF0YGEoIYu37QOajkc",
            url_parsed.query,
        )

    def test_sso_client_authenticate(self):
        url_to_authenticate = reverse("simple-sso-authenticate")
        self.assertEqual("/sso/client/authenticate/", url_to_authenticate)
        query = (
            "next=%2F&access_token=InBBMjllMlNla2ZWdDdJMnR0c3R3QWIxcjQwRzV6TmphZDRSaEprbjlMbnR0TnF"
            "Ka3Q2d1dNR1lVYkhzVThvZU0i.XTeRVQ.3XiIMg0AFcJKDFCekse6s43uNLI"
        )
        url_to_authenticate += "?" + query

        with ConnectionMock():
            with TimestampSignerMock():
                response = self.client.get(url_to_authenticate)

        self.assertEqual(302, response.status_code)
        self.assertEqual("/", response.url)

        u = User.objects.first()
        self.assertEqual("jkowalski", u.username)
