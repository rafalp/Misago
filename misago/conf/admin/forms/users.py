from django import forms
from django.utils.translation import gettext_lazy as _

from ....admin.forms import YesNoSwitch
from ....core.validators import validate_image_square
from ....users.validators import validate_username_content
from ... import settings
from .base import ChangeSettingsForm


class ChangeUsersSettingsForm(ChangeSettingsForm):
    settings = [
        "account_activation",
        "allow_custom_avatars",
        "avatar_upload_limit",
        "default_avatar",
        "default_gravatar_fallback",
        "blank_avatar",
        "signature_length_max",
        "subscribe_reply",
        "subscribe_start",
        "username_length_max",
        "username_length_min",
        "anonymous_username",
        "users_per_page",
        "users_per_page_orphans",
        "top_posters_ranking_length",
        "top_posters_ranking_size",
        "allow_data_downloads",
        "data_downloads_expiration",
        "allow_delete_own_account",
        "new_inactive_accounts_delete",
        "ip_storage_time",
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
    new_inactive_accounts_delete = forms.IntegerField(
        label=_(
            "Delete new inactive accounts if they weren't activated "
            "within this number of days"
        ),
        help_text=_("Enter 0 to never delete inactive new accounts."),
        min_value=0,
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
    blank_avatar = forms.ImageField(
        label=_("Blank avatar"),
        help_text=_(
            "Blank avatar is displayed in the interface when user's avatar is not "
            "available: when user was deleted or is guest. Uploaded image should be "
            "a square."
        ),
        required=False,
    )
    blank_avatar_delete = forms.BooleanField(
        label=_("Delete custom blank avatar"), required=False
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

    users_per_page = forms.IntegerField(
        label=_("Number of users displayed on a single page"), min_value=4
    )
    users_per_page_orphans = forms.IntegerField(
        label=_("Maximum orphans"),
        help_text=_(
            "If number of users to be displayed on the last page is less or equal to "
            "number specified in this setting, those users will instead be displayed "
            "on previous page, reducing the total number of pages on the list."
        ),
        min_value=0,
    )

    top_posters_ranking_length = forms.IntegerField(
        label=_("Maximum age in days of posts that should count to the ranking"),
        min_value=1,
    )
    top_posters_ranking_size = forms.IntegerField(
        label=_("Maximum number of ranked users"), min_value=2
    )

    allow_data_downloads = YesNoSwitch(label=_("Allow users to download their data"))
    data_downloads_expiration = forms.IntegerField(
        label=_("Maximum age in hours of data downloads before they expire"),
        help_text=_(
            "Data downloads older than specified will have their files deleted and "
            "will be marked as expired."
        ),
        min_value=1,
    )

    allow_delete_own_account = YesNoSwitch(
        label=_("Allow users to delete their own accounts")
    )

    ip_storage_time = forms.IntegerField(
        label=_("IP storage time"),
        help_text=_(
            "Number of days for which users IP addresses are stored in forum database. "
            "Enter zero to store registered IP addresses forever. Deleting user "
            "account always deletes the IP addresses associated with it."
        ),
        min_value=0,
    )

    anonymous_username = forms.CharField(
        label=_("Anonymous username"),
        help_text=_(
            "This username is displayed instead of delete user's actual name "
            "next to their content."
        ),
        min_length=1,
        max_length=15,
        validators=[validate_username_content],
    )

    def clean_blank_avatar(self):
        upload = self.cleaned_data.get("blank_avatar")
        if not upload or upload == self.initial.get("blank_avatar"):
            return None

        validate_image_square(upload.image)
        min_size = max(settings.MISAGO_AVATARS_SIZES)
        if upload.image.width < min_size:
            raise forms.ValidationError(
                _("Uploaded image's edge should be at least %(size)s pixels long.")
                % {"size": min_size}
            )

        return upload

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("users_per_page_orphans") > cleaned_data.get(
            "users_per_page"
        ):
            self.add_error(
                "users_per_page_orphans",
                _("This value must be lower than number of users per page."),
            )
        return cleaned_data
