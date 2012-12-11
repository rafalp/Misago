from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    if role.token != 'admin' and request.user.is_god():
        form.base_fields['can_use_acp'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
        form.layout.append((
                            _("Admin Control Panel"),
                            (('can_use_acp', {'label': _("Can use Admin Control Panel"), 'help_text': _("Change this permission to yes to grant admin access for users with this role.")}),),
                            ))


class AdminACL(BaseACL):
    def is_admin(self):
        return self.acl['can_use_acp']
    

def build(acl, roles):
    acl.admin = AdminACL()
    acl.admin.acl['can_use_acp'] = False
    
    for role in roles:
        if 'can_use_acp' in role and role['can_use_acp'] > acl.admin.acl['can_use_acp']:
            acl.admin.acl['can_use_acp'] = role['can_use_acp']