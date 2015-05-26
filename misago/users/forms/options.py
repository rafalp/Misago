from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _, ungettext

from misago.conf import settings
from misago.core import forms

from misago.users.models import (AUTO_SUBSCRIBE_CHOICES,
                                 PRIVATE_THREAD_INVITES_LIMITS_CHOICES)
from misago.users.validators import validate_email, validate_password


class ForumOptionsForm(forms.ModelForm):
    is_hiding_presence = forms.YesNoSwitch()

    limits_private_thread_invites_to = forms.TypedChoiceField(
        coerce=int, choices=PRIVATE_THREAD_INVITES_LIMITS_CHOICES)

    subscribe_to_started_threads = forms.TypedChoiceField(
        coerce=int, choices=AUTO_SUBSCRIBE_CHOICES)

    subscribe_to_replied_threads = forms.TypedChoiceField(
        coerce=int, choices=AUTO_SUBSCRIBE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = [
            'is_hiding_presence',
            'limits_private_thread_invites_to',
            'subscribe_to_started_threads',
            'subscribe_to_replied_threads'
        ]


class EditSignatureForm(forms.ModelForm):
    signature = forms.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['signature']

    def clean(self):
        data = super(EditSignatureForm, self).clean()

        if len(data.get('signature', '')) > settings.signature_length_max:
            raise forms.ValidationError(_("Signature is too long."))

        return data


class ChangeEmailPasswordForm(forms.Form):
    current_password = forms.CharField(
        label=_("Current password"),
        max_length=200,
        required=False,
        widget=forms.PasswordInput())

    new_email = forms.CharField(
        label=_("New e-mail"),
        max_length=200,
        required=False)

    new_password = forms.CharField(
        label=_("New password"),
        max_length=200,
        required=False,
        widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeEmailPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(ChangeEmailPasswordForm, self).clean()

        current_password = data.get('current_password')
        new_email = data.get('new_email')
        new_password = data.get('new_password')

        if not data.get('current_password'):
            message = _("You have to enter your current password.")
            raise forms.ValidationError(message)

        if not self.user.check_password(current_password):
            raise forms.ValidationError(_("Entered password is invalid."))

        if not (new_email or new_password):
            message = _("You have to enter new e-mail or password.")
            raise forms.ValidationError(message)

        if new_email:
            if new_email.lower() == self.user.email.lower():
                message = _("New e-mail is same as current one.")
                raise forms.ValidationError(message)
            validate_email(new_email)

        if new_password:
            validate_password(new_password)

        return data
