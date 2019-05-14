from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from ...admin.views import render
from ...admin.views.generic import AdminView
from ..models import Setting


def index(request):
    return render(request, "misago/admin/conf/index.html")


class ChangeSettingsView(AdminView):
    root_link = None  # Unused by change config views
    template_name = None
    form = None

    def final_template(self):
        return self.template_name

    def dispatch(self, request, *args, **kwargs):
        settings = self.get_settings(self.form.settings)
        initial = self.get_initial_form_data(settings)
        form = self.form(initial=initial)
        if request.method == "POST":
            form = self.form(request.POST, request.FILES, initial=initial)
            if form.is_valid():
                form.save(settings)
                messages.success(request, _("Changes in settings have been saved!"))
                return redirect(request.path_info)
        return self.render(request, {"form": form})

    def get_settings(self, form_settings):
        settings = {}
        for setting in Setting.objects.filter(setting__in=form_settings):
            settings[setting.setting] = setting

        if len(settings) != len(form_settings):
            not_found_settings = list(set(settings.keys()) - set(form_settings))
            raise ValueError(
                "Some of settings defined in form could not be found: "
                ", ".join(not_found_settings)
            )

        return settings

    def get_initial_form_data(self, settings):
        return {key: setting.value for key, setting in settings.items()}
