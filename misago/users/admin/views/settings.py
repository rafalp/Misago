from ....conf.admin.views import ChangeSettingsView
from ..forms import ChangeCaptchaSettingsForm, ChangeUsersSettingsForm


class ChangeUsersSettingsView(ChangeSettingsView):
    form = ChangeUsersSettingsForm
    template_name = "misago/admin/users/users_settings.html"


class ChangeCaptchaSettingsView(ChangeSettingsView):
    form = ChangeCaptchaSettingsForm
    template_name = "misago/admin/users/captcha_settings.html"
