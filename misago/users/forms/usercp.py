from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _, ungettext

from misago.conf import settings
from misago.core import forms, timezones

from misago.users.models import (AUTO_SUBSCRIBE_CHOICES,
                                 PRIVATE_THREAD_INVITES_LIMITS_CHOICES)
from misago.users.validators import validate_email, validate_password


class ChangeForumOptionsBaseForm(forms.ModelForm):
    timezone = forms.ChoiceField(
        label=_("Your current timezone"), choices=[],
        help_text=_("If dates and hours displayed by forums are inaccurate, "
                    "you can fix it by adjusting timezone setting."))

    is_hiding_presence = forms.YesNoSwitch(
        label=_("Hide my presence"),
        help_text=_("If you hide your presence, only members with permission "
                    "to see hidden will see when you are online."))

    limits_private_thread_invites_to = forms.TypedChoiceField(
        label=_("Who can add me to private threads"),
        coerce=int,
        choices=PRIVATE_THREAD_INVITES_LIMITS_CHOICES)

    subscribe_to_started_threads = forms.TypedChoiceField(
        label=_("Threads I start"), coerce=int, choices=AUTO_SUBSCRIBE_CHOICES)

    subscribe_to_replied_threads = forms.TypedChoiceField(
        label=_("Threads I reply to"), coerce=int,
        choices=AUTO_SUBSCRIBE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = [
            'timezone',
            'is_hiding_presence',
            'limits_private_thread_invites_to',
            'subscribe_to_started_threads',
            'subscribe_to_replied_threads'
        ]


def ChangeForumOptionsForm(*args, **kwargs):
    timezone = forms.ChoiceField(
        label=_("Your current timezone"), choices=timezones.choices(),
        help_text=_("If dates and hours displayed by forums are inaccurate, "
                    "you can fix it by adjusting timezone setting."))

    FinalFormType = type('FinalChangeForumOptionsForm',
                         (ChangeForumOptionsBaseForm,),
                         {'timezone': timezone})
    return FinalFormType(*args, **kwargs)


class EditSignatureForm(forms.ModelForm):
    signature = forms.CharField(label=_("Signature"), required=False)

    class Meta:
        model = get_user_model()
        fields = ['signature']

    def clean(self):
        data = super(EditSignatureForm, self).clean()

        length_limit = settings.signature_length_max
        if len(data) > length_limit:
            raise forms.ValidationError(ungettext(
                "Signature can't be longer than %(limit)s character.",
                "Signature can't be longer than %(limit)s characters.",
                length_limit) % {'limit': length_limit})

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
