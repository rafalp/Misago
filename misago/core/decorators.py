from django.shortcuts import render


def ajax_only(f):
    def decorator(request, *args, **kwargs):
        if not request.is_ajax():
            response = render(request, 'misago/errorpages/wrong_way.html')
            response.status_code = 405
            return response
        else:
            return f(request, *args, **kwargs)
    return decorator


def require_POST(f):
    def decorator(request, *args, **kwargs):
        if not request.method == 'POST':
            response = render(request, 'misago/errorpages/wrong_way.html')
            response.status_code = 405
            return response
        else:
            return f(request, *args, **kwargs)
    return decorator
