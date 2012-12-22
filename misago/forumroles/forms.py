from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.forms import Form

class ForumRoleForm(Form):
    name = forms.CharField(max_length=255)
    
    def finalize_form(self):
        self.layout = (
                       (
                        _("Basic Role Options"),
                        (
                         ('name', {'label': _("Role Name"), 'help_text': _("Role Name is used to identify this role in Admin Control Panel.")}),
                         ),
                        ),
                       )