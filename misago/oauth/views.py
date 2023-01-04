from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from unidecode import unidecode

from ..users.registration import send_welcome_email
from ..users.setupnewuser import setup_new_user
from .client import (
    exchange_code_for_token,
    receive_code,
    retrieve_user_data,
    start_flow,
)
from .models import Subject

User = get_user_model()


def oauth_start(request):
    redirect_to = start_flow(request)
    return HttpResponseRedirect(redirect_to)


def oauth_redirect(request):
    code = receive_code(request)
    token = exchange_code_for_token(request, code)
    user_data = retrieve_user_data(request, token)

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
