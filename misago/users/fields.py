from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from ..forms.widgets import ListInput

if TYPE_CHECKING:
    from ..users.models import User


class UserMultipleChoiceWidget(forms.MultiWidget):
    template_name = "misago/widgets/user_multiple_choice.html"
    subfields = ("default", "noscript")

    def __init__(self, attrs: dict | None = None):
        super().__init__(
            widgets={
                "": ListInput,
                "noscript": forms.TextInput,
            },
            attrs=attrs,
        )

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        for i, subwidget in enumerate(context["widget"]["subwidgets"]):
            subwidget_name = self.subfields[i]
            context["widget"][subwidget_name] = subwidget
        
        del context["widget"]["subwidgets"]

        return context

    def decompress(self, value):
        if value and isinstance(value[0], get_user_model()):
            return [value, value]
        return [None, None]


class UserMultipleChoiceField(forms.MultiValueField):
    widget = UserMultipleChoiceWidget

    def __init__(self, *, queryset: QuerySet | None = None, max_choices: int = 5, **kwargs):
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

    def compress(self, data_list: tuple[list[str], str]) -> list["User"]:
        if data_list:
            value, value_noscript = data_list
            return value or value_noscript
        return None


class UserMultipleChoiceSubField(forms.Field):
    def __init__(self, queryset: QuerySet | None = None, max_choices: int = 5, **kwargs):
        self.max_choices = max_choices
        self.queryset = queryset

        super().__init__(**kwargs)

    def get_users(self, queryset: QuerySet, usernames: list[str]) -> list["User"]:
        return queryset.filter(slug__in=set(username.lower() for username in usernames))


class UserMultipleChoiceJavaScriptSubField(UserMultipleChoiceSubField):
    widget = ListInput

    def clean(self, value: list[str]) -> list["User"]:
        value = self.to_python(value)[:self.max_choices]

        if value:
            value = list(self.get_users(self.queryset, value))
        else:
            value = []

        self.validate(value)
        self.run_validators(value)
        return value


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

    def clean(self, value: list[str]) -> list["User"]:
        value = self.to_python(value)

        if len(value) > self.max_choices:
            raise forms.ValidationError("TODO")

        if value:
            value = list(self.get_users(self.queryset, value))
        else:
            value = []

        self.validate(value)
        self.run_validators(value)
        return value

