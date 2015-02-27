from django.test import TestCase
from django.utils import timezone

from misago.conf import settings

from misago.users.middleware import TimezoneMiddleware


class MockRequest(object):
    def __init__(self, user):
        self.user = user


class MockAuthenticated(object):
    timezone = 'Europe/Warsaw'

    def is_authenticated(self):
        return True


class MockGuest(object):
    def is_authenticated(self):
        return False


class TimezoneMiddlewareTests(TestCase):
    def setUp(self):
        timezone.activate('Europe/Paris')

    def tearDown(self):
        timezone.deactivate()

    def test_middleware_sets_timezone_for_guest(self):
        """Middleware sets ip from remote_addr header"""
        request = MockRequest(MockGuest())
        TimezoneMiddleware().process_request(request)

        self.assertEqual(timezone.get_current_timezone_name().lower(),
                         settings.default_timezone)

    def test_middleware_sets_timezone_for_authenticated(self):
        """Middleware sets ip from forwarded_for header"""
        request = MockRequest(MockAuthenticated())
        TimezoneMiddleware().process_request(request)

        self.assertEqual(timezone.get_current_timezone_name(),
                         MockAuthenticated.timezone)
