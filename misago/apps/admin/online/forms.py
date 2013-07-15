import floppyforms as forms
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form

class SearchSessionsForm(Form):
    search_name = _("Search Sessions")
    username = forms.CharField(label=_("Username"), max_length=255, required=False)
    ip_address = forms.CharField(label=_("IP Address"), max_length=255, required=False)
    useragent = forms.CharField(label=_("User Agent"), max_length=255, required=False)
    type = forms.ChoiceField(label=_("Session Type"),
                             choices=(
                                      ('all', _("All types")),
                                      ('registered', _("Registered Members Sessions")),
                                      ('guest', _("Guests Sessions")),
                                      ('crawler', _("Crawler Sessions")),
                                     ), required=False)
