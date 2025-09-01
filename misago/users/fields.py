from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.translation import npgettext_lazy, pgettext_lazy

from ..forms.widgets import ListInput
from ..core.utils import slugify

if TYPE_CHECKING:
    from ..users.models import User


class UserMultipleChoiceWidget(forms.MultiWidget):
    template_name = "misago/widgets/user_multiple_choice.html"
    subfields = ("default", "noscript")

    def __init__(self, attrs: dict | None = None):
        super().__init__(
            {
                "": ListInput,
                "noscript": forms.TextInput,
            },
            attrs=attrs,
        )

    def get_context(self, name, value, attrs):
        max_choices = attrs.pop("max_choices", None)
        choices = attrs.pop("choices", None)

        # Decompress value manually because MultiWidget never calls decompress for lists
        value = self.decompress_unknown_value(value)

        context = super().get_context(name, value, attrs)
        for i, subwidget in enumerate(context["widget"]["subwidgets"]):
            subwidget_name = self.subfields[i]
            context["widget"][subwidget_name] = subwidget

        del context["widget"]["subwidgets"]

        context["widget"]["max_choices"] = max_choices
        context["widget"]["choices"] = choices

        return context

    def decompress_unknown_value(self, value) -> list:
        if not value or not isinstance(value, (list, tuple)):
            # unknown value, discard
            return [None, None]

        if isinstance(value[0], get_user_model()):
            # Iterable[User], initial value
            return [value, " ".join(user.username for user in value)]

        return value


class UserMultipleChoiceField(forms.MultiValueField):
    widget = UserMultipleChoiceWidget

    def __init__(
        self, *, queryset: QuerySet | None = None, max_choices: int = 5, **kwargs
    ):
        super().__init__(
            fields=(
                UserMultipleChoiceJavaScriptSubField(required=False),
                UserMultipleChoiceNoScriptSubField(required=False),
            ),
            require_all_fields=False,
            **kwargs,
        )

        self.max_choices = max_choices
        self.queryset = queryset or get_user_model().objects

    def _get_max_choices(self) -> int:
        return self._max_choices

    def _set_max_choices(self, max_choices: int):
        self._max_choices = max_choices
        for field in self.fields:
            field.max_choices = max_choices

    max_choices: int = property(_get_max_choices, _set_max_choices)

    def _get_queryset(self) -> QuerySet:
        return self._queryset

    def _set_queryset(self, queryset: QuerySet):
        self._queryset = queryset
        for field in self.fields:
            field.queryset = queryset

    queryset: QuerySet = property(_get_queryset, _set_queryset)

    def get_users_cache(self) -> list["User"] | None:
        for field in self.fields:
            if users_cache := getattr(field, "users_cache", None):
                return users_cache
        return None

    def compress(self, data_list: tuple[list[str], str]) -> list["User"]:
        if data_list:
            value, value_noscript = data_list
            # Prioritize the noscript value because its only present with the JS disabled
            return value_noscript or value
        return None

    def get_bound_field(self, form, field_name):
        return UserMultipleChoiceBoundField(form, self, field_name)


class UserMultipleChoiceSubField(forms.Field):
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

    def __init__(
        self, queryset: QuerySet | None = None, max_choices: int = 5, **kwargs
    ):
        self.max_choices = max_choices
        self.queryset = queryset

        super().__init__(**kwargs)

    def get_users(self, queryset: QuerySet, usernames: list[str]) -> list["User"]:
        raise NotImplementedError()

    def validate_max_choices(self, value_length: int):
        if value_length > self.max_choices:
            raise forms.ValidationError(
                self.error_messages["max_choices"],
                code="max_choices",
                params={"max": self.max_choices},
            )


class UserNotFound:
    id = None
    username: str

    __slots__ = ("username",)

    def __init__(self, username: str):
        self.username = username


class UserMultipleChoiceJavaScriptSubField(UserMultipleChoiceSubField):
    widget = ListInput

    def to_python(self, value) -> list[str]:
        return value or []

    def clean(self, usernames: list[str]) -> list["User"]:
        usernames = self.to_python(usernames)

        if usernames:
            value = self.get_users(self.queryset, usernames)
            self.users_cache = value
            self.validate_max_choices(len(value))
        else:
            value = []

        self.validate(value)
        self.run_validators(value)
        return value

    def get_users(self, queryset: QuerySet, usernames: list[str]) -> list["User"]:
        slugs: dict[str, str] = {}
        for username in usernames:
            slug = slugify(username)
            slugs[slug] = username

        users = list(queryset.filter(slug__in=slugs)[: self.max_choices + 16])
        users_dict = {user.slug: user for user in users}

        ordered_users = []
        for slug, username in slugs.items():
            if slug in users_dict:
                ordered_users.append(users_dict[slug])
            else:
                # Return "blank" user item to appear in the UI
                ordered_users.append(UserNotFound(username))

        return ordered_users

    def validate(self, value: list["User"]):
        invalid_choices: list[str] = [user.username for user in value if not user.id]
        if invalid_choices:
            raise forms.ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": ", ".join(invalid_choices)},
            )


class UserMultipleChoiceNoScriptSubField(UserMultipleChoiceSubField):
    def to_python(self, value) -> list[str]:
        if not value:
            return []

        final_value = []
        for item in value.split():
            if "," in item:
                final_value += [i.strip() for i in item.split(",")]
            else:
                final_value.append(item)
        return [item for item in final_value if item]

    def clean(self, usernames: list[str]) -> list["User"]:
        usernames = self.to_python(usernames)

        if usernames:
            self.validate_max_choices(len(usernames))
            value = self.get_users(self.queryset, usernames)
        else:
            value = []

        self.validate(value, usernames)
        self.run_validators(value)
        return value

    def get_users(self, queryset: QuerySet, usernames: list[str]) -> list["User"]:
        slugs: set[str] = set(slugify(username) for username in usernames)
        return list(queryset.filter(slug__in=slugs)[: self.max_choices + 1])

    def validate(self, value: list["User"], usernames: list[str]):
        slugs: set[str] = set(user.slug for user in value)
        invalid_choices: list[str] = []
        for username in usernames:
            username_slug = slugify(username)
            if username_slug not in slugs:
                invalid_choices.append(username)

        if invalid_choices:
            raise forms.ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": ", ".join(invalid_choices)},
            )


class UserMultipleChoiceBoundField(forms.BoundField):
    @property
    def max_choices(self) -> int:
        return self.field.max_choices

    def build_widget_attrs(self, attrs: dict, widget: forms.Widget | None = None):
        attrs = super().build_widget_attrs(attrs, widget)
        attrs["max_choices"] = self.max_choices
        attrs["choices"] = self.field.get_users_cache() or self.initial or []
        return attrs
