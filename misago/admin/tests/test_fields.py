from django import forms

from ...permissions.enums import PermissionValue
from ..forms import ColorField, YesNoField, YesNoNeverField


class ColorForm(forms.Form):
    test_field = ColorField(label="Hello!")


def test_color_field_returns_str_with_color_hex():
    form = ColorForm({"test_field": "#e9e9e9"})
    form.full_clean()
    assert form.cleaned_data["test_field"] == "#e9e9e9"


def test_color_field_rejects_short_color():
    form = ColorForm({"test_field": "#eee"})
    form.full_clean()
    assert "test_field" not in form.cleaned_data


def test_color_field_rejects_invalid_color():
    form = ColorForm({"test_field": "#ggg"})
    form.full_clean()
    assert "test_field" not in form.cleaned_data


def test_color_field_returns_none_for_empty_value():
    form = ColorForm({"test_field": ""})
    form.full_clean()
    assert "test_field" not in form.cleaned_data


class YesNoForm(forms.Form):
    test_field = YesNoField(label="Hello!")


def test_yes_no_field_returns_int_true_for_valid_true_input():
    for value in ("1", "True", "true", 1, True):
        form = YesNoForm({"test_field": value})
        form.full_clean()
        assert form.cleaned_data["test_field"] == 1


def test_yes_no_field_returns_int_false_for_false_input():
    for value in ("0", "False", "false", False, 0, None, ""):
        form = YesNoForm({"test_field": value})
        form.full_clean()
        assert form.cleaned_data["test_field"] == 0


def test_yes_no_field_returns_int_false_for_invalid_input():
    form = YesNoForm({"test_field": "invalid"})
    form.full_clean()
    assert form.cleaned_data["test_field"] == 0


class YesNoNeverForm(forms.Form):
    test_field = YesNoNeverField(label="Hello!")


def test_yes_no_never_field_returns_yes_value():
    form = YesNoNeverForm({"test_field": str(PermissionValue.YES.value)})
    form.full_clean()
    assert form.cleaned_data["test_field"] == PermissionValue.YES


def test_yes_no_never_field_returns_no_value():
    form = YesNoNeverForm({"test_field": str(PermissionValue.NO.value)})
    form.full_clean()
    assert form.cleaned_data["test_field"] == PermissionValue.NO


def test_yes_no_never_field_returns_never_value():
    form = YesNoNeverForm({"test_field": str(PermissionValue.NEVER.value)})
    form.full_clean()
    assert form.cleaned_data["test_field"] == PermissionValue.NEVER
