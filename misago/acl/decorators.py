from django.core.exceptions import PermissionDenied
from django.http import Http404


def require_target_type(supported_type):
    def wrap(f):
        def decorator(user, target):
            if isinstance(target, supported_type):
                return f(user, target)
            else:
                return None
        return decorator
    return wrap


def return_boolean(f):
    def decorator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except (Http404, PermissionDenied):
            return False
        else:
            return True
    return decorator
