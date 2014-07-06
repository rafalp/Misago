from django.shortcuts import redirect, render

from misago.conf import settings
from misago.users.decorators import deny_authenticated, deny_banned_ips
from misago.users.forms.register import RegisterForm


def register_decorator(f):
    def decorator(request):
        if settings.account_activation == 'disabled':
            return registration_disabled(request)
        else:
            return f(request)
    return decorator


@deny_authenticated
@deny_banned_ips
@register_decorator
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            pass

    return render(request, 'misago/register/form.html', {'form': form,})


def registration_disabled(request):
    return render(request, 'misago/register/disabled.html')
