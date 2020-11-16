from rest_framework import serializers

from .errorpages import not_allowed


def ajax_only(f):
    def decorator(request, *args, **kwargs):
        if not request.is_ajax():
            return not_allowed(request)
        return f(request, *args, **kwargs)

    return decorator


def require_POST(f):
    def decorator(request, *args, **kwargs):
        if not request.method == "POST":
            return not_allowed(request)
        return f(request, *args, **kwargs)

    return decorator


def require_dict_data(f):
    def decorator(request, *args, **kwargs):
        if request.method == "POST":
            DummySerializer(data=request.data).is_valid(raise_exception=True)
        return f(request, *args, **kwargs)

    return decorator


class DummySerializer(serializers.Serializer):
    pass
