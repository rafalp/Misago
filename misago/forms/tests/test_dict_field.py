import pytest
from django import forms
from django.core.exceptions import ValidationError

from ..fields import DictField


def test_dict_field_clean_raises_validation_error_if_type_is_wrong():
    field = DictField()

    with pytest.raises(ValidationError) as exc_info:
        field.clean("invalid")

    assert exc_info.value.message == "Enter a dict."
    assert exc_info.value.code == "invalid_dict"


def test_dict_field_clean_strips_keys_whitespace():
    field = DictField()
    assert field.clean({"  a  ": "1"}) == {"a": "1"}


def test_dict_field_clean_strips_values_whitespace():
    field = DictField()
    assert field.clean({"a": "  1  "}) == {"a": "1"}


def test_dict_field_clean_doesnt_strip_values_whitespace():
    field = DictField(strip=False)
    assert field.clean({"a": "  1  "}) == {"a": "  1  "}


def test_dict_field_clean_coerces_keys():
    field = DictField(coerce=int)
    assert field.clean({"  1  ": "1", "2": "2"}) == {1: "1", 2: "2"}


def test_dict_field_clean_raises_validation_error_if_key_cant_be_coerced():
    field = DictField(coerce=int)

    with pytest.raises(ValidationError) as exc_info:
        field.clean({"invalid": "1"})

    assert exc_info.value.message == (
        "Select a valid choice. %(value)s is not one of the available choices."
    )
    assert exc_info.value.code == "invalid_choice"
    assert exc_info.value.params == {"value": "invalid"}


def test_dict_field_clean_validates_keys_against_choices():
    field = DictField(choices=["a", "b", "c"])
    assert field.clean({"a": "1", "c": "2"}) == {"a": "1", "c": "2"}


def test_dict_field_clean_raises_validation_error_if_key_is_not_in_choices():
    field = DictField(choices=["a", "b", "c"])

    with pytest.raises(ValidationError) as exc_info:
        field.clean({"a": "1", "d": "2"})

    assert exc_info.value.message == (
        "Select a valid choice. %(value)s is not one of the available choices."
    )
    assert exc_info.value.code == "invalid_choice"
    assert exc_info.value.params == {"value": "d"}


def test_dict_field_clean_validates_keys_against_choices_after_coerce():
    field = DictField(coerce=int, choices=[1, 2, 3])
    assert field.clean({"1": "1", "2": "2"}) == {1: "1", 2: "2"}


def test_dict_field_clean_raises_required_error_if_field_is_required():
    field = DictField(required=True)

    with pytest.raises(ValidationError) as exc_info:
        field.clean({})

    assert exc_info.value.message == "This field is required."
    assert exc_info.value.code == "required"


def test_dict_field_clean_allows_empty_value_if_field_is_optional():
    field = DictField(required=False)
    assert field.clean({}) == {}


def test_dict_field_clean_uses_key_field_to_clean_keys():
    field = DictField(key_field=forms.IntegerField())
    assert field.clean({"1": "1", "2": "2"}) == {1: "1", 2: "2"}


def test_dict_field_clean_uses_key_field_validation_errors():
    field = DictField(key_field=forms.IntegerField(min_value=2))

    with pytest.raises(ValidationError) as exc_info:
        field.clean({"1": "1", "2": "2"})

    assert exc_info.value.messages == [
        '"1": Ensure this value is greater than or equal to 2.'
    ]


def test_dict_field_clean_uses_value_field_to_clean_values():
    field = DictField(value_field=forms.IntegerField())
    assert field.clean({"1": "1", "2": "2"}) == {"1": 1, "2": 2}


def test_dict_field_clean_uses_value_field_validation_errors():
    field = DictField(value_field=forms.IntegerField(min_value=2))

    with pytest.raises(ValidationError) as exc_info:
        field.clean({"1": "1", "2": "2"})

    assert exc_info.value.messages == [
        '"1": Ensure this value is greater than or equal to 2.'
    ]


def test_dict_field_has_changed_returns_false_if_field_is_disabled():
    field = DictField(disabled=True)
    assert not field.has_changed({}, {1: 2})


def test_dict_field_has_changed_returns_false_if_field_has_no_values():
    field = DictField()
    assert not field.has_changed(None, None)


def test_dict_field_has_changed_returns_false_if_field_is_empty():
    field = DictField()
    assert not field.has_changed(None, {})


def test_dict_field_has_changed_returns_true_if_values_differ():
    field = DictField()
    assert field.has_changed({}, {1: 2})
