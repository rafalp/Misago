from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form, YesNoSwitch
from misago.validators import validate_sluggable

class RoleForm(Form):
    name = forms.CharField(label=_("Role Name"),
                           help_text=_("Role Name is used to identify this role in Admin Control Panel."),
                           max_length=255,validators=[validate_sluggable(
                                                                         _("Role name must contain alphanumeric characters."),
                                                                         _("Role name is too long.")
                                                                         )])
    protected = forms.BooleanField(label=_("Protect this Role"),
                                   help_text=_("Only system administrators can edit or assign protected roles."),
                                   widget=YesNoSwitch,required=False)

    def finalize_form(self):
        if not self.request.user.is_god():
            del self.fields['protected']