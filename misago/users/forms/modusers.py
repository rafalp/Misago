from datetime import timedelta

from django.utils.translation import ugettext_lazy as _, ungettext
from django.utils import timezone

from misago.core import forms

from misago.users.forms.admin import BanUsersForm
from misago.users.models import Ban, BAN_EMAIL, BAN_USERNAME


class BanForm(BanUsersForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BanForm, self).__init__(*args, **kwargs)

        if self.user.acl_['max_ban_length']:
            message = ungettext(
                "Required. Can't be longer than %(days)s day.",
                "Required. Can't be longer than %(days)s days.",
                self.user.acl_['max_ban_length'])
            message = message % {'days': self.user.acl_['max_ban_length']}
            self['valid_until'].field.help_text = message

    def clean_valid_until(self):
        data = self.cleaned_data['valid_until']

        if self.user.acl_['max_ban_length']:
            max_ban_length = timedelta(days=self.user.acl_['max_ban_length'])
            if not data or data > (timezone.now() + max_ban_length).date():
                message = ungettext(
                    "You can't set bans longer than %(days)s day.",
                    "You can't set bans longer than %(days)s days.",
                    self.user.acl_['max_ban_length'])
                message = message % {'days': self.user.acl_['max_ban_length']}
                raise forms.ValidationError(message)
        elif data and data < timezone.now().date():
            raise forms.ValidationError(_("Expiration date is in past."))

        return data

    def ban_user(self):
        new_ban = Ban(banned_value=self.user.username,
                      user_message=self.cleaned_data['user_message'],
                      staff_message=self.cleaned_data['staff_message'],
                      valid_until=self.cleaned_data['valid_until'])
        new_ban.save()

        Ban.objects.invalidate_cache()
