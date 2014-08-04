from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _, ungettext
from django.utils import timezone

from misago.conf import settings
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


class ModerateAvatarForm(forms.ModelForm):
    is_avatar_banned = forms.YesNoSwitch(
        label=_("Ban avatar changes"),
        help_text=_("Setting this to yes will ban user from "
                    "changing his/her avatar, and will reset "
                    "his/her avatar to procedurally generated one."))
    avatar_ban_user_message = forms.CharField(
        label=_("User ban message"),
        help_text=_("Optional message for user explaining "
                    "why he/she is banned form changing avatar."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)
    avatar_ban_staff_message = forms.CharField(
        label=_("Staff ban message"),
        help_text=_("Optional message for forum team members explaining "
                    "why user is banned form changing avatar."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)

    class Meta:
        model = get_user_model()
        fields = ['is_avatar_banned', 'avatar_ban_user_message',
                  'avatar_ban_staff_message']


class ModerateSignatureForm(forms.ModelForm):
    signature = forms.CharField(
        label=_("Signature contents"),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)
    is_signature_banned = forms.YesNoSwitch(
        label=_("Ban signature changes"),
        help_text=_("Setting this to yes will ban user from "
                    "making changes to his/her signature."))
    signature_ban_user_message = forms.CharField(
        label=_("User ban message"),
        help_text=_("Optional message for user explaining "
                    "why he/she is banned form editing signature."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)
    signature_ban_staff_message = forms.CharField(
        label=_("Staff ban message"),
        help_text=_("Optional message for forum team members explaining "
                    "why user is banned form editing signature."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)

    class Meta:
        model = get_user_model()
        fields = ['signature', 'is_signature_banned',
                  'signature_ban_user_message', 'signature_ban_staff_message']

    def clean_signature(self):
        data = self.cleaned_data['signature']

        length_limit = settings.signature_length_max
        if len(data) > length_limit:
            raise forms.ValidationError(ungettext(
                "Signature can't be longer than %(limit)s character.",
                "Signature can't be longer than %(limit)s characters.",
                length_limit) % {'limit': length_limit})

        return data

