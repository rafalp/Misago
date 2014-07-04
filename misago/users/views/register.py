from django.shortcuts import redirect, render

from misago.conf import settings
from misago.users.decorators import deny_authenticated, deny_banned_ips


def register_decorator(f):
    def decorator(request):
        if True or settings.account_activation == 'disabled':
            return registration_disabled(request)
        else:
            return f(request)
    return decorator


@deny_authenticated
@deny_banned_ips
@register_decorator
def register(request):
    return render(request, 'misago/register/form.html')


def registration_disabled(request):
    return render(request, 'misago/register/disabled.html')
