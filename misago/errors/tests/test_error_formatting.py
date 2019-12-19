from .. import AuthError, InvalidCredentialsError
from ..format import ROOT_LOCATION, get_error_dict, get_error_type


def test_error_dict_includes_error_messsage():
    error_dict = get_error_dict(Exception("message"))
    assert error_dict["msg"] == "message"


def test_error_dict_includes_error_type():
    error_dict = get_error_dict(Exception("message"))
    assert error_dict["type"] == "value_error.exception"


def test_error_dict_includes_default_location():
    error_dict = get_error_dict(Exception("message"))
    assert error_dict["loc"] == (ROOT_LOCATION,)


def test_error_dict_includes_provided_location():
    error_dict = get_error_dict(Exception("message"), "field")
    assert error_dict["loc"] == ("field",)


def test_error_dict_includes_provided_sequence_location():
    error_dict = get_error_dict(Exception("message"), ["field", 1, "name"])
    assert error_dict["loc"] == ("field", 1, "name",)


def test_error_type_is_resolved_for_assertion_error():
    assert get_error_type(AssertionError()) == "assertion_error"


def test_error_type_is_resolved_for_value_error():
    assert get_error_type(ValueError()) == "value_error.value"


def test_error_type_is_resolved_for_type_error():
    assert get_error_type(TypeError()) == "type_error.type"


def test_error_type_is_resolved_for_auth_error():
    assert get_error_type(AuthError()) == "auth_error.auth"


def test_error_type_is_resolved_for_pydantic_error():
    assert (
        get_error_type(InvalidCredentialsError()) == "value_error.invalid_credentials"
    )
