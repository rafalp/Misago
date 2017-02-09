from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from misago.conf import settings
from misago.core.forms import YesNoSwitch

from misago.users.bans import ban_user


class ModerateAvatarForm(forms.ModelForm):
    is_avatar_locked = YesNoSwitch()
    avatar_lock_user_message = forms.CharField(required=False)
    avatar_lock_staff_message = forms.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'is_avatar_locked',
            'avatar_lock_user_message',
            'avatar_lock_staff_message',
        ]


class ModerateSignatureForm(forms.ModelForm):
    signature = forms.CharField(
        label=_("Signature contents"),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)
    is_signature_locked = YesNoSwitch(
        label=_("Lock signature"),
        help_text=_("Setting this to yes will stop user from "
                    "making changes to his/her signature."))
    signature_lock_user_message = forms.CharField(
        label=_("User message"),
        help_text=_("Optional message to user explaining "
                    "why his/hers signature is locked."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)
    signature_lock_staff_message = forms.CharField(
        label=_("Staff message"),
        help_text=_("Optional message to team members explaining "
                    "why user signature is locked."),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'signature',
            'is_signature_locked',
            'signature_lock_user_message',
            'signature_lock_staff_message'
        ]

    def clean_signature(self):
        data = self.cleaned_data['signature']

        length_limit = settings.signature_length_max
        if len(data) > length_limit:
            raise forms.ValidationError(ungettext(
                "Signature can't be longer than %(limit)s character.",
                "Signature can't be longer than %(limit)s characters.",
                length_limit) % {'limit': length_limit})

        return data


class BanForm(forms.Form):
    user_message = forms.CharField(
        label=_("User message"), required=False, max_length=1000,
        help_text=_("Optional message displayed to user "
                    "instead of default one."),
        widget=forms.Textarea(attrs={'rows': 3}),
        error_messages={
            'max_length': _("Message can't be longer than 1000 characters.")
        })
    staff_message = forms.CharField(
        label=_("Team message"), required=False, max_length=1000,
        help_text=_("Optional ban message for moderators and administrators."),
        widget=forms.Textarea(attrs={'rows': 3}),
        error_messages={
            'max_length': _("Message can't be longer than 1000 characters.")
        })
    expires_on = forms.DateTimeField(
        label=_("Expires on"),
        required=False, localize=True,
        help_text=_('Leave this field empty for this ban to never expire.'))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BanForm, self).__init__(*args, **kwargs)

        if self.user.acl_['max_ban_length']:
            message = ungettext(
                "Required. Can't be longer than %(days)s day.",
                "Required. Can't be longer than %(days)s days.",
                self.user.acl_['max_ban_length'])
            message = message % {'days': self.user.acl_['max_ban_length']}
            self['expires_on'].field.help_text = message

    def clean_expires_on(self):
        data = self.cleaned_data['expires_on']

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
        ban_user(self.user,
                 user_message=self.cleaned_data['user_message'],
                 staff_message=self.cleaned_data['staff_message'],
                 expires_on=self.cleaned_data['expires_on'])
