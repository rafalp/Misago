from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form, YesNoSwitch
from misago.validators import validate_sluggable

class RoleForm(Form):
    name = forms.CharField(max_length=255,validators=[validate_sluggable(
                                                                         _("Role name must contain alphanumeric characters."),
                                                                         _("Role name is too long.")
                                                                         )])
    protected = forms.BooleanField(widget=YesNoSwitch,required=False)
    
    def finalize_form(self):
        self.layout = [
                       [
                        _("Basic Role Options"),
                        [
                         ('name', {'label': _("Role Name"), 'help_text': _("Role Name is used to identify this role in Admin Control Panel.")}),
                         ('protected', {'label': _("Protect this Role"), 'help_text': _("Only system administrators can edit or assign protected roles.")}),
                         ],
                        ],
                       ]
        
        if not self.request.user.is_god():
            del self.fields['protected']
            del self.layout[0][1][1]