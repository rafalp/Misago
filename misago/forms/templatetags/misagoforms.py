from django import template
from django.forms.boundfield import BoundField, BoundWidget


register = template.Library()


@register.filter
def checkedhtml(bound_widget: BoundWidget) -> str:
    return " checked" if bound_widget.data.get("selected") else ""


@register.filter
def selectedhtml(bound_widget: BoundWidget) -> str:
    return " selected" if bound_widget.data.get("selected") else ""


@register.filter
def requiredhtml(field_or_widget: BoundField | BoundWidget) -> str:
    if isinstance(field_or_widget, BoundField) and field_or_widget.field.required:
        return " required"
    if isinstance(field_or_widget, BoundWidget) and field_or_widget.data["attrs"].get(
        "required"
    ):
        return " required"

    return ""
