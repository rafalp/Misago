from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    if role.special != 'guest':
        form.base_fields['can_warn_members'] = forms.BooleanField(label=_("Can warn members"),
                                                                  widget=YesNoSwitch, initial=False, required=False)

        form.fieldsets.append((
                               _("Warning Members"),
                               ('can_warn_members',)
                              ))


class WarningsACL(BaseACL):
    def can_warn_members(self):
        return self.acl['can_warn_members']


def build(acl, roles):
    acl.warnings = WarningsACL()
    acl.warnings.acl['can_warn_members'] = False

    for role in roles:
        try:
            if role['can_warn_members']:
                acl.warnings.acl['can_warn_members'] = True
        except KeyError:
            pass
