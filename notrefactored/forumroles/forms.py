from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.forms import Form
from misago.utils.validators import validate_sluggable

class ForumRoleForm(Form):
    name = forms.CharField(max_length=255, validators=[validate_sluggable(
                                                                         _("Role name must be sluggable."),
                                                                         _("Role name is too long.")
                                                                         )])

    def finalize_form(self):
        self.layout = (
                       (
                        _("Basic Role Options"),
                        (
                         ('name', {'label': _("Role Name"), 'help_text': _("Role Name is used to identify this role in Admin Control Panel.")}),
                         ),
                        ),
                       )
