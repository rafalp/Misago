from ...admin.views.generic import AdminView
from ..models import Setting


class ChangeConfigView(AdminView):
    root_link = None  # Unused by change config views
    template_name = None
    form = None

    def final_template(self):
        return self.template_name

    def dispatch(self, request, *args, **kwargs):
        settings = self.get_settings(self.form.settings)
        initial = {key: setting.value for key, setting in settings.items()}
        form = self.form(initial=initial)
        return self.render(request, {"form": form})

    def get_settings(self, settings):
        settings_dict = {}
        for setting in Setting.objects.filter(setting__in=settings):
            settings_dict[setting.name] = setting
        if len(settings_dict) != len(settings):
            not_found_settings = list(set(settings_dict.keys()) - set(settings))
            raise ValueError(
                "Some of settings defined in form could not be found: "
                ", ".join(not_found_settings)
            )
        return settings_dict
