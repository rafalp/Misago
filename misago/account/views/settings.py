from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext
from django.views import View

from ..forms import AccountPreferencesForm
from ..menus import account_settings_menu


def raise_if_not_authenticated(request):
    if not request.user.is_authenticated:
        raise PermissionDenied(
            pgettext(
                "account settings page error",
                "You need to be signed in to change your account's settings."
            )
        )


def index(request):
    raise_if_not_authenticated(request)

    menu = account_settings_menu.bind_to_request(request)
    return redirect(menu.items[0].url)


class AccountSettingsView(View):
    template_name: str

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        raise_if_not_authenticated(request)

        return super().dispatch(request, *args, **kwargs)

    def render(self, request: HttpRequest, context: dict[str, Any] | None = None) -> HttpResponse:
        context = context or {}
        context["account_menu"] = account_settings_menu.bind_to_request(request)

        return render(request, self.template_name, context)


class AccountPreferencesView(AccountSettingsView):
    template_name = "misago/account/settings/preferences.html"

    def get(self, request):
        form = AccountPreferencesForm(instance=request.user)
        return self.render(request, {"form": form})

    def post(self, request):
        form = AccountPreferencesForm(request.POST, instance=request.user)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print(form.errors)

        return self.render(request, {"form": form})
