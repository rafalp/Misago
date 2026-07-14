from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.translation import npgettext_lazy, pgettext_lazy

from ..core.utils import slugify

if TYPE_CHECKING:
    from ..users.models import User


class UserNotFound:
    id = None
    username: str

    __slots__ = ("username",)

    def __init__(self, username: str):
        self.username = username


class UserMultipleChoiceWidget(forms.Widget):
    template_name = "misago/widgets/user_multiple_choice.html"

    def format_value(self, value: list["User"] | list[str] | None) -> str | None:
        if not value:
            return None

        usernames = []
        for item in value:
            if isinstance(item, str):
                usernames.append(item)
            else:
                usernames.append(item.username)

        return " ".join(usernames)

    def format_chips(self, value: list["User"] | list[str] | None) -> list["User"]:
        if not value:
            return None

        chips = []
        for item in value:
            if isinstance(item, str):
                chips.append(UserNotFound(item))
            else:
                chips.append(item)

        return chips or []

    def get_context(
        self, name: str, value: list["User"] | list[str] | None, attrs: dict
    ) -> dict:
        source = attrs.pop("source", None)

        context = super().get_context(name, value, attrs)

        context["widget"].update(
            {
                "source_text": source == "text",
                "source_chip": source == "chip",
                "chips": self.format_chips(value),
            }
        )

        if source == "text":
            context["widget"]["chips"] = None
        elif source == "chip":
            context["widget"]["value"] = None

        return context

    def value_from_datadict(self, data, files, name) -> list[str] | None:
        if text_data := data.get(f"{name}_text"):
            return self.list_value_from_datadict(text_data.split())

        if list_data := data.getlist(f"{name}_chip"):
            return self.list_value_from_datadict(list_data)

        return None

    def list_value_from_datadict(self, data: list[str]) -> list[str]:
        list_value: list[str] = []
        for value in data:
            value = value.strip()
            if value and value not in list_value:
                list_value.append(value)
        return list_value


class UserMultipleChoiceField(forms.Field):
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
        self.max_choices = max_choices
        self.queryset = queryset or get_user_model().objects

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

        if len(users_dict) != len(slugs):
            invalid_choices = []
            for slug, username in slugs.items():
                if slug not in users_dict:
                    invalid_choices.append(username)

            raise forms.ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": ", ".join(invalid_choices)},
            )

        python_value = []
        for slug, username in slugs.items():
            if slug in users_dict:
                python_value.append(users_dict[slug])
            else:
                # Return "blank" user item to appear in the UI
                python_value.append(UserNotFound(username))

        return python_value

    def widget_attrs(self, widget: forms.Widget) -> dict:
        return {"maxchoices": self.max_choices}

    def get_bound_field(self, form, field_name):
        return UserMultipleChoiceBoundField(form, self, field_name)


class UserMultipleChoiceBoundField(forms.BoundField):
    def value(self):
        if hasattr(self.form, "cleaned_data") and self.name in self.form.cleaned_data:
            return self.form.cleaned_data[self.name]

        return super().value()

    def max_choices(self) -> int:
        return self.field.max_choices

    def build_widget_attrs(
        self, attrs: dict, widget: forms.Widget | None = None
    ) -> dict:
        attrs = super().build_widget_attrs(attrs, widget)

        if self.form.is_bound:
            if self.form.data.get(f"{self.html_name}_text"):
                attrs["source"] = "text"
            elif self.form.data.getlist(f"{self.html_name}_chip"):
                attrs["source"] = "chip"

        return attrs
