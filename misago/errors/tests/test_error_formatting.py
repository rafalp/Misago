from pydantic.errors import NoneIsNotAllowedError, PydanticErrorMixin

from ..format import ROOT_LOCATION, get_error_dict


class BaseError(PydanticErrorMixin, Exception):
    base_name = "custom_error"


class SpecializedBaseError(BaseError):
    code = "specialized"
    msg_template = "specialized error"


def test_error_dict_is_created_for_bare_exception():
    error_dict = get_error_dict(Exception("error message"))
    assert error_dict == {
        "type": "error.exception",
        "msg": "error message",
        "loc": ROOT_LOCATION,
    }


def test_error_dict_is_created_for_value_error():
    error_dict = get_error_dict(ValueError("error message"))
    assert error_dict == {
        "type": "value_error.value",
        "msg": "error message",
        "loc": ROOT_LOCATION,
    }


def test_error_dict_is_created_for_type_error():
    error_dict = get_error_dict(TypeError("error message"))
    assert error_dict == {
        "type": "type_error.type",
        "msg": "error message",
        "loc": ROOT_LOCATION,
    }


def test_error_dict_is_created_for_assertion_error():
    error_dict = get_error_dict(AssertionError("error message"))
    assert error_dict == {
        "type": "assertion_error",
        "msg": "error message",
        "loc": ROOT_LOCATION,
    }


def test_error_dict_is_created_for_pydantic_error():
    error_dict = get_error_dict(NoneIsNotAllowedError())
    assert error_dict == {
        "type": "type_error.none.not_allowed",
        "msg": "none is not an allowed value",
        "loc": ROOT_LOCATION,
    }


def test_error_dict_is_created_for_custom_error():
    error_dict = get_error_dict(SpecializedBaseError())
    assert error_dict == {
        "type": "custom_error.specialized",
        "msg": "specialized error",
        "loc": ROOT_LOCATION,
    }


def test_error_dict_includes_custom_location():
    error_dict = get_error_dict(Exception("message"), "field")
    assert error_dict["loc"] == "field"


def test_error_dict_location_is_flattened():
    error_dict = get_error_dict(Exception("message"), ["field_test", 1, "name"])
    assert error_dict["loc"] == "fieldTest.1.name"
