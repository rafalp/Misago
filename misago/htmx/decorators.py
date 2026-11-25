from functools import wraps

from django.http import Http404

from .request import is_request_htmx


def require_htmx(f):
    @wraps(f)
    def htmx_required_decorator(request, *args, **kwargs):
        if is_request_htmx(request):
            return f(request, *args, **kwargs)

        raise Http404()

    return htmx_required_decorator
