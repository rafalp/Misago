from unittest.mock import Mock

import pytest

from ..serializers import deserialize_value, serialize_value


def test_string_value_can_be_deserialized_and_serialized_back():
    assert serialize_value("string", deserialize_value("string", "test")) == "test"


def test_int_value_is_deserialized_to_string():
    assert deserialize_value("string", 123) == "123"


def test_empty_string_value_is_serialized_to_empty_string():
    assert serialize_value("string", None) == ""


def test_bool_false_value_can_be_deserialized_and_serialized_back():
    assert serialize_value("bool", deserialize_value("bool", False)) is False


def test_bool_true_value_can_be_deserialized_and_serialized_back():
    assert serialize_value("bool", deserialize_value("bool", True)) is True


def test_bool_none_value_can_be_deserialized_and_serialized_back_to_false():
    assert serialize_value("bool", deserialize_value("bool", None)) is False


def test_int_value_can_be_deserialized_and_serialized_back():
    assert serialize_value("int", deserialize_value("int", 123)) == 123


def test_empty_int_value_can_be_deserialized_and_serialized_back():
    assert serialize_value("int", deserialize_value("int", 0)) == 0


def test_none_int_value_is_deserialized_to_zero_string():
    assert deserialize_value("int", None) == "0"


def test_none_int_value_is_serialized_to_zero():
    assert serialize_value("int", None) == 0


def test_empty_int_value_is_serialized_to_zero():
    assert serialize_value("int", "") == 0


def test_list_value_can_be_deserialized_and_serialized_back():
    assert serialize_value("list", deserialize_value("list", ["a", "b"])) == ["a", "b"]


def test_single_item_list_value_can_be_deserialized_and_serialized_back():
    assert serialize_value("list", deserialize_value("list", ["a"])) == ["a"]


def test_empty_list_value_can_be_deserialized_and_serialized_back():
    assert serialize_value("list", deserialize_value("list", [])) == []


def test_none_list_value_can_be_deserialized_and_serialized_to_empty_list():
    assert serialize_value("list", deserialize_value("list", None)) == []


def test_empty_list_value_is_serialized_to_empty_list():
    assert serialize_value("list", "") == []


def test_none_list_value_is_serialized_to_empty_list():
    assert serialize_value("list", None) == []


def test_none_list_value_is_deserialized_to_empty_string():
    assert deserialize_value("list", None) == ""


def test_image_value_hydration_is_noop():
    image = Mock()
    assert serialize_value("image", image) is image


def test_image_value_dehydration_is_noop():
    image = Mock()
    assert deserialize_value("image", image) is image


def test_value_error_is_raised_on_unsupported_type_dehydration():
    with pytest.raises(ValueError):
        deserialize_value("unsupported", None)


def test_value_error_is_raised_on_unsupported_type_hydration():
    with pytest.raises(ValueError):
        serialize_value("unsupported", None)
