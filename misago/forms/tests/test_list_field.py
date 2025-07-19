import pytest
from django.forms import IntegerField, ValidationError
from django.http import QueryDict

from ..fields import ListField


def test_list_field_clean_returns_empty_values():
    field = ListField(strip=False)
    assert field.clean(["A", " B ", "", "A", "  "]) == ["A", " B ", "", "A", "  "]


def test_list_field_clean_returns_value_with_whitespaces_stripped():
    field = ListField()
    assert field.clean(["A", " B ", "", "A", "  "]) == ["A", "B", "A"]


def test_list_field_clean_lowercase_returns_value_lowercased():
    field = ListField(lowercase=True)
    assert field.clean(["A", " B ", "", "A", "  "]) == ["a", "b", "a"]


def test_list_field_clean_uppercase_returns_value_uppercased():
    field = ListField(uppercase=True)
    assert field.clean(["a", " b ", "", "a", "  "]) == ["A", "B", "A"]


def test_list_field_clean_unique_returns_unique_value():
    field = ListField(unique=True)
    assert field.clean(["A", " B ", "", " A", "a"]) == ["A", "B", "a"]


def test_list_field_clean_unique_lowercase_returns_unique_lowercase_value():
    field = ListField(unique=True, lowercase=True)
    assert field.clean(["A", " B ", "", " A", "a"]) == ["a", "b"]


def test_list_field_clean_unique_uppercase_returns_unique_uppercase_value():
    field = ListField(unique=True, uppercase=True)
    assert field.clean(["a", " b ", "", " A", "a"]) == ["A", "B"]


def test_list_field_clean_unique_caseinsensitive_returns_caseinsensitive_value():
    field = ListField(unique=True, case_insensitive=True)
    assert field.clean(["a", " B ", "", " A", "a"]) == ["a", "B"]


def test_list_field_raises_error_if_lowercase_is_set_with_uppercase():
    with pytest.raises(ValueError) as exc_info:
        ListField(lowercase=True, uppercase=True)

    assert str(exc_info.value) == (
        "'lowercase' and 'uppercase' options cannot both be enabled."
    )


def test_list_field_raises_error_if_case_insensitive_is_set_without_unique():
    with pytest.raises(ValueError) as exc_info:
        ListField(case_insensitive=True)

    assert str(exc_info.value) == (
        "'case_insensitive' requires 'unique' option to be enabled."
    )


def test_list_field_raises_error_if_case_insensitive_is_set_with_lowercase():
    with pytest.raises(ValueError) as exc_info:
        ListField(case_insensitive=True, lowercase=True)

    assert str(exc_info.value) == (
        "'case_insensitive' and 'lowercase' options cannot both be enabled."
    )


def test_list_field_raises_error_if_case_insensitive_is_set_with_uppercase():
    with pytest.raises(ValueError) as exc_info:
        ListField(case_insensitive=True, uppercase=True)

    assert str(exc_info.value) == (
        "'case_insensitive' and 'uppercase' options cannot both be enabled."
    )


def test_list_field_clean_uses_field_arg_for_item_cleaning():
    field = ListField(field=IntegerField())
    assert field.clean(["1", "2", "3", "5"]) == [1, 2, 3, 5]


def test_list_field_clean_uses_field_arg_for_item_validation():
    field = ListField(field=IntegerField(max_value=3))

    with pytest.raises(ValidationError) as exc_info:
        field.clean(["1", "2", "3", "5"])

    assert exc_info.value.messages == ["Ensure this value is less than or equal to 3."]
