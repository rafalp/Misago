from functools import wraps
from logging import getLogger

from django.contrib.auth import get_user_model, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from unidecode import unidecode

from ..users.decorators import deny_banned_ips
from ..users.registration import send_welcome_email
from ..users.setupnewuser import setup_new_user
from .client import (
    create_login_url,
    exchange_code_for_token,
    receive_code_grant,
    retrieve_user_data,
)
from .exceptions import OAuth2Error
from .models import Subject

logger = getLogger("misago.oauth2")

User = get_user_model()


def oauth2_view(f):
    f = deny_banned_ips(f)

    @wraps(f)
    @never_cache
    def wrapped_oauth2_view(request):
        if not request.settings.enable_oauth2_client:
            raise Http404()

        return f(request)

    return wrapped_oauth2_view


@oauth2_view
def oauth2_login(request):
    redirect_to = create_login_url(request)
    return redirect(redirect_to)


@oauth2_view
def oauth2_complete(request):
    try:
        code_grant = receive_code_grant(request)
        token = exchange_code_for_token(request, code_grant)
        user_data = retrieve_user_data(request, token)
    except OAuth2Error as error:
        logger.exception("OAuth2 Error")
        return render(request, "misago/errorpages/oauth2.html", {"error": error})

    if user_data["name"]:
        user_data["name"] = convert_name(user_data["id"], user_data["name"])

    if user_data["id"]:
        try:
            subject = Subject.objects.select_related("user").get(sub=user_data["id"])
            subject.last_used_on = timezone.now()
            subject.save(update_fields=["last_used_on"])

            login(request, subject.user)
            return redirect(reverse("misago:index"))
        except Subject.DoesNotExist:
            pass

    activation_kwargs = {}
    if request.settings.account_activation == "admin":
        activation_kwargs = {"requires_activation": User.ACTIVATION_ADMIN}

    new_user = User.objects.create_user(
        user_data["name"],
        user_data["email"],
        joined_from_ip=request.user_ip,
        **activation_kwargs,
    )

    Subject.objects.create(sub=user_data["id"], user=new_user)

    setup_new_user(request.settings, new_user)
    send_welcome_email(request, new_user)

    login(request, new_user)
    return redirect(reverse("misago:index"))


def convert_name(user_id, name):
    clean_name = [c for c in unidecode(name.replace("_", "")) if c.isalnum()]
    return "".join(clean_name) or f"User_{user_id[:-6]}"
