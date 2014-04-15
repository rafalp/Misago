from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from misago.core.decorators import require_POST
from misago.users.decorators import deny_authenticated, deny_guests


@sensitive_post_parameters()
@deny_authenticated
@csrf_protect
@never_cache
def login(request):
    return render(request, 'misago/login.html')


@deny_guests
@require_POST
@csrf_protect
@never_cache
def logout(request):
    raise NotImplementedError()
