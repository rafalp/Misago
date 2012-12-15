from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.forms import Form, YesNoSwitch

class RoleForm(Form):
    name = forms.CharField(max_length=255)
    protected = forms.BooleanField(widget=YesNoSwitch,required=False)
    layout = [
              [
               _("Basic Role Options"),
               [
                ('name', {'label': _("Role Name"), 'help_text': _("Role Name is used to identify this role in Admin Control Panel.")}),
                ('protected', {'label': _("Protect this Role"), 'help_text': _("Only system administrators can edit or assign protected roles.")}),
                ],
              ],
             ]
    
    def __init__(self, *args, **kwargs):
        if not kwargs['request'].user.is_god():
            del self.base_fields['protected']
            del self.layout[0][1][1]
        super(RoleForm, self).__init__(*args, **kwargs)