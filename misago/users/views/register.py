from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from misago.conf import settings
from misago.core.captcha import add_captcha_to_form
from misago.core.mail import mail_user

from misago.users.decorators import deny_authenticated, deny_banned_ips
from misago.users.forms.register import RegisterForm
from misago.users.models import (ACTIVATION_REQUIRED_USER,
                                 ACTIVATION_REQUIRED_ADMIN)


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
            activation_kwargs = {}
            if settings.account_activation == 'user':
                activation_kwargs = {
                    'requires_activation': ACTIVATION_REQUIRED_USER
                }
            elif settings.account_activation == 'admin':
                activation_kwargs = {
                    'requires_activation': ACTIVATION_REQUIRED_ADMIN
                }

            User = get_user_model()
            new_user = User.objects.create_user(form.cleaned_data['username'],
                                                form.cleaned_data['email'],
                                                form.cleaned_data['password'],
                                                **activation_kwargs)

            if settings.account_activation == 'none':
                authenticated_user = authenticate(
                    username=new_user.email,
                    password=form.cleaned_data['password'])
                login(request, authenticated_user)

                welcome_message = _("Welcome aboard, %(username)s!")
                welcome_message = welcome_message % {'username': new_user.username}
                messages.success(request, welcome_message)

                subject = _("Welcome on %(forum_title)s forums!")
                subject = subject % {'forum_title': settings.forum_name}
                mail_user(request, new_user, subject,
                          'misago/emails/register/complete')

                return redirect('misago:index')
            else:
                request.session['registered_user'] = new_user.pk
                return redirect('misago:register_completed')

    return render(request, 'misago/register/form.html', {'form': form, 'testname': 'and<b>rzej'})


def registration_disabled(request):
    return render(request, 'misago/register/disabled.html')


def registration_completed(request):
    """
    If user needs to activate his account, we display him page with message
    """
    registered_user_pk = request.session.get('registered_user')
    if not registered_user_pk:
        raise Http404

    registered_user = get_object_or_404(get_user_model().objects,
                                        pk=registered_user_pk)

    if not registered_user.requires_activation:
        return redirect('misago:index')

    activation_method = registered_user.requires_activation
    activation_by_admin = activation_method == ACTIVATION_REQUIRED_ADMIN
    activation_by_user = activation_method == ACTIVATION_REQUIRED_USER

    return render(
        request,
        'misago/register/completed.html',
        {
            'activation_by_admin': activation_by_admin,
            'activation_by_user': activation_by_user,
            'registered_user': registered_user,
        })

