from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import render
from django.utils.translation import pgettext

from ..credentialchange import read_new_credential
from ..decorators import deny_guests
from ..pages import usercp


@deny_guests
def index(request, *args, **kwargs):
    user_options = []
    for section in usercp.get_sections(request):
        user_options.append(
            {
                "name": str(section["name"]),
                "icon": section["icon"],
                "component": section["component"],
            }
        )

    request.frontend_context.update({"USER_OPTIONS": user_options})

    return render(request, "misago/options/noscript.html")


class ChangeError(Exception):
    pass


def confirm_change_view(f):
    @deny_guests
    def decorator(request, token):
        try:
            return f(request, token)
        except ChangeError:
            return render(request, "misago/options/credentials_error.html", status=400)

    return decorator


@confirm_change_view
def confirm_email_change(request, token):
    if request.settings.enable_oauth2_client:
        raise PermissionDenied(
            pgettext("user options", "Please use %(provider)s to change your e-mail.")
            % {"provider": request.settings.oauth2_provider}
        )

    new_credential = read_new_credential(request, "email", token)
    if not new_credential:
        raise ChangeError()

    try:
        request.user.set_email(new_credential)
        request.user.save(update_fields=["email", "email_hash"])
    except IntegrityError:
        raise ChangeError()

    message = pgettext("user options", "%(user)s, your e-mail has been changed.")
    return render(
        request,
        "misago/options/credentials_changed.html",
        {"message": message % {"user": request.user.username}},
    )


@confirm_change_view
def confirm_password_change(request, token):
    if request.settings.enable_oauth2_client:
        raise PermissionDenied(
            pgettext("user options", "Please use %(provider)s to change your password.")
            % {"provider": request.settings.oauth2_provider}
        )

    new_credential = read_new_credential(request, "password", token)
    if not new_credential:
        raise ChangeError()

    request.user.set_password(new_credential)
    update_session_auth_hash(request, request.user)
    request.user.save(update_fields=["password"])

    message = pgettext("user options", "%(user)s, your password has been changed.")
    return render(
        request,
        "misago/options/credentials_changed.html",
        {"message": message % {"user": request.user.username}},
    )
