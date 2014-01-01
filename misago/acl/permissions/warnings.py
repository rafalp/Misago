from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.acl.exceptions import ACLError403, ACLError404
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    if role.special != 'guest':
        form.base_fields['can_warn_members'] = forms.BooleanField(label=_("Can warn other members"),
                                                                  widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_see_other_members_warns'] = forms.BooleanField(label=_("Can see other members warnings"),
                                                                             widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_cancel_warnings'] = forms.BooleanField(label=_("Can cancel warnings"),
                                                                     widget=forms.Select, initial=0, coerce=int,
                                                                     choices=(
                                                                        (0, _("No")),
                                                                        (1, _("If is warning giver")),
                                                                        (2, _("Yes, all warnings")),
                                                                     ))
        form.base_fields['can_cancel_warnings_newer_than'] = forms.IntegerField(label=_("Maximum age of warning that can be canceled (in minutes)"),
                                                                                help_text=_("Enter zero to disable this limitation."),
                                                                                min_value=0, initial=15)
        form.base_fields['can_delete_warnings'] = forms.BooleanField(label=_("Can delete warnings"),
                                                                     widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_be_warned'] = forms.BooleanField(label=_("Can be warned"),
                                                               widget=YesNoSwitch, initial=False, required=False)

        form.fieldsets.append((
                               _("Warning Members"),
                               ('can_warn_members', 'can_see_other_members_warns',
                                'can_cancel_warnings', 'can_cancel_warnings_newer_than',
                                'can_delete_warnings', 'can_be_warned',)
                              ))


class WarningsACL(BaseACL):
    def allow_warning_members(self):
        if not self.acl['can_warn_members']:
            raise ACLError403(_("You can't warn other members."))

    def can_warn_members(self):
        try:
            self.allow_warning_members()
            return True
        except ACLError403:
            return False

    def allow_member_warns_view(self, user, other_user):
        try:
            if user.pk == other_user.pk:
                return
        except AttributeError:
            pass
        if not self.acl['can_see_other_members_warns']:
            raise ACLError403(_("You don't have permission to see this member warnings."))

    def can_see_member_warns(self, user, other_user):
        try:
            self.allow_member_warns_view(user, other_user)
            return True
        except ACLError403:
            return False

    def allow_warning(self):
        if not self.acl['can_be_warned']:
            raise ACLError403(_("This member can't be warned."))

    def can_be_warned(self):
        try:
            self.allow_warning()
            return True
        except ACLError403:
            return False


def build(acl, roles):
    acl.warnings = WarningsACL()
    acl.warnings.acl['can_warn_members'] = False
    acl.warnings.acl['can_see_other_members_warns'] = False
    acl.warnings.acl['can_be_warned'] = True
    acl.warnings.acl['can_cancel_warnings'] = 1
    acl.warnings.acl['can_cancel_warnings_newer_than'] = 5
    acl.warnings.acl['can_delete_warnings'] = False

    for role in roles:
        try:
            if role['can_warn_members']:
                acl.warnings.acl['can_warn_members'] = True
            if role['can_see_other_members_warns']:
                acl.warnings.acl['can_see_other_members_warns'] = True
            if role['can_be_warned']:
                acl.warnings.acl['can_be_warned'] = True
            if role['can_cancel_warnings'] > acl.warnings.acl['can_cancel_warnings']:
                acl.warnings.acl['can_cancel_warnings'] = role['can_cancel_warnings']
            if (role['can_cancel_warnings_newer_than'] == 0
                    or role['can_cancel_warnings_newer_than'] > acl.warnings.acl['can_cancel_warnings_newer_than']):
                acl.warnings.acl['can_cancel_warnings_newer_than'] = role['can_cancel_warnings_newer_than']
            if role['can_delete_warnings']:
                acl.warnings.acl['can_delete_warnings'] = True
        except KeyError:
            pass
