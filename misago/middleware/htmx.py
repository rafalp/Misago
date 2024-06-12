from ..htmx.request import is_request_htmx


def htmx_middleware(get_response):
    def middleware(request):
        request.is_htmx = is_request_htmx(request)
        return get_response(request)

    return middleware
