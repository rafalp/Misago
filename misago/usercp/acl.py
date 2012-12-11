from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    form.base_fields['can_use_signature'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.layout.append((
                        _("Signature"),
                        (('can_use_signature', {'label': _("Can have signature")}),),
                        ))


class UserCPACL(BaseACL):
    def can_use_signature(self):
        return self.acl['signature']


def build(acl, roles):
    acl.usercp = UserCPACL()
    acl.usercp.acl['signature'] = False
    
    for role in roles:
        if 'can_use_signature' in role and role['can_use_signature'] > acl.usercp.acl['signature']:
            acl.usercp.acl['signature'] = role['can_use_signature']

