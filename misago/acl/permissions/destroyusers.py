from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.forms import YesNoSwitch
from misago.acl.exceptions import ACLError403, ACLError404

def make_form(request, role, form):
    if role.special != 'guest':
        form.base_fields['can_destroy_user_older_than'] = forms.IntegerField(label=_("Maximum Age of destroyed account (in days)"),
                                                                             help_text=_("Enter zero to disable this check."),
                                                                             initial=0, min_value=0, required=False)
        form.base_fields['can_destroy_user_with_more_posts_than'] = forms.IntegerField(label=_("Maximum number of posts on destroyed account"),
                                                                                       help_text=_("Enter zero to disable this check."),
                                                                                       initial=0, min_value=0, required=False)

        form.fieldsets.append((
                               _("Destroying User Accounts"),
                               ('can_destroy_user_older_than',
                                'can_destroy_user_with_more_posts_than')
                              ))


class DestroyUserACL(BaseACL):
    def allow_destroy_user(self, user):
        if not (self.acl['can_destroy_user_older_than']
                or self.acl['can_destroy_user_with_more_posts_than']):
            raise ACLError403(_("You can't destroy user accounts."))

        if user.is_god() or user.is_team:
            raise ACLError403(_("This user account is protected and cannot be destroyed."))

        if self.acl['can_destroy_user_older_than']:
            user_age = timezone.now() - user.join_date
            if user_age.days > self.acl['can_destroy_user_older_than']:
                raise ACLError403(_("You can't destroy this user account. It's too old."))

        if (self.acl['can_destroy_user_with_more_posts_than']
                and user.posts > self.acl['can_destroy_user_with_more_posts_than']):
            raise ACLError403(_("You can't destroy this user account. Too many messages were posted from it."))

    def can_destroy_user(self, user):
        try:
            self.allow_destroy_user(user)
        except ACLError403:
            return False
        return True


def build(acl, roles):
    acl.destroyusers = DestroyUserACL()
    acl.destroyusers.acl['can_destroy_user_older_than'] = 0
    acl.destroyusers.acl['can_destroy_user_with_more_posts_than'] = 0

    for role in roles:
        try:
            if (role['can_destroy_user_older_than']
                    and role['can_destroy_user_older_than'] > acl.destroyusers.acl['can_destroy_user_older_than']):
                acl.destroyusers.acl['can_destroy_user_older_than'] = role['can_destroy_user_older_than']
            if (role['can_destroy_user_with_more_posts_than']
                    and role['can_destroy_user_with_more_posts_than'] > acl.destroyusers.acl['can_destroy_user_with_more_posts_than']):
                acl.destroyusers.acl['can_destroy_user_with_more_posts_than'] = role['can_destroy_user_with_more_posts_than']
        except KeyError:
            pass
