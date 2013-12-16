from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    if not role.special and request.user.is_god():
        form.base_fields['can_use_acp'] = forms.BooleanField(label=_("Can use Admin Control Panel"),
                                                             help_text=_("Change this permission to yes to grant admin access for users with this role."),
                                                             widget=YesNoSwitch, initial=False, required=False)

        form.fieldsets.append((
                               _("Admin Control Panel"),
                               ('can_use_acp',)
                              ))


class ACPAccessACL(BaseACL):
    def is_admin(self):
        return self.acl['can_use_acp']


def build(acl, roles):
    acl.acp = ACPAccessACL()
    acl.acp.acl['can_use_acp'] = False

    for role in roles:
        try:
            if role['can_use_acp']:
                acl.acp.acl['can_use_acp'] = True
        except KeyError:
            pass

    if acl.acp.acl['can_use_acp']:
        acl.team = True
