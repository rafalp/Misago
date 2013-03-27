from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    if not role.special and request.user.is_god():
        form.base_fields['can_use_mcp'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_use_acp'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
        form.layout.append((_("Special Access"),
                            (
                             ('can_use_mcp', {'label': _("Can use Moderator Control Panel"), 'help_text': _("Change this permission to yes to grant access to Mod CP for users with this role.")}),
                             ('can_use_acp', {'label': _("Can use Admin Control Panel"), 'help_text': _("Change this permission to yes to grant admin access for users with this role.")}),
                             )
                            ))


class SpecialACL(BaseACL):
    def is_admin(self):
        return self.acl['can_use_acp']

    def can_use_mcp(self):
        return self.acl['can_use_mcp']


def build(acl, roles):
    acl.special = SpecialACL()
    acl.special.acl['can_use_acp'] = False
    acl.special.acl['can_use_mcp'] = False

    for role in roles:
        try:
            if role['can_use_acp']:
                acl.special.acl['can_use_acp'] = True
            if 'can_use_mcp' in role and role['can_use_mcp']:
                acl.special.acl['can_use_mcp'] = True
        except KeyError:
            pass

    if acl.special.acl['can_use_acp'] or acl.special.acl['can_use_mcp']:
        acl.team = True
