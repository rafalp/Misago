from django.shortcuts import redirect, render
from django.views.decorators.debug import sensitive_post_parameters

from misago.conf import settings
from misago.core.captcha import add_captcha_to_form

from misago.users.decorators import deny_authenticated, deny_banned_ips
from misago.users.forms.register import RegisterForm


def register_decorator(f):
    def decorator(request):
        if settings.account_activation == 'disabled':
            return registration_disabled(request)
        else:
            return f(request)
    return decorator


@sensitive_post_parameters("email", "password")
@deny_authenticated
@deny_banned_ips
@register_decorator
def register(request):
    SecuredForm = add_captcha_to_form(RegisterForm, request)

    form = SecuredForm()
    if request.method == 'POST':
        form = SecuredForm(request.POST)
        if form.is_valid():
            pass

    return render(request, 'misago/register/form.html', {'form': form, 'testname': 'and<b>rzej'})


def registration_disabled(request):
    return render(request, 'misago/register/disabled.html')
