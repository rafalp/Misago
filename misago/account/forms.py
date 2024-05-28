from dataclasses import dataclass

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import pgettext, pgettext_lazy

from ..users.validators import validate_username

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


class AccountUsernameForm(forms.Form):
    username = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")
        self.settings = kwargs.pop("settings")
        self.username_cache = None

        super().__init__(*args, **kwargs)

        self.fields["username"].max_length = self.settings.username_length_max

    def clean_username(self):
        data = self.cleaned_data["username"]
        if data == self.instance.username:
            return data

        validate_username(self.settings, data, self.instance)
        return data

    def clean(self):
        super().clean()
        self["username"].value = ""

    def save(self):
        username = self.cleaned_data["username"]
        if username != self.instance.username:
            self.instance.set_username(username, changed_by=self.instance)
            self.instance.save()

        return self.instance
