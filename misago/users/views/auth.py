from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
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
            request.session.pop('login_ban', None)

    return render(request, 'misago/login.html', {'form': form})


@deny_guests
@require_POST
@csrf_protect
@never_cache
def logout(request):
    return redirect('misago:index')


@never_cache
def login_banned(request):
    try:
        ban = request.session.['login_ban']
    except KeyError:
        Http404()

    return render(request, 'misago/errorpages/banned.html', {'ban': ban})
