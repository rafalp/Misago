from typing import Iterable

from django import forms
from django.utils.crypto import get_random_string

from ..forms.fields import DictField, ListField
from ..forms.widgets import DictInput, ListInput, ListTextarea
from .choices import PollChoices


class PollChoicesValue:
    choices: PollChoices
    edit: dict[str, str]
    delete: set[str]
    new: list[str]

    __slots__ = ("choices", "edit", "delete", "new")

    def __init__(
        self,
        choices: PollChoices | None = None,
        edit: dict[str, str] | None = None,
        delete: Iterable[str] | None = None,
        new: list[str] | None = None,
    ):
        self.choices = choices or []
        self.edit = edit or {}
        self.new = new or []
        self.delete = set(delete) if delete else set()

    def __bool__(self):
        return bool(self.json())

    def json(self):
        choices: PollChoices = []

        for choice in self.choices:
            choice_id = choice["id"]
            if choice_id in self.delete:
                continue

            choice = choice.copy()
            if choice_id in self.edit:
                choice["name"] = self.edit[choice_id]

            choices.append(choice)

        for name in self.new:
            choices.append(
                {
                    "id": get_random_string(12),
                    "name": name,
                    "votes": 0,
                }
            )

        return choices


CHOICES_FIELDS = ("new", "new_noscript", "edit", "delete")


class PollChoicesWidget(forms.MultiWidget):
    template_name = "misago/widgets/poll_choices.html"
    subwidgets_names = CHOICES_FIELDS

    def __init__(self):
        super().__init__(self.get_widgets())

    def get_widgets(self) -> tuple[forms.Widget, ...]:
        return {
            "new": ListInput(),
            "new_noscript": ListTextarea(),
        }

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        del context["widget"]["value"]
        del context["widget"]["subwidgets"]

        if not isinstance(value, (list, tuple)):
            value = self.decompress(value)

        final_attrs = context["widget"]["attrs"]
        id_ = final_attrs.get("id")

        for i, (widget_name, widget) in enumerate(
            zip(self.widgets_names, self.widgets)
        ):
            widget_name = name + widget_name
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                widget_attrs = final_attrs.copy()
                widget_attrs["id"] = "%s_%s" % (id_, i)
            else:
                widget_attrs = final_attrs
            context["widget"][self.subwidgets_names[i]] = widget.get_context(
                widget_name, widget_value, widget_attrs
            )["widget"]

        return context

    def decompress(self, value: PollChoicesValue | None):
        if value:
            return [value.new, value.new]

        return [[], []]


class EditPollChoicesWidget(PollChoicesWidget):
    def get_widgets(self) -> tuple[forms.Widget, ...]:
        return {
            "new": ListInput(),
            "new_noscript": ListTextarea(),
            "edit": DictInput(),
            "delete": ListInput(),
        }

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        if not isinstance(value, (list, tuple)):
            value = self.decompress(value)

        edit_attrs = context["widget"]["edit"]
        delete_attrs = context["widget"]["delete"]

        _, _, edit, delete = value

        choices = []
        for choice_id, choice_name in edit.items():
            choices.append(
                {
                    "id": choice_id,
                    "edit_name": f'{edit_attrs["name"]}[{choice_id}]',
                    "delete_name": f'{delete_attrs["name"]}',
                    "value": choice_name,
                    "checked": choice_id in delete,
                }
            )

        context["widget"]["choices"] = choices
        return context

    def decompress(self, value: PollChoicesValue | None):
        if value:
            edit_names = {choice["id"]: choice["name"] for choice in value.choices}
            return [value.new, value.new, edit_names, value.delete]

        return [[], [], {}, set()]


class PollChoicesField(forms.MultiValueField):
    widget = PollChoicesWidget
    subfields = CHOICES_FIELDS

    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop("max_choices", 5)

        super().__init__(
            *args,
            **kwargs,
            require_all_fields=False,
            fields=self.get_fields(),
        )

    def get_fields(self) -> tuple[forms.Field, ...]:
        return (
            ListField(required=False, widget=ListInput),
            ListField(required=False),
        )

    def widget_attrs(self, widget: forms.Widget) -> dict:
        return {"max_choices": self.max_choices}

    def compress(self, data):
        if not data:
            return PollChoicesValue()

        data_dict = {self.subfields[i]: v for i, v in enumerate(data)}
        return PollChoicesValue(
            new=data_dict["new"] or data_dict["new_noscript"],
        )

    def get_bound_field(self, form, field_name):
        return PollChoicesBoundField(form, self, field_name)


class EditPollChoicesField(PollChoicesField):
    widget = EditPollChoicesWidget

    def get_fields(self) -> tuple[forms.Field, ...]:
        return (
            ListField(required=False),
            ListField(required=False),
            DictField(required=False),
            ListField(required=False),
        )

    def bound_data(self, data: list | None, initial: PollChoicesValue | None):
        if self.disabled:
            if initial:
                edit = {choice["id"]: choice["name"] for choice in initial.choices}
                return [initial.new, initial.new, edit, initial.delete]
            return [[], [], {}, set()]

        if not initial:
            return data

        new, new_noscript, edit, delete = data

        final_edit = {choice["id"]: choice["name"] for choice in initial.choices}
        for choice_id, choice_name in edit.items():
            if choice_id in final_edit and choice_name:
                final_edit[choice_id] = choice_name

        return [new, new_noscript, final_edit, delete]

    def compress(self, data):
        choices = self.initial.choices if self.initial else None

        if not data:
            return PollChoicesValue(choices=choices)

        data_dict = {self.subfields[i]: v for i, v in enumerate(data)}

        return PollChoicesValue(
            choices=choices,
            new=data_dict["new"] or data_dict["new_noscript"],
            edit=data_dict["edit"],
            delete=data_dict["delete"],
        )


class PollChoicesBoundField(forms.BoundField):
    @property
    def max_choices(self) -> int:
        return self.field.max_choices
