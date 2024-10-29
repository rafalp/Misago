import pytest
from django import forms

from ..formset import Formset


class UserForm(forms.Form):
    name = forms.CharField(max_length=10)

    def clean(self):
        data = super().clean()
        if data.get("name") == "Bob":
            raise forms.ValidationError("Name can't be Bob!")
        return data


class AgeForm(forms.Form):
    age = forms.IntegerField(min_value=18)

    def clean(self):
        data = super().clean()
        if data.get("age") == 42:
            raise forms.ValidationError("Age can't be 42!")
        return data


def test_formset_add_form_adds_form_with_prefix():
    form = UserForm(prefix="user")

    formset = Formset()
    formset.add_form(form)

    assert formset["user"] is form


def test_formset_add_form_raises_value_error_if_form_is_missing_prefix():
    with pytest.raises(ValueError) as exc_info:
        formset = Formset()
        formset.add_form(UserForm())

    assert "must have a prefix" in str(exc_info.value)


def test_formset_add_form_raises_value_error_if_form_with_prefix_already_exists():
    with pytest.raises(ValueError) as exc_info:
        formset = Formset()
        formset.add_form(UserForm(prefix="user"))
        formset.add_form(AgeForm(prefix="user"))

    assert "is already a part of this formset" in str(exc_info.value)


def test_formset_add_form_inserts_form_after_other():
    formset = Formset()
    formset.add_form(UserForm(prefix="user"))
    formset.add_form(AgeForm(prefix="age"), after="user")

    prefixes = [form.prefix for form in formset.get_forms()]
    assert prefixes == ["user", "age"]


def test_formset_add_form_inserts_form_before_other():
    formset = Formset()
    formset.add_form(UserForm(prefix="user"))
    formset.add_form(AgeForm(prefix="age"), before="user")

    prefixes = [form.prefix for form in formset.get_forms()]
    assert prefixes == ["age", "user"]


def test_formset_add_form_raises_value_error_if_both_after_and_before_are_used():
    with pytest.raises(ValueError) as exc_info:
        formset = Formset()
        formset.add_form(UserForm(prefix="user"))
        formset.add_form(AgeForm(prefix="age"), after="user", before="user")

    assert "'after' and 'before' arguments can't be combined." in str(exc_info.value)


def test_formset_add_form_raises_value_error_if_after_value_is_invalid():
    with pytest.raises(ValueError) as exc_info:
        formset = Formset()
        formset.add_form(UserForm(prefix="user"))
        formset.add_form(AgeForm(prefix="age"), after="invalid")

    assert "Form with prefix 'invalid' doesn't exist in this formset." in str(
        exc_info.value
    )


def test_formset_add_form_raises_value_error_if_before_value_is_invalid():
    with pytest.raises(ValueError) as exc_info:
        formset = Formset()
        formset.add_form(UserForm(prefix="user"))
        formset.add_form(AgeForm(prefix="age"), after="invalid")

    assert "Form with prefix 'invalid' doesn't exist in this formset." in str(
        exc_info.value
    )


def test_formset_in_operation_returns_true_if_form_is_already_in_formset():
    user_form = UserForm(prefix="user")
    age_form = AgeForm(prefix="age")

    formset = Formset()
    formset.add_form(user_form)

    assert user_form in formset
    assert age_form not in formset


def test_formset_in_operation_returns_true_if_form_prefix_is_already_in_formset():
    formset = Formset()
    formset.add_form(UserForm(prefix="user"))

    assert "user" in formset
    assert "age" not in formset


def test_formset_is_bound_is_true_if_all_forms_are_bound():
    formset = Formset()
    formset.add_form(UserForm({"user-name": "Alice"}, prefix="user"))
    formset.add_form(AgeForm({"age-age": 12}, prefix="age"))
    assert formset.is_bound


def test_formset_is_bound_is_false_if_some_forms_are_bound():
    formset = Formset()
    formset.add_form(UserForm({"user-name": "Alice"}, prefix="user"))
    formset.add_form(AgeForm(prefix="age"))
    assert not formset.is_bound


def test_formset_is_bound_is_false_if_no_forms_are_bound():
    formset = Formset()
    formset.add_form(UserForm(prefix="user"))
    formset.add_form(AgeForm(prefix="age"))
    assert not formset.is_bound


def test_formset_is_valid_is_true_if_all_forms_are_valid():
    formset = Formset()
    formset.add_form(UserForm({"user-name": "Alice"}, prefix="user"))
    formset.add_form(AgeForm({"age-age": 22}, prefix="age"))
    assert formset.is_valid()


def test_formset_is_valid_is_false_if_some_forms_are_valid():
    formset = Formset()
    formset.add_form(UserForm({"user-name": "Alice"}, prefix="user"))
    formset.add_form(AgeForm({"age-age": 12}, prefix="age"))
    assert not formset.is_valid()


def test_formset_is_valid_is_false_if_no_forms_are_valid():
    formset = Formset()
    formset.add_form(UserForm({"user-name": "Alice" * 10}, prefix="user"))
    formset.add_form(AgeForm({"age-age": 12}, prefix="age"))
    assert not formset.is_valid()


def test_formset_non_field_errors_returns_empty_if_forms_have_no_non_field_errors():
    formset = Formset()
    formset.add_form(UserForm({"user-name": "Alice"}, prefix="user"))
    formset.add_form(AgeForm({"age-age": 22}, prefix="age"))

    assert formset.is_valid()
    assert formset.non_field_errors() == []


def test_formset_non_field_errors_returns_list_if_any_form_has_no_non_field_errors():
    formset = Formset()
    formset.add_form(UserForm({"user-name": "Bob"}, prefix="user"))
    formset.add_form(AgeForm({"age-age": 22}, prefix="age"))

    assert not formset.is_valid()
    assert len(formset.non_field_errors()) == 1


def test_formset_non_field_errors_returns_list_of_all_non_field_errors():
    formset = Formset()
    formset.add_form(UserForm({"user-name": "Bob"}, prefix="user"))
    formset.add_form(AgeForm({"age-age": 42}, prefix="age"))

    assert not formset.is_valid()
    assert len(formset.non_field_errors()) == 2
