from django import forms
from django.utils.translation import npgettext_lazy, pgettext_lazy

from ....admin.forms import YesNoSwitch
from ....core.validators import validate_image_square
from ....users.validators import validate_username_content
from ... import settings
from .base import SettingsForm


class UsersSettingsForm(SettingsForm):
    settings = [
        "account_activation",
        "allow_custom_avatars",
        "avatar_upload_limit",
        "default_avatar",
        "default_gravatar_fallback",
        "blank_avatar",
        "signature_length_max",
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
        label=pgettext_lazy(
            "admin users settings form", "Require new accounts activation"
        ),
        choices=[
            (
                "none",
                pgettext_lazy(
                    "admin users account activation field choice",
                    "No activation required",
                ),
            ),
            (
                "user",
                pgettext_lazy(
                    "admin users account activation field choice",
                    "Activation token sent to user e-mail",
                ),
            ),
            (
                "admin",
                pgettext_lazy(
                    "admin users account activation field choice",
                    "Activation by administrator",
                ),
            ),
            (
                "closed",
                pgettext_lazy(
                    "admin users account activation field choice",
                    "Disable new registrations",
                ),
            ),
        ],
        widget=forms.RadioSelect(),
    )
    new_inactive_accounts_delete = forms.IntegerField(
        label=pgettext_lazy(
            "admin users settings form",
            "Delete new inactive accounts if they weren't activated within this number of days",
        ),
        help_text=pgettext_lazy(
            "admin users settings form",
            "Enter 0 to never delete inactive new accounts.",
        ),
        min_value=0,
    )

    username_length_min = forms.IntegerField(
        label=pgettext_lazy(
            "admin users settings form", "Minimum allowed username length"
        ),
        min_value=2,
        max_value=20,
    )
    username_length_max = forms.IntegerField(
        label=pgettext_lazy(
            "admin users settings form", "Maximum allowed username length"
        ),
        min_value=2,
        max_value=20,
    )

    allow_custom_avatars = YesNoSwitch(
        label=pgettext_lazy("admin users settings form", "Allow custom avatar uploads"),
        help_text=pgettext_lazy(
            "admin users settings form",
            "Turning this option off will forbid forum users from uploading custom avatars.",
        ),
    )
    avatar_upload_limit = forms.IntegerField(
        label=pgettext_lazy(
            "admin users settings form", "Maximum size of uploaded avatar"
        ),
        help_text=pgettext_lazy(
            "admin users settings form",
            "Enter maximum allowed file size (in KB) for avatar uploads.",
        ),
        min_value=0,
    )
    default_avatar = forms.ChoiceField(
        label=pgettext_lazy("admin users settings form", "Default avatar"),
        choices=[
            (
                "dynamic",
                pgettext_lazy(
                    "admin users default avatar choice",
                    "Individual",
                ),
            ),
            (
                "gravatar",
                pgettext_lazy(
                    "admin users default avatar choice",
                    "Gravatar",
                ),
            ),
            (
                "gallery",
                pgettext_lazy(
                    "admin users default avatar choice",
                    "Random avatar from gallery",
                ),
            ),
        ],
        widget=forms.RadioSelect(),
    )
    default_gravatar_fallback = forms.ChoiceField(
        label=pgettext_lazy(
            "admin users settings form", "Fallback for default Gravatar"
        ),
        help_text=pgettext_lazy(
            "admin users settings form",
            "Select which avatar to use when user has no Gravatar associated with their e-mail address.",
        ),
        choices=[
            (
                "dynamic",
                pgettext_lazy("admin users gravatar fallback choice", "Individual"),
            ),
            (
                "gallery",
                pgettext_lazy(
                    "admin users gravatar fallback choice", "Random avatar from gallery"
                ),
            ),
        ],
        widget=forms.RadioSelect(),
    )
    blank_avatar = forms.ImageField(
        label=pgettext_lazy("admin users settings form", "Blank avatar"),
        help_text=pgettext_lazy(
            "admin users settings form",
            "Blank avatar is displayed in the interface when user's avatar is not available: when user was deleted or is guest. Uploaded image should be a square.",
        ),
        required=False,
    )
    blank_avatar_delete = forms.BooleanField(
        label=pgettext_lazy("admin users settings form", "Delete custom blank avatar"),
        required=False,
    )

    signature_length_max = forms.IntegerField(
        label=pgettext_lazy(
            "admin users settings form", "Maximum allowed signature length"
        ),
        min_value=10,
        max_value=5000,
    )

    users_per_page = forms.IntegerField(
        label=pgettext_lazy(
            "admin users settings form", "Number of users displayed on a single page"
        ),
        min_value=4,
    )
    users_per_page_orphans = forms.IntegerField(
        label=pgettext_lazy("admin users settings form", "Maximum orphans"),
        help_text=pgettext_lazy(
            "admin users settings form",
            "This setting prevents situations when the last page of a users list contains very few items. If number of users to be displayed on the last page is less or equal to number specified in this setting, those users will instead be appended to the previous page, reducing number of list's pages.",
        ),
        min_value=0,
    )

    top_posters_ranking_length = forms.IntegerField(
        label=pgettext_lazy(
            "admin users settings form",
            "Maximum age in days of posts that should count to the ranking position",
        ),
        min_value=1,
    )
    top_posters_ranking_size = forms.IntegerField(
        label=pgettext_lazy(
            "admin users settings form", "Maximum number of ranked users"
        ),
        min_value=2,
    )

    allow_data_downloads = YesNoSwitch(
        label=pgettext_lazy(
            "admin users settings form", "Allow users to download their data"
        )
    )
    data_downloads_expiration = forms.IntegerField(
        label=pgettext_lazy(
            "admin users settings form",
            "Maximum age in hours of data downloads before they expire",
        ),
        help_text=pgettext_lazy(
            "admin users settings form",
            "Data downloads older than specified will have their files deleted and will be marked as expired.",
        ),
        min_value=1,
    )

    allow_delete_own_account = YesNoSwitch(
        label=pgettext_lazy(
            "admin users settings form", "Allow users to delete their own accounts"
        )
    )

    ip_storage_time = forms.IntegerField(
        label=pgettext_lazy("admin users settings form", "IP storage time"),
        help_text=pgettext_lazy(
            "admin users settings form",
            "Number of days for which users IP addresses are stored in forum database. Enter zero to store registered IP addresses forever. Deleting user account always deletes the IP addresses associated with it.",
        ),
        min_value=0,
    )

    anonymous_username = forms.CharField(
        label=pgettext_lazy("admin users settings form", "Anonymous username"),
        help_text=pgettext_lazy(
            "admin users settings form",
            "This username is displayed instead of delete user's actual name next to their content.",
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
                npgettext_lazy(
                    "admin users settings form",
                    "Uploaded image's edge should be at least %(size)s pixel long.",
                    "Uploaded image's edge should be at least %(size)s pixels long.",
                    min_size,
                )
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
                pgettext_lazy(
                    "admin users settings form",
                    "This value must be lower than number of users per page.",
                ),
            )
        return cleaned_data
