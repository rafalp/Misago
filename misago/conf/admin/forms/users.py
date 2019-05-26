from django import forms
from django.utils.translation import gettext_lazy as _

from ....admin.forms import YesNoSwitch
from .base import ChangeSettingsForm


class ChangeUsersSettingsForm(ChangeSettingsForm):
    settings = [
        "account_activation",
        "allow_custom_avatars",
        "avatar_upload_limit",
        "default_avatar",
        "default_gravatar_fallback",
        "signature_length_max",
        "subscribe_reply",
        "subscribe_start",
        "username_length_max",
        "username_length_min",
    ]

    account_activation = forms.ChoiceField(
        label=_("Require new accounts activation"),
        choices=[
            ("none", _("No activation required")),
            ("user", _("Activation token sent to user e-mail")),
            ("admin", _("Activation by administrator")),
            ("closed", _("Disable new registrations")),
        ],
        widget=forms.RadioSelect(),
    )
    username_length_min = forms.IntegerField(
        label=_("Minimum allowed username length"), min_value=2, max_value=20
    )
    username_length_max = forms.IntegerField(
        label=_("Maximum allowed username length"), min_value=2, max_value=20
    )
    allow_custom_avatars = YesNoSwitch(
        label=_("Allow custom avatar uploads"),
        help_text=_(
            "Turning this option off will forbid forum users from uploading custom "
            "avatars. Good for forums adressed at young users."
        ),
    )
    avatar_upload_limit = forms.IntegerField(
        label=_("Maximum size of uploaded avatar"),
        help_text=_("Enter maximum allowed file size (in KB) for avatar uploads."),
        min_value=0,
    )
    default_avatar = forms.ChoiceField(
        label=_("Default avatar"),
        choices=[
            ("dynamic", _("Individual")),
            ("gravatar", _("Gravatar")),
            ("gallery", _("Random avatar from gallery")),
        ],
        widget=forms.RadioSelect(),
    )
    default_gravatar_fallback = forms.ChoiceField(
        label=_("Fallback for default gravatar"),
        help_text=_(
            "Select which avatar to use when user has no gravatar associated with "
            "their e-mail address."
        ),
        choices=[
            ("dynamic", _("Individual")),
            ("gallery", _("Random avatar from gallery")),
        ],
        widget=forms.RadioSelect(),
    )
    signature_length_max = forms.IntegerField(
        label=_("Maximum allowed signature length"), min_value=10, max_value=5000
    )
    subscribe_start = forms.ChoiceField(
        label=_("Started threads"),
        choices=[
            ("no", _("Don't watch")),
            ("watch", _("Put on watched threads list")),
            (
                "watch_email",
                _("Put on watched threads list and e-mail user when somebody replies"),
            ),
        ],
        widget=forms.RadioSelect(),
    )
    subscribe_reply = forms.ChoiceField(
        label=_("Replied threads"),
        choices=[
            ("no", _("Don't watch")),
            ("watch", _("Put on watched threads list")),
            (
                "watch_email",
                _("Put on watched threads list and e-mail user when somebody replies"),
            ),
        ],
        widget=forms.RadioSelect(),
    )
