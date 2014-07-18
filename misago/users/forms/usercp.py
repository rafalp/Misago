from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from misago.core import forms, timezones
from misago.users.models import (PRESENCE_VISIBILITY_CHOICES,
                                 AUTO_SUBSCRIBE_CHOICES)
from misago.users.validators import validate_username


class ChangeForumOptionsBaseForm(forms.ModelForm):
    timezone = forms.ChoiceField(
        label=_("Your current timezone"), choices=[],
        help_text=_("If dates and hours displayed by forums are inaccurate, "
                    "you can fix it by adjusting timezone setting."))

    presence_visibility = forms.TypedChoiceField(
        label=_("Show my presence to"),
        choices=PRESENCE_VISIBILITY_CHOICES, coerce=int,
        help_text=_("If you want to, you can limit other members ability to "
                    "track your presence on forums."))

    subscribe_to_started_threads = forms.TypedChoiceField(
        label=_("Threads I start"), coerce=int, choices=AUTO_SUBSCRIBE_CHOICES)

    subscribe_to_replied_threads = forms.TypedChoiceField(
        label=_("Threads I reply to"), coerce=int,
        choices=AUTO_SUBSCRIBE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ['timezone', 'presence_visibility',
                  'subscribe_to_started_threads',
                  'subscribe_to_replied_threads']


def ChangeForumOptionsForm(*args, **kwargs):
    timezone = forms.ChoiceField(
        label=_("Your current timezone"), choices=timezones.choices(),
        help_text=_("If dates and hours displayed by forums are inaccurate, "
                    "you can fix it by adjusting timezone setting."))

    FinalFormType = type('FinalChangeForumOptionsForm',
                         (ChangeForumOptionsBaseForm,),
                         {'timezone': timezone})
    return FinalFormType(*args, **kwargs)


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(label=_("New username"), max_length=200,
                                   required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(ChangeUsernameForm, self).clean()
        new_username = data.get('new_username')

        if not new_username:
            raise forms.ValidationError(_("Enter new username."))

        if new_username == self.user.username:
            message = _("New username is same as current one.")
            raise forms.ValidationError(message)

        validate_username(new_username, exclude=self.user)

        return data


class ChangeEmailPasswordForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'title']
