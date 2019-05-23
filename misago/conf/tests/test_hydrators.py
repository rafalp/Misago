from unittest.mock import Mock

import pytest

from ..hydrators import dehydrate_value, hydrate_value


def test_string_value_can_be_dehydrated_and_hydrated_back():
    assert hydrate_value("string", dehydrate_value("string", "test")) == "test"


def test_int_value_is_dehydrated_to_string():
    assert dehydrate_value("string", 123) == "123"


def test_empty_string_value_is_hydrated_to_empty_string():
    assert hydrate_value("string", None) == ""


def test_bool_false_value_can_be_dehydrated_and_hydrated_back():
    assert hydrate_value("bool", dehydrate_value("bool", False)) is False


def test_bool_true_value_can_be_dehydrated_and_hydrated_back():
    assert hydrate_value("bool", dehydrate_value("bool", True)) is True


def test_bool_none_value_can_be_dehydrated_and_hydrated_back_to_false():
    assert hydrate_value("bool", dehydrate_value("bool", None)) is False


def test_int_value_can_be_dehydrated_and_hydrated_back():
    assert hydrate_value("int", dehydrate_value("int", 123)) == 123


def test_empty_int_value_can_be_dehydrated_and_hydrated_back():
    assert hydrate_value("int", dehydrate_value("int", 0)) == 0


def test_none_int_value_is_dehydrated_to_zero_string():
    assert dehydrate_value("int", None) == "0"


def test_none_int_value_is_hydrated_to_zero():
    assert hydrate_value("int", None) == 0


def test_empty_int_value_is_hydrated_to_zero():
    assert hydrate_value("int", "") == 0


def test_list_value_can_be_dehydrated_and_hydrated_back():
    assert hydrate_value("list", dehydrate_value("list", ["a", "b"])) == ["a", "b"]


def test_single_item_list_value_can_be_dehydrated_and_hydrated_back():
    assert hydrate_value("list", dehydrate_value("list", ["a"])) == ["a"]


def test_empty_list_value_can_be_dehydrated_and_hydrated_back():
    assert hydrate_value("list", dehydrate_value("list", [])) == []


def test_none_list_value_can_be_dehydrated_and_hydrated_to_empty_list():
    assert hydrate_value("list", dehydrate_value("list", None)) == []


def test_empty_list_value_is_hydrated_to_empty_list():
    assert hydrate_value("list", "") == []


def test_none_list_value_is_hydrated_to_empty_list():
    assert hydrate_value("list", None) == []


def test_none_list_value_is_dehydrated_to_empty_string():
    assert dehydrate_value("list", None) == ""


def test_image_value_hydration_is_noop():
    image = Mock()
    assert hydrate_value("image", image) is image


def test_image_value_dehydration_is_noop():
    image = Mock()
    assert dehydrate_value("image", image) is image


def test_value_error_is_raised_on_unsupported_type_dehydration():
    with pytest.raises(ValueError):
        dehydrate_value("unsupported", None)


def test_value_error_is_raised_on_unsupported_type_hydration():
    with pytest.raises(ValueError):
        hydrate_value("unsupported", None)
