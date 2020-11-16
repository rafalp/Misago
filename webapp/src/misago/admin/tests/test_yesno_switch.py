from django import forms

from ..forms import YesNoSwitch


class YesNoForm(forms.Form):
    test_field = YesNoSwitch(label="Hello!")


def test_input_returns_int_true_for_valid_true_input():
    for value in ("1", "True", "true", 1, True):
        form = YesNoForm({"test_field": value})
        form.full_clean()
        assert form.cleaned_data["test_field"] == 1


def test_input_returns_int_false_for_false_input():
    for value in ("0", "False", "false", False, 0, None, ""):
        form = YesNoForm({"test_field": value})
        form.full_clean()
        assert form.cleaned_data["test_field"] == 0


def test_input_returns_int_false_for_invalid_input():
    form = YesNoForm({"test_field": "invalid"})
    form.full_clean()
    assert form.cleaned_data["test_field"] == 0
