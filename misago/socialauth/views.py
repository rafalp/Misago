from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse
from django.utils.translation import pgettext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from social_core.actions import do_auth, do_complete
from social_django.views import _do_login
from social_django.utils import load_strategy


def get_provider_from_request(request, backend):
    try:
        return request.socialauth[backend]
    except KeyError:
        raise Http404()


def social_auth_view(f):
    def social_auth_view_wrapper(request, backend, *args, **kwargs):
        if request.settings.enable_oauth2_client:
            raise PermissionDenied(
                pgettext(
                    "social auth",
                    "This feature has been disabled. Please use %(provider)s to sign in.",
                )
                % {"provider": request.settings.oauth2_provider}
            )

        provider = get_provider_from_request(request, backend)
        request.strategy = load_strategy(request)

        backend_class = provider["auth_backend"]
        request.backend = backend_class(
            request.strategy,
            reverse("misago:social-complete", kwargs={"backend": backend}),
        )

        return f(request, backend, *args, **kwargs)

    return social_auth_view_wrapper


@never_cache
@social_auth_view
def auth(request, backend):
    return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)


@never_cache
@csrf_exempt
@social_auth_view
def complete(request, backend, *args, **kwargs):
    return do_complete(
        request.backend,
        do_login,
        user=request.user,
        redirect_name=REDIRECT_FIELD_NAME,
        request=request,
        *args,
        **kwargs
    )


def do_login(backend, user, social_user):
    user.backend = "misago.users.authbackends.MisagoBackend"
    login(backend.strategy.request, user)
