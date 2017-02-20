from .errorpages import not_allowed


def ajax_only(f):
    def decorator(request, *args, **kwargs):
        if not request.is_ajax():
            return not_allowed(request)
        else:
            return f(request, *args, **kwargs)

    return decorator


def require_POST(f):
    def decorator(request, *args, **kwargs):
        if not request.method == 'POST':
            return not_allowed(request)
        else:
            return f(request, *args, **kwargs)

    return decorator
