from dataclasses import dataclass
from functools import cached_property
from typing import Any

from django import forms
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import pgettext, pgettext_lazy

from ..permissions.accounts import check_delete_own_account_permission
from ..profile.profilefields import profile_fields
from ..users.utils import hash_email
from ..users.validators import validate_email, validate_username
from .namechanges import get_available_username_changes

User = get_user_model()


class AccountPreferencesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "limits_private_thread_invites_to",
            "watch_started_threads",
            "watch_replied_threads",
            "watch_new_private_threads_by_followed",
            "watch_new_private_threads_by_other_users",
            "notify_new_private_threads_by_followed",
            "notify_new_private_threads_by_other_users",
        ]
        widgets = {
            "limits_private_thread_invites_to": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = kwargs["instance"]

        self.fields["is_hiding_presence"] = forms.TypedChoiceField(
            coerce=int,
            choices=(
                (
                    0,
                    pgettext_lazy(
                        "account privacy choice",
                        "Show other users when I am online",
                    ),
                ),
                (
                    1,
                    pgettext_lazy(
                        "account privacy choice",
                        "Don't show other users when I am online",
                    ),
                ),
            ),
            initial=1 if user.is_hiding_presence else 0,
            widget=forms.RadioSelect(),
        )

    def save(self):
        self.instance.is_hiding_presence = self.cleaned_data.get("is_hiding_presence")
        return super().save()


class AccountNotifications:
    header: str
    items: dict[str, str]

    def __init__(self, header: str):
        self.header = header
        self.items = {}

    def add_item(self, field: str, label: str):
        self.items[field] = label

    def get_items(self, form: forms.Form) -> "AccountNotificationsItems":
        items: list["AccountNotificationsItem"] = []
        for field_name, label in self.items.items():
            items.append(
                AccountNotificationsItem(
                    label=label,
                    field=form[field_name],
                )
            )

        return AccountNotificationsItems(
            header=self.header,
            items=items,
        )


@dataclass
class AccountNotificationsItems:
    header: str
    items: list["AccountNotificationsItem"]


@dataclass
class AccountNotificationsItem:
    label: str
    field: forms.BoundField


watching_preferences = AccountNotifications(
    pgettext_lazy("account settings preferences watching", "Content")
)

watching_preferences.add_item(
    "watch_started_threads",
    pgettext_lazy(
        "account settings preferences",
        "Threads I am starting",
    ),
)
watching_preferences.add_item(
    "watch_replied_threads",
    pgettext_lazy(
        "account settings preferences",
        "Threads I am replying to",
    ),
)
watching_preferences.add_item(
    "watch_new_private_threads_by_followed",
    pgettext_lazy(
        "account settings preferences",
        "Private threads I am invited to by users I follow",
    ),
)
watching_preferences.add_item(
    "watch_new_private_threads_by_other_users",
    pgettext_lazy(
        "account settings preferences",
        "Private threads I am invited to by other users",
    ),
)

notifications_preferences = AccountNotifications(
    pgettext_lazy("account settings preferences watching", "Event")
)

notifications_preferences.add_item(
    "notify_new_private_threads_by_followed",
    pgettext_lazy(
        "account settings preferences",
        "Private threads invitations from users I follow",
    ),
)
notifications_preferences.add_item(
    "notify_new_private_threads_by_other_users",
    pgettext_lazy(
        "account settings preferences",
        "Private threads invitations from other users",
    ),
)


class AccountDetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.instance = kwargs.pop("instance")

        super().__init__(*args, **kwargs)

        self.form_data = profile_fields.get_form_data(self.request, self.instance)
        self.fields.update(self.form_data.fields)

    @property
    def fieldsets(self):
        for fieldset in self.form_data.fieldsets:
            yield {
                "name": fieldset["name"],
                "fields": (self[field] for field in fieldset["fields"]),
            }

    def clean(self):
        cleaned_data: dict[str, Any] = {}
        for field, data in dict(super().clean()).items():
            if field not in self.form_data.fields:
                continue

            try:
                cleaned_data[field] = self.form_data.clean_data(
                    field, data, self.request, self.instance
                )
            except forms.ValidationError as e:
                self.add_error(field, e)

        return cleaned_data

    def save(self):
        new_data: dict[str, Any] = {}
        for field_name in self.form_data.fields:
            if self.cleaned_data.get(field_name):
                new_data[field_name] = self.cleaned_data[field_name]

        self.instance.profile_fields = new_data
        self.instance.save(update_fields=["profile_fields"])


class AccountUsernameForm(forms.Form):
    username = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        self.instance = kwargs.pop("instance")
        self.permissions = request.user_permissions
        self.settings = request.settings
        self.username_cache = None

        super().__init__(*args, **kwargs)

        self.fields["username"].max_length = self.settings.username_length_max

    @cached_property
    def available_changes(self):
        return get_available_username_changes(self.instance, self.permissions)

    def clean_username(self):
        data = self.cleaned_data["username"]
        if data == self.instance.username:
            raise forms.ValidationError(
                pgettext(
                    "account username form",
                    "This username is the same as the current one.",
                ),
            )

        if not self.permissions.can_change_username:
            raise forms.ValidationError(
                pgettext(
                    "account username help",
                    "You can't change your username.",
                ),
            )

        if not self.available_changes.can_change_username:
            raise forms.ValidationError(
                pgettext(
                    "account username help",
                    "You can't change your username at the moment.",
                ),
            )

        validate_username(self.settings, data, self.instance)
        return data

    def clean(self):
        super().clean()

        if "username" not in self.errors:
            self["username"].value = ""

    def save(self):
        username = self.cleaned_data["username"]
        if username != self.instance.username:
            self.instance.set_username(username, changed_by=self.instance)
            self.instance.save()
            del self.available_changes

        return self.instance


class AccountPasswordForm(forms.Form):
    current_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.instance = kwargs.pop("instance")

        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        data = self.cleaned_data["current_password"]
        if not self.instance.check_password(data):
            raise forms.ValidationError(
                pgettext(
                    "account settings form",
                    "Password is incorrect.",
                ),
            )
        return data

    def clean_new_password(self):
        data = self.cleaned_data["new_password"]
        validate_password(data)
        return data

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("new_password") and cleaned_data.get(
            "confirm_password"
        ) != cleaned_data.get("new_password"):
            self.add_error(
                "confirm_password",
                pgettext(
                    "account password form",
                    "New passwords don't match.",
                ),
            )

        return cleaned_data

    def save(self):
        self.instance.set_password(self.cleaned_data["new_password"])
        self.instance.save()

        update_session_auth_hash(self.request, self.instance)

        return self.instance


class AccountEmailForm(forms.Form):
    current_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    new_email = forms.EmailField(max_length=255, widget=forms.PasswordInput)
    confirm_email = forms.EmailField(max_length=255, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.instance = kwargs.pop("instance")
        self.email_cache = None

        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        data = self.cleaned_data["current_password"]
        if not self.instance.check_password(data):
            raise forms.ValidationError(
                pgettext(
                    "account settings form",
                    "Password is incorrect.",
                ),
            )
        return data

    def clean_new_email(self):
        data = self.cleaned_data["new_email"]
        if hash_email(data) == self.instance.email_hash:
            raise forms.ValidationError(
                pgettext(
                    "account email form",
                    "This email address is the same as the current one.",
                ),
            )

        validate_email(data, self.instance)
        return data

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("new_email") and cleaned_data.get(
            "confirm_email"
        ) != cleaned_data.get("new_email"):
            self.add_error(
                "confirm_email",
                pgettext(
                    "account email form",
                    "New email addresses don't match.",
                ),
            )

        return cleaned_data


class AccountDeleteForm(forms.Form):
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput,
        required=True,
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")

        super().__init__(*args, **kwargs)

    def clean_password(self):
        data = self.cleaned_data["password"]
        if not self.instance.check_password(data):
            raise forms.ValidationError(
                pgettext(
                    "account delete form",
                    "Entered password is incorrect.",
                ),
            )

        try:
            check_delete_own_account_permission(self.instance)
        except PermissionDenied as e:
            raise forms.ValidationError(str(e))

        return data
