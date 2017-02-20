from django.test import TestCase

from misago.users.middleware import RealIPMiddleware


class MockRequest(object):
    def __init__(self, addr, forwarded_for=None):
        self.META = {'REMOTE_ADDR': addr}

        if forwarded_for:
            self.META['HTTP_X_FORWARDED_FOR'] = forwarded_for


class RealIPMiddlewareTests(TestCase):
    def test_middleware_sets_ip_from_remote_add(self):
        """Middleware sets ip from remote_addr header"""
        request = MockRequest('83.42.13.77')
        RealIPMiddleware().process_request(request)

        self.assertEqual(request.user_ip, request.META['REMOTE_ADDR'])

    def test_middleware_sets_ip_from_forwarded_for(self):
        """Middleware sets ip from forwarded_for header"""
        request = MockRequest('127.0.0.1', '83.42.13.77')
        RealIPMiddleware().process_request(request)

        self.assertEqual(request.user_ip, request.META['HTTP_X_FORWARDED_FOR'])
