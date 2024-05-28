from typing import Any

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.forms import Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext, pgettext_lazy
from django.views import View

from ...pagination.cursor import paginate_queryset
from ..forms import (
    AccountPreferencesForm,
    AccountUsernameForm,
    notifications_preferences,
    watching_preferences,
)
from ..menus import account_settings_menu


def raise_if_not_authenticated(request):
    if not request.user.is_authenticated:
        raise PermissionDenied(
            pgettext(
                "account settings page error",
                "You need to be signed in to change your account's settings.",
            )
        )


def index(request):
    raise_if_not_authenticated(request)

    menu = account_settings_menu.bind_to_request(request)
    return redirect(menu.items[0].url)


class AccountSettingsView(View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        raise_if_not_authenticated(request)

        return super().dispatch(request, *args, **kwargs)

    def get_template_context(
        self,
        request: HttpRequest,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return context

    def render(
        self,
        request: HttpRequest,
        template_name: str,
        context: dict[str, Any] | None = None,
    ) -> HttpResponse:
        final_context = self.get_template_context(request, context)
        final_context["account_menu"] = account_settings_menu.bind_to_request(request)
        return render(request, template_name, final_context)


class AccountSettingsFormView(AccountSettingsView):
    template_name: str
    template_htmx_name: str | None = None
    success_message: str

    def get_form_instance(self, request: HttpRequest) -> Form:
        raise NotImplementedError()

    def save_form(self, request: HttpRequest, form: Form) -> None:
        form.save()

    def get_template_context(
        self,
        request: HttpRequest,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return context

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.get_form_instance(request)
        return self.render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.get_form_instance(request)
        if form.is_valid():
            self.save_form(request, form)

            messages.success(request, self.success_message)

            if request.is_htmx and self.template_htmx_name:
                return self.render(request, self.template_htmx_name, {"form": form})

            return redirect(request.path_info)

        if request.is_htmx and self.template_htmx_name:
            template_name = self.template_htmx_name
        else:
            template_name = self.template_name

        return self.render(request, template_name, {"form": form})


class AccountPreferencesView(AccountSettingsFormView):
    template_name = "misago/account/settings/preferences.html"
    template_htmx_name = "misago/account/settings/preferences_form.html"

    success_message = pgettext_lazy(
        "account settings preferences updated", "Preferences updated"
    )

    def get_form_instance(self, request: HttpRequest) -> AccountPreferencesForm:
        if request.method == "POST":
            return AccountPreferencesForm(request.POST, instance=request.user)

        return AccountPreferencesForm(instance=request.user)

    def get_template_context(
        self,
        request: HttpRequest,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        form = context["form"]
        context.update(
            {
                "notifications_preferences": notifications_preferences.get_items(form),
                "watching_preferences": watching_preferences.get_items(form),
            }
        )

        return context


class AccountUsernameView(AccountSettingsFormView):
    template_name = "misago/account/settings/username.html"
    template_htmx_name = "misago/account/settings/username_form.html"
    template_history_name = "misago/account/settings/username_history.html"

    success_message = pgettext_lazy(
        "account settings username changed", "Username changed"
    )

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.get_form_instance(request)

        if request.is_htmx:
            template_name = self.template_history_name
        else:
            template_name = self.template_name

        return self.render(request, template_name, {"form": form})

    def get_template_context(
        self,
        request: HttpRequest,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        context["username_history"] = self.get_username_history(request)
        return context

    def get_form_instance(self, request: HttpRequest) -> AccountUsernameForm:
        if request.method == "POST":
            return AccountUsernameForm(
                request.POST,
                instance=request.user,
                request=request,
            )

        return AccountUsernameForm(
            instance=request.user,
            request=request,
        )

    def get_username_history(self, request: HttpRequest):
        return paginate_queryset(
            request, request.user.namechanges.select_related("changed_by"), 10, "-id"
        )
