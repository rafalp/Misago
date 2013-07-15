import floppyforms as forms
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form

class SearchSessionsForm(Form):
    username = forms.CharField(max_length=255, required=False)
    ip_address = forms.CharField(max_length=255, required=False)
    useragent = forms.CharField(max_length=255, required=False)
    type = forms.ChoiceField(choices=(
                                      ('all', _("All types")),
                                      ('registered', _("Registered Members Sessions")),
                                      ('guest', _("Guests Sessions")),
                                      ('crawler', _("Crawler Sessions")),
                                      ), required=False)

    layout = (
              (
               _("Search Sessions"),
               (
                ('ip_address', {'label': _("IP Address"), 'attrs': {'placeholder': _("IP begins with...")}}),
                ('username', {'label': _("Username"), 'attrs': {'placeholder': _("Username begings with...")}}),
                ('useragent', {'label': _("User Agent"), 'attrs': {'placeholder': _("User Agent contains...")}}),
                ('type', {'label': _("Session Type")}),
               ),
              ),
             )
