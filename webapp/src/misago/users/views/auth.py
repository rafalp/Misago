from urllib.parse import urlparse

from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from django.urls import NoReverseMatch
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


@sensitive_post_parameters()
@never_cache
@csrf_protect
def login(request):
    if request.method == "POST":
        redirect_to = request.POST.get("redirect_to")
        if redirect_to:
            is_redirect_safe = is_safe_url(
                url=redirect_to,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            )
            if is_redirect_safe:
                redirect_to_path = urlparse(redirect_to).path
                if "?" not in redirect_to_path:
                    redirect_to_path = "%s?" % redirect_to_path
                else:
                    redirect_to_path = "%s&" % redirect_to_path
                redirect_to_path = "%sref=login" % redirect_to_path
                try:
                    return redirect(redirect_to_path)
                except NoReverseMatch:
                    pass

    return redirect(settings.LOGIN_REDIRECT_URL)


@never_cache
@csrf_protect
def logout(request):
    if request.method == "POST" and request.user.is_authenticated:
        auth.logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)
