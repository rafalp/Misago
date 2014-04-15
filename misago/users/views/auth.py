from django.contrib.auth import authenticate, login
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
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            pass

    return render(request, 'misago/login.html', {'form': form})


@deny_guests
@require_POST
@csrf_protect
@never_cache
def logout(request):
    return redirect('misago:index')
