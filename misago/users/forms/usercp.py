from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from misago.core import forms, timezones
from misago.users.models import (PRESENCE_VISIBILITY_CHOICES,
                                 AUTO_SUBSCRIBE_CHOICES)


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


class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'title']


class ChangeEmailPasswordForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'title']
