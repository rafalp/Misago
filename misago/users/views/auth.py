from django.conf import settings
from django.contrib import auth, messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from misago.core.decorators import require_POST

from misago.users.decorators import deny_authenticated, deny_guests
from misago.users.forms.auth import AuthenticationForm


@sensitive_post_parameters()
@deny_authenticated
@csrf_protect
@never_cache
def login(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            message = _("Welcome back, %(username)s! You have been "
                        "signed in successfully.")
            messages.success(
                request, message % {'username': form.user_cache.username})
            auth.login(request, form.user_cache)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'misago/login.html', {'form': form})


@deny_guests
@require_POST
@csrf_protect
@never_cache
def logout(request):
    message = _("%(username)s, you have been signed out.")
    messages.info(
        request, message % {'username': request.user.username})
    auth.logout(request)
    return redirect('misago:index')
