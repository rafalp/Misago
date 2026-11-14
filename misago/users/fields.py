from typing import TYPE_CHECKING, Union

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.translation import npgettext_lazy, pgettext_lazy

from ..core.utils import slugify

if TYPE_CHECKING:
    from ..users.models import User


class UserNotFound:
    is_anonymous = True
    is_authenticated = False

    id = None
    username: str

    __slots__ = ("username",)

    def __init__(self, username: str):
        self.username = username


class UserMultipleChoiceWidget(forms.Widget):
    template_name = "misago/widgets/user_multiple_choice.html"

    def format_value(self, value: list[Union["User", str]] | None) -> list["User"]:
        if not value:
            return None

        users = []
        for item in value:
            if isinstance(item, str):
                users.append(UserNotFound(item))
            else:
                users.append(item)

        return users

    def value_from_datadict(self, data, files, name) -> list[str]:
        raw_value = data.get(name)
        if not raw_value:
            return []

        value: list[str] = []
        unique_values: set[str] = set()

        for item in raw_value.split(","):
            item = item.strip()
            if not item:
                continue

            item_unique = item.lower()
            if item_unique in unique_values:
                continue

            value.append(item)
            unique_values.add(item_unique)

        return value


class UserMultipleChoiceField(forms.Field):
    queryset: QuerySet
    max_choices: int

    default_error_messages = {
        "invalid_choice": pgettext_lazy(
            "user multiple choice field error", "One or more users not found: %(value)s"
        ),
        "max_choices": npgettext_lazy(
            "user multiple choice field error",
            "Enter no more than %(max)d user.",
            "Enter no more than %(max)d users.",
            "max",
        ),
    }
    widget = UserMultipleChoiceWidget

    def __init__(
        self, *, queryset: QuerySet | None = None, max_choices: int = 5, **kwargs
    ):
        self.queryset = queryset or get_user_model().objects
        self.max_choices = max_choices

        super().__init__(**kwargs)

    def to_python(self, value: list[str] | None) -> list["User"]:
        if not value:
            return []

        if len(value) > self.max_choices:
            raise forms.ValidationError(
                self.error_messages["max_choices"],
                code="max_choices",
                params={"max": self.max_choices},
            )

        slugs: dict[str, str] = {}
        for username in value:
            slug = slugify(username)
            slugs[slug] = username

        queryset = self.queryset.filter(slug__in=slugs)[: self.max_choices + 5]
        users_dict = {user.slug: user for user in queryset}

        python_value = []
        for slug, username in slugs.items():
            if slug in users_dict:
                python_value.append(users_dict[slug])
            else:
                # Return "blank" user item to appear in the UI
                python_value.append(UserNotFound(username))

        if len(users_dict) != len(slugs):
            # Hack: store partially valid value for BoundField.value
            self._partial_value = python_value

            # Raise validation error
            invalid_choices = []
            for slug, username in slugs.items():
                if slug not in users_dict:
                    invalid_choices.append(username)

            raise forms.ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": ", ".join(invalid_choices)},
            )

        return python_value

    def widget_attrs(self, widget: forms.Widget) -> dict:
        return {"maxchoices": self.max_choices}

    def get_bound_field(self, form, field_name):
        return UserMultipleChoiceBoundField(form, self, field_name)


class UserMultipleChoiceBoundField(forms.BoundField):
    def value(self):
        if hasattr(self.form, "cleaned_data") and self.name in self.form.cleaned_data:
            return self.form.cleaned_data[self.name]

        if partial_value := getattr(self.field, "_partial_value", None):
            return partial_value

        return super().value()

    def max_choices(self) -> int:
        return self.field.max_choices
