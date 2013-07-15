import floppyforms as forms
from django.utils.translation import ugettext_lazy as _
from misago.apps.threadtype.posting.forms import (NewThreadForm as NewThreadBaseForm,
                                                  EditThreadForm as EditThreadBaseForm,
                                                  NewReplyForm as NewReplyBaseForm,
                                                  EditReplyForm as EditReplyBaseForm)
from misago.forms import Form
from misago.models import User
from misago.utils.strings import slugify

class InviteUsersMixin(object):
    def type_fields(self):
        self.fields['invite_users'] = forms.CharField(label=_("Invite members to thread"),
                                                      max_length=255,
                                                      required=False)

    def clean_invite_users(self):
        self.invite_users = []
        usernames = []
        slugs = [self.request.user.username_slug]
        for username in self.cleaned_data['invite_users'].split(','):
            username = username.strip()
            slug = slugify(username)
            if len(slug) >= 3 and not slug in slugs:
                slugs.append(slug)
                usernames.append(username)
                try:
                    user = User.objects.get(username_slug=slug)
                    if not user.acl(self.request).private_threads.can_participate():
                        raise forms.ValidationError(_('%(user)s cannot participate in private threads.') % {'user': user.username})
                    if (not self.request.acl.private_threads.can_invite_ignoring() and
                            not user.allow_pd_invite(self.request.user)):
                        raise forms.ValidationError(_('%(user)s restricts who can invite him to private threads.') % {'user': user.username})
                    self.invite_users.append(user)
                except User.DoesNotExist:
                    raise forms.ValidationError(_('User "%(username)s" could not be found.') % {'username': username})
            if len(usernames) > 8:
                raise forms.ValidationError(_('You cannot invite more than 8 members at single time. Post thread and then invite additional members.'))
        return ', '.join(usernames)


class NewThreadForm(NewThreadBaseForm, InviteUsersMixin):
    include_thread_weight = False
    include_close_thread = False


class EditThreadForm(EditThreadBaseForm):
    include_thread_weight = False
    include_close_thread = False


class NewReplyForm(NewReplyBaseForm, InviteUsersMixin):
    include_thread_weight = False
    include_close_thread = False


class EditReplyForm(EditReplyBaseForm):
    include_thread_weight = False
    include_close_thread = False


class InviteMemberForm(Form):
    username = forms.CharField(max_length=200)