from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
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
            User = get_user_model()
            new_user = User.objects.create_user(form.cleaned_data['username'],
                                                form.cleaned_data['email'],
                                                form.cleaned_data['password'])

            authenticated_user = authenticate(
                username=new_user.email,
                password=form.cleaned_data['password'])
            login(request, authenticated_user)

            welcome_message = _("Welcome aboard, %(username)s!")
            welcome_message = welcome_message % {'username': new_user.username}
            messages.success(request, welcome_message)

            return redirect('misago:index')

    return render(request, 'misago/register/form.html', {'form': form, 'testname': 'and<b>rzej'})


def registration_disabled(request):
    return render(request, 'misago/register/disabled.html')
