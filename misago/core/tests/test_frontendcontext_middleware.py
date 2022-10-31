from django.http import HttpResponse

from ..middleware import FrontendContextMiddleware


class MockRequest:
    pass


def get_response(*_):
    return HttpResponse("OK!")


def test_frontend_middleware_sets_frontend_context_dict_on_request():
    request = MockRequest()
    FrontendContextMiddleware(get_response)(request)
    assert request.frontend_context == {}
