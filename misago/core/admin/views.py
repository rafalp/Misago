from ...conf.admin.views import ChangeSettingsView
from .forms import ChangeGeneralSettingsForm


class ChangeGeneralSettingsView(ChangeSettingsView):
    form = ChangeGeneralSettingsForm
    template_name = "misago/admin/core/general_conf.html"
