from django.test import TestCase
from django.utils import translation

from .. import context_processors


class MockRequest:
    path = "/"

    def __init__(self, secure, host):
        self.secure = secure
        self.host = host

    def is_secure(self):
        return self.secure

    def get_host(self):
        return self.host


class MetaMockRequest:
    def __init__(self, meta):
        self.META = meta


class MomentjsLocaleTests(TestCase):
    def test_momentjs_locale(self):
        """momentjs_locale adds MOMENTJS_LOCALE_URL to context"""
        with translation.override("no-no"):
            self.assertEqual(
                context_processors.momentjs_locale(True), {"MOMENTJS_LOCALE_URL": None}
            )

        with translation.override("en-us"):
            self.assertEqual(
                context_processors.momentjs_locale(True), {"MOMENTJS_LOCALE_URL": None}
            )

        with translation.override("de"):
            self.assertEqual(
                context_processors.momentjs_locale(True),
                {"MOMENTJS_LOCALE_URL": "misago/momentjs/de.js"},
            )

        with translation.override("pl-de"):
            self.assertEqual(
                context_processors.momentjs_locale(True),
                {"MOMENTJS_LOCALE_URL": "misago/momentjs/pl.js"},
            )


class FrontendContextTests(TestCase):
    def test_frontend_context(self):
        """frontend_context is available in templates"""
        mock_request = MockRequest(False, "somewhere.com")
        mock_request.include_frontend_context = True
        mock_request.frontend_context = {"someValue": "Something"}

        self.assertEqual(
            context_processors.frontend_context(mock_request),
            {"frontend_context": {"someValue": "Something"}},
        )

        mock_request.include_frontend_context = False
        self.assertEqual(context_processors.frontend_context(mock_request), {})
