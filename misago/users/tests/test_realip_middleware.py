from django.http import HttpResponse

from ..middleware import RealIPMiddleware


def get_response(*_):
    return HttpResponse("OK!")


class MockRequest:
    def __init__(self, addr, forwarded_for=None):
        self.META = {"REMOTE_ADDR": addr}

        if forwarded_for:
            self.META["HTTP_X_FORWARDED_FOR"] = forwarded_for


def test_user_ip_middleware_sets_ip_from_remote_add_on_request():
    request = MockRequest("83.42.13.77")
    RealIPMiddleware(get_response)(request)

    assert request.user_ip == request.META["REMOTE_ADDR"]


def test_user_ip_middleware_sets_ip_from_forwarded_for_on_request():
    request = MockRequest("127.0.0.1", "83.42.13.77")
    RealIPMiddleware(get_response)(request)

    assert request.user_ip == request.META["HTTP_X_FORWARDED_FOR"]
