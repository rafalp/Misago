from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.forms import Form, ValidationError
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _, pgettext, pgettext_lazy
from django.views import View
from django.views.decorators.debug import sensitive_post_parameters

from ...auth.decorators import login_required
from ...core.mail import build_mail
from ...pagination.cursor import EmptyPageError, paginate_queryset
from ...pagination.redirect import redirect_to_last_page
from ...users.datadownloads import (
    request_user_data_download,
    user_has_data_download_request,
)
from ...users.models import DataDownload
from ...users.online.tracker import clear_tracking
from ...users.tasks import delete_user
from ...users.validators import validate_email
from ..forms import (
    AccountDeleteForm,
    AccountDetailsForm,
    AccountEmailForm,
    AccountPasswordForm,
    AccountPreferencesForm,
    AccountUsernameForm,
    notifications_preferences,
    watching_preferences,
)
from ..emailchange import (
    EmailChangeTokenError,
    create_email_change_token,
    read_email_change_token,
)
from ..menus import account_settings_menu

User = get_user_model()


def account_settings_login_required():
    return login_required(
        pgettext(
            "account settings login page",
            "Sign in to change your settings",
        )
    )


@account_settings_login_required()
def index(request):
    menu = account_settings_menu.bind_to_request(request)
    return redirect(menu.items[0].url)


class AccountSettingsView(View):
    @method_decorator(account_settings_login_required())
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        except EmptyPageError as exception:
            return redirect_to_last_page(request, exception)

    def get_context_data(
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
        final_context = self.get_context_data(request, context or {})
        final_context["account_menu"] = account_settings_menu.bind_to_request(request)
        return render(request, template_name, final_context)


class AccountSettingsFormView(AccountSettingsView):
    template_name: str
    template_name_htmx: str | None = None
    success_message: str

    def get_form_instance(self, request: HttpRequest) -> Form:
        raise NotImplementedError()

    def save_form(self, request: HttpRequest, form: Form) -> None:
        form.save()

    def get_context_data(
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
            return self.handle_valid_form(request, form)

        return self.handle_invalid_form(request, form)

    def handle_valid_form(self, request: HttpRequest, form: Form) -> HttpResponse:
        self.save_form(request, form)

        messages.success(request, self.success_message)

        if request.is_htmx and self.template_name_htmx:
            return self.render(request, self.template_name_htmx, {"form": form})

        return redirect(request.path_info)

    def handle_invalid_form(self, request: HttpRequest, form: Form) -> HttpResponse:
        messages.error(request, _("Form contains errors"))

        if request.is_htmx and self.template_name_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return self.render(request, template_name, {"form": form})


class AccountPreferencesView(AccountSettingsFormView):
    template_name = "misago/account/settings/preferences.html"
    template_name_htmx = "misago/account/settings/preferences_form.html"

    success_message = pgettext_lazy(
        "account settings preferences updated", "Preferences updated"
    )

    def get_form_instance(self, request: HttpRequest) -> AccountPreferencesForm:
        if request.method == "POST":
            return AccountPreferencesForm(request.POST, instance=request.user)

        return AccountPreferencesForm(instance=request.user)

    def get_context_data(
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


class AccountDetailsView(AccountSettingsFormView):
    template_name = "misago/account/settings/details.html"
    template_name_htmx = "misago/account/settings/details_form.html"

    success_message = pgettext_lazy(
        "account settings preferences updated", "Profile updated"
    )

    def get_form_instance(self, request: HttpRequest) -> AccountPreferencesForm:
        if request.method == "POST":
            return AccountDetailsForm(
                request.POST,
                instance=request.user,
                request=request,
            )

        return AccountDetailsForm(
            instance=request.user,
            request=request,
        )


class AccountUsernameView(AccountSettingsFormView):
    template_name = "misago/account/settings/username.html"
    template_name_htmx = "misago/account/settings/username_form.html"
    template_history_name = "misago/account/settings/username_history.html"

    success_message = pgettext_lazy(
        "account settings username changed", "Username changed"
    )

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.settings.enable_oauth2_client:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.get_form_instance(request)

        if request.is_htmx:
            template_name = self.template_history_name
        else:
            template_name = self.template_name

        return self.render(request, template_name, {"form": form})

    def get_context_data(
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


class AccountPasswordView(AccountSettingsFormView):
    template_name = "misago/account/settings/password.html"
    template_name_htmx = "misago/account/settings/password_form.html"
    email_template_name = "misago/emails/password_changed"

    success_message = pgettext_lazy(
        "account settings password changed", "Password changed"
    )

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.settings.enable_oauth2_client:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get_form_instance(self, request: HttpRequest) -> AccountPasswordForm:
        if request.method == "POST":
            return AccountPasswordForm(
                request.POST,
                instance=request.user,
                request=request,
            )

        return AccountPasswordForm(
            instance=request.user,
            request=request,
        )

    def save_form(self, request: HttpRequest, form: Form) -> None:
        form.save()

        mail = build_mail(
            request.user,
            pgettext(
                "password changed email subject",
                "Your password on the %(forum_name)s forums has been changed",
            )
            % {"forum_name": request.settings.forum_name},
            self.email_template_name,
            context={"settings": request.settings},
        )
        mail.send(fail_silently=True)


class AccountEmailView(AccountSettingsFormView):
    template_name = "misago/account/settings/email.html"
    template_name_htmx = "misago/account/settings/email_form.html"
    template_htmx_success_name = "misago/account/settings/email_form_completed.html"
    email_template_name = "misago/emails/email_confirm_change"

    success_message = pgettext_lazy(
        "account settings email confirm", "Confirmation email sent"
    )

    @method_decorator(sensitive_post_parameters("current_password"))
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.settings.enable_oauth2_client:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.get_form_instance(request)

        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return self.render(request, template_name, {"form": form})

    def get_form_instance(self, request: HttpRequest) -> AccountEmailForm:
        if request.method == "POST":
            return AccountEmailForm(
                request.POST,
                instance=request.user,
                request=request,
            )

        return AccountEmailForm(
            instance=request.user,
            request=request,
        )

    def handle_valid_form(self, request: HttpRequest, form: Form) -> HttpResponse:
        self.save_form(request, form)

        if request.is_htmx and self.template_name_htmx:
            messages.success(request, self.success_message)
            return self.render(
                request,
                self.template_htmx_success_name,
                {"new_email": form.cleaned_data["new_email"]},
            )

        request.session["misago_new_email"] = form.cleaned_data["new_email"]
        return redirect(reverse("misago:account-email-confirm-sent"))

    def save_form(self, request: HttpRequest, form: Form) -> None:
        new_email = form.cleaned_data["new_email"]
        token = create_email_change_token(request.user, form.cleaned_data["new_email"])

        # Swap e-mail on user instance so email is sent to a new address
        request.user.email = new_email

        mail = build_mail(
            request.user,
            pgettext(
                "email confirm change email subject",
                "Change your email on the %(forum_name)s forums",
            )
            % {"forum_name": request.settings.forum_name},
            self.email_template_name,
            context={
                "settings": request.settings,
                "token": token,
                "expires_in": settings.MISAGO_EMAIL_CHANGE_TOKEN_EXPIRES,
            },
        )
        mail.send(fail_silently=True)


class AccountEmailConfirm(AccountSettingsView):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.settings.enable_oauth2_client:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        new_email = request.session.pop("misago_new_email", None)
        if not new_email:
            return redirect(reverse("misago:account-email"))

        return self.render(
            request,
            "misago/account/settings/email_confirm.html",
            {"new_email": new_email},
        )


def account_email_confirm_change(request, user_id, token):
    if request.settings.enable_oauth2_client:
        raise Http404()

    user = get_object_or_404(User.objects, id=user_id, is_active=True)

    try:
        new_email = read_email_change_token(user, token)
        validate_email(new_email, user)
    except EmailChangeTokenError as e:
        return render(
            request,
            "misago/account/settings/email_change_error.html",
            {
                "message": str(e),
                "error_code": str(e.code),
            },
        )
    except ValidationError as e:
        return render(
            request,
            "misago/account/settings/email_change_error.html",
            {"message": str(e.messages[0])},
        )

    if new_email != user.email:
        user.set_email(new_email)
        user.save()

    return render(
        request,
        "misago/account/settings/email_changed.html",
        {"username": user.username, "new_email": new_email},
    )


class AccountDownloadDataView(AccountSettingsView):
    template_name = "misago/account/settings/download_data.html"
    template_name_htmx = "misago/account/settings/download_data_form.html"

    success_message = pgettext_lazy(
        "account settings data download requested", "Data download requested"
    )

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.settings.allow_data_downloads:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return self.render(request, template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        if user_has_data_download_request(request.user):
            messages.warning(
                request,
                pgettext(
                    "account settings data download requested",
                    "You can't request a new data download before the previous one completes.",
                ),
            )
        else:
            request_user_data_download(request.user, request.user)
            messages.success(request, self.success_message)

        if request.is_htmx:
            return self.render(request, self.template_name_htmx)

        return redirect("misago:account-download-data")

    def get_context_data(
        self,
        request: HttpRequest,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        context["data_downloads"] = self.get_data_downloads(request)
        context["has_data_download_request"] = user_has_data_download_request(
            request.user
        )

        if context["data_downloads"].items:
            for item in context["data_downloads"].items:
                if item.status < DataDownload.STATUS_READY:
                    context["data_downloads_refresh"] = True
                    break

        return context

    def get_data_downloads(self, request: HttpRequest):
        return paginate_queryset(request, request.user.datadownload_set, 15, "-id")


class AccountDeleteView(AccountSettingsFormView):
    template_name = "misago/account/settings/delete.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if (
            request.settings.enable_oauth2_client
            or not request.settings.allow_delete_own_account
        ):
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get_form_instance(self, request: HttpRequest) -> AccountDeleteForm:
        if request.method == "POST":
            return AccountDeleteForm(request.POST, instance=request.user)

        return AccountDeleteForm(instance=request.user)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.get_form_instance(request)
        if form.is_valid():
            logout(request)
            clear_tracking(request)

            form.instance.mark_for_delete()
            delete_user.delay(form.instance.id)

            request.session["misago_deleted_account"] = form.instance.username
            return redirect("misago:account-delete-completed")

        return self.render(request, self.template_name, {"form": form})


def account_delete_completed(request):
    deleted_account = request.session.pop("misago_deleted_account", None)
    if not deleted_account:
        raise Http404()

    return render(
        request,
        "misago/account/settings/delete_completed.html",
        {"deleted_account": deleted_account},
    )
