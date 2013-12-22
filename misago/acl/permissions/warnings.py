from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    if role.special != 'guest':
        form.base_fields['can_warn_members'] = forms.BooleanField(label=_("Can warn members"),
                                                                  widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_see_other_members_warns'] = forms.BooleanField(label=_("Can see other members warnings"),
                                                                             widget=YesNoSwitch, initial=False, required=False)


        form.fieldsets.append((
                               _("Warning Members"),
                               ('can_warn_members', 'can_see_other_members_warns',)
                              ))


class WarningsACL(BaseACL):
    def can_warn_members(self):
        return self.acl['can_warn_members']

    def can_see_member_warns(self, user, other_user):
        if user.pk == other_user.pk:
            return Ture
        return self.acl['can_see_other_members_warns']


def build(acl, roles):
    acl.warnings = WarningsACL()
    acl.warnings.acl['can_warn_members'] = False
    acl.warnings.acl['can_see_other_members_warns'] = False

    for role in roles:
        try:
            if role['can_warn_members']:
                acl.warnings.acl['can_warn_members'] = True
            if role['can_see_other_members_warns']:
                acl.warnings.acl['can_see_other_members_warns'] = True
        except KeyError:
            pass
