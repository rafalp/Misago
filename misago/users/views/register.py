from misago.conf import settings
from misago.users.decorators import deny_authenticated, deny_banned_ips


def register_decorator(f):
    def decorator(request):
        if settings.account_activation == 'disabled':
            return registrations_off(request)
        else:
            return f(request)
    return decorator


@deny_authenticated
@deny_banned_ips
@register_decorator
def register(request):
    pass


def registration_off(request):
    pass
