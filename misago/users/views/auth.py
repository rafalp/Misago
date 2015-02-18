from django.conf import settings
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from misago.core.decorators import require_POST

from misago.users.decorators import (deny_authenticated, deny_guests,
                                     deny_banned_ips)
from misago.users.forms.auth import AuthenticationForm


@sensitive_post_parameters()
@never_cache
@deny_authenticated
@csrf_protect
@deny_banned_ips
def login(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.user_cache)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'misago/login.html', {'form': form})


@never_cache
@deny_guests
@require_POST
@csrf_protect
def logout(request):
    auth.logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)
