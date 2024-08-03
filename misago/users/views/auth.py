from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


@never_cache
@csrf_protect
def logout(request):
    if request.method == "POST" and request.user.is_authenticated:
        auth.logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)
