from django.core.exceptions import PermissionDenied
from django.http import Http404


def return_boolean(f):
    def decorator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except (Http404, PermissionDenied):
            return False
        else:
            return True

    return decorator
