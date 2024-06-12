from django import forms, template
from django.forms.boundfield import BoundField


register = template.Library()


TEXT_WIDGETS = (
    forms.TextInput,
    forms.EmailInput,
    forms.PasswordInput,
    forms.URLInput,
)


@register.filter
def profilefieldwidget(field: BoundField) -> dict:
    if isinstance(field.field.widget, TEXT_WIDGETS):
        return get_textinput_data(field)

    if isinstance(field.field.widget, forms.Textarea):
        return get_textarea_data(field)

    if isinstance(field.field.widget, forms.RadioSelect):
        return get_choice_data(field)

    return {}


def get_textinput_data(field: BoundField) -> dict:
    data = {
        "input": "text",
        "type": "text",
    }

    if isinstance(field.field.widget, forms.EmailInput):
        data["type"] = "email"
    elif isinstance(field.field.widget, forms.PasswordInput):
        data["type"] = "password"
    elif isinstance(field.field.widget, forms.URLInput):
        data["type"] = "url"

    return data


def get_textarea_data(field: BoundField) -> dict:
    return {
        "input": "textarea",
        "rows": field.field.widget.attrs.get("rows"),
        "cols": field.field.widget.attrs.get("cols"),
    }


def get_choice_data(field: BoundField) -> dict:
    return {
        "input": "radiochoice",
        "rows": field.field.widget.attrs.get("rows"),
        "cols": field.field.widget.attrs.get("cols"),
    }
