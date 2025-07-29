from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

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
            return value or value_noscript
        return None

    def get_bound_field(self, form, field_name):
        return UserMultipleChoiceBoundField(form, self, field_name)


class UserMultipleChoiceSubField(forms.Field):
    def __init__(
        self, queryset: QuerySet | None = None, max_choices: int = 5, **kwargs
    ):
        self.max_choices = max_choices
        self.queryset = queryset

        super().__init__(**kwargs)

    def get_users(self, queryset: QuerySet, slugs: list[str]) -> list["User"]:
        return list(queryset.filter(slug__in=set(slugs)))


class UserMultipleChoiceJavaScriptSubField(UserMultipleChoiceSubField):
    widget = ListInput

    def to_python(self, value) -> list[str]:
        if not value:
            return []

        return [slugify(item) for item in value]

    def clean(self, value: list[str]) -> list["User"]:
        value = self.to_python(value)[: self.max_choices]

        if value:
            usernames = value
            value = self.get_users(self.queryset, value)
            self.set_users_cache(usernames, value)
        else:
            value = []

        self.validate(value)
        self.run_validators(value)
        return value

    def set_users_cache(self, usernames: list[str], users: list[str]):
        users_map = {user.slug: user for user in users}

        ordered_users = []
        for username in usernames:
            slug = username.lower()
            if slug in users_map:
                ordered_users.append(users_map.pop(slug))
        self.users_cache = ordered_users + list(users_map.values())


class UserMultipleChoiceNoScriptSubField(UserMultipleChoiceSubField):
    def to_python(self, value) -> list[str]:
        if not value:
            return []

        final_value = []
        for item in value.split():
            if "," in item:
                final_value += [slugify(i.strip()) for i in item.split(",")]
            else:
                final_value.append(slugify(item))
        return [item for item in final_value if item]

    def clean(self, value: list[str]) -> list["User"]:
        value = self.to_python(value)

        if len(value) > self.max_choices:
            raise forms.ValidationError("TODO")

        if value:
            value = self.get_users(self.queryset, value)
        else:
            value = []

        self.validate(value)
        self.run_validators(value)
        return value


class UserMultipleChoiceBoundField(forms.BoundField):
    @property
    def max_choices(self) -> int:
        return self.field.max_choices

    def build_widget_attrs(self, attrs: dict, widget: forms.Widget | None = None):
        attrs = super().build_widget_attrs(attrs, widget)
        attrs["max_choices"] = self.max_choices
        attrs["choices"] = self.field.get_users_cache() or self.initial or []
        return attrs
