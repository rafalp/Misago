from datetime import timedelta
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    if role.token != 'guest':
        form.base_fields['name_changes_allowed'] = forms.IntegerField(min_value=0,initial=1)
        form.base_fields['changes_expire'] = forms.IntegerField(min_value=0,initial=0)
        form.base_fields['can_use_signature'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
        form.base_fields['allow_signature_links'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
        form.base_fields['allow_signature_images'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
        form.layout.append((
                            _("User Profile"),
                            (
                             ('name_changes_allowed', {'label': _("Allowed Username changes number"), 'help_text': _("Enter zero to don't allow users with this role to change their names.")}),
                             ('changes_expire', {'label': _("Don't count username changes older than"), 'help_text': _("Number of days since name change that makes that change no longer count to limit. For example, if you enter 7 days and set changes limit 3, users with this rank will not be able to make more than three changes in duration of 7 days. Enter zero to make all changes count.")}),
                             ('can_use_signature', {'label': _("Can have signature")}),
                             ('allow_signature_links', {'label': _("Can put links in signature")}),
                             ('allow_signature_images', {'label': _("Can put images in signature")}),
                             ),
                            ))


class UserCPACL(BaseACL):        
    def show_username_change(self):
        return self.acl['name_changes_allowed'] > 0
    
    def changes_expire(self):
        return self.acl['changes_expire'] > 0
    
    def changes_left(self, user):
        if not self.acl['name_changes_allowed']:
            return 0
        
        if self.acl['changes_expire']:
            changes_left = self.acl['name_changes_allowed'] - user.namechanges.filter(
                                                    date__gte=timezone.now() - timedelta(days=self.acl['changes_expire']),
                                                    ).count()
        else:
            changes_left = self.acl['name_changes_allowed'] - user.namechanges.all().count()
            
        if changes_left:
            return changes_left
        return 0
    
    def can_use_signature(self):
        return self.acl['signature']
    
    def allow_signature_links(self):
        return self.acl['signature_links']
    
    def allow_signature_images(self):
        return self.acl['signature_images']


def build(acl, roles):
    acl.usercp = UserCPACL()
    acl.usercp.acl['name_changes_allowed'] = 0
    acl.usercp.acl['changes_expire'] = 0
    acl.usercp.acl['signature'] = False
    acl.usercp.acl['signature_links'] = False
    acl.usercp.acl['signature_images'] = False
    
    for role in roles:
        if 'name_changes_allowed' in role and role['name_changes_allowed'] > acl.usercp.acl['name_changes_allowed']:
            acl.usercp.acl['name_changes_allowed'] = role['name_changes_allowed']

        if 'changes_expire' in role and role['changes_expire'] > acl.usercp.acl['changes_expire']:
            acl.usercp.acl['changes_expire'] = role['changes_expire']
            
        if 'can_use_signature' in role and role['can_use_signature'] > acl.usercp.acl['signature']:
            acl.usercp.acl['signature'] = role['can_use_signature']
            
        if 'allow_signature_links' in role and role['allow_signature_links'] > acl.usercp.acl['signature_links']:
            acl.usercp.acl['signature_links'] = role['allow_signature_links']
            
        if 'allow_signature_images' in role and role['allow_signature_images'] > acl.usercp.acl['signature_images']:
            acl.usercp.acl['signature_images'] = role['allow_signature_images']
