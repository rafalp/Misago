from django import forms

from ..forms import ColorField


class ColorForm(forms.Form):
    test_field = ColorField(label="Hello!")


def test_input_returns_str_with_color_hex():
    form = ColorForm({"test_field": "#e9e9e9"})
    form.full_clean()
    assert form.cleaned_data["test_field"] == "#e9e9e9"


def test_input_rejects_short_color():
    form = ColorForm({"test_field": "#eee"})
    form.full_clean()
    assert "test_field" not in form.cleaned_data


def test_input_rejects_invalid_color():
    form = ColorForm({"test_field": "#ggg"})
    form.full_clean()
    assert "test_field" not in form.cleaned_data


def test_input_returns_none_for_empty_value():
    form = ColorForm({"test_field": ""})
    form.full_clean()
    assert "test_field" not in form.cleaned_data
