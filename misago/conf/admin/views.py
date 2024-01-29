from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import pgettext

from ...admin.views import render
from ...admin.views.generic import AdminView
from ..models import Setting
from .forms import (
    AnalyticsSettingsForm,
    CaptchaSettingsForm,
    GeneralSettingsForm,
    NotificationsSettingsForm,
    OAuth2SettingsForm,
    ThreadsSettingsForm,
    UsersSettingsForm,
)


def index(request):
    return render(request, "misago/admin/conf/index.html")


class SettingsView(AdminView):
    root_link = None  # Unused by change config views
    template_name = None
    form_class = None

    def get_template_name(self, request):
        return self.template_name

    def dispatch(self, request, *args, **kwargs):
        settings = self.get_settings(self.form_class.settings)
        initial = self.get_initial_form_data(settings)
        form = self.form_class(request=request, initial=initial)
        if request.method == "POST":
            form = self.form_class(
                request.POST, request.FILES, request=request, initial=initial
            )

            if form.is_valid():
                form.save(settings)
                messages.success(
                    request, pgettext("admin settings", "Settings have been saved.")
                )
                return redirect(request.path_info)
        return self.render(request, {"form": form, "form_settings": settings})

    def get_settings(self, form_settings):
        settings = {}
        for setting in Setting.objects.filter(setting__in=form_settings):
            settings[setting.setting] = setting

        if len(settings) != len(form_settings):
            not_found_settings = list(
                set(settings.keys()).symmetric_difference(set(form_settings))
            )
            raise ValueError(
                "Some of settings defined in form could not be found: %s"
                % (", ".join(not_found_settings))
            )

        return settings

    def get_initial_form_data(self, settings):
        return {key: setting.value for key, setting in settings.items()}


class AnalyticsSettingsView(SettingsView):
    form_class = AnalyticsSettingsForm
    template_name = "misago/admin/conf/analytics_settings.html"


class CaptchaSettingsView(SettingsView):
    form_class = CaptchaSettingsForm
    template_name = "misago/admin/conf/captcha_settings.html"


class GeneralSettingsView(SettingsView):
    form_class = GeneralSettingsForm
    template_name = "misago/admin/conf/general_settings.html"


class NotificationsSettingsView(SettingsView):
    form_class = NotificationsSettingsForm
    template_name = "misago/admin/conf/notifications_settings.html"


class OAuth2SettingsView(SettingsView):
    form_class = OAuth2SettingsForm
    template_name = "misago/admin/conf/oauth2_settings.html"


class ThreadsSettingsView(SettingsView):
    form_class = ThreadsSettingsForm
    template_name = "misago/admin/conf/threads_settings.html"


class UsersSettingsView(SettingsView):
    form_class = UsersSettingsForm
    template_name = "misago/admin/conf/users_settings.html"
