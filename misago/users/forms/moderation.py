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
