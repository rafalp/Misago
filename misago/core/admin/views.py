from django import forms
from django.utils.translation import gettext_lazy as _

from ...conf.admin.views import ChangeConfigView


class ChangeGeneralConfigForm(forms.Form):
    settings = ["forum_name", "forum_index_title"]

    forum_name = forms.CharField(label=_("Forum name"), min_length=2, max_length=255)
    forum_index_title = forms.CharField(
        label=_("Index title"),
        help_text=_("You may set custon title on forum index by typing it here."),
        min_length=2,
        max_length=255,
    )


class ChangeGeneralConfigView(ChangeConfigView):
    form = ChangeGeneralConfigForm
    template_name = "misago/admin/core/general_conf.html"
