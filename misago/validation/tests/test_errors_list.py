import pytest
from pydantic.errors import BoolError, NoneIsNotAllowedError

from ..errorslist import ErrorsList


@pytest.fixture
def errors_list():
    return ErrorsList()


def test_error_is_added_to_errors_list(errors_list):
    errors_list.add_error("field", NoneIsNotAllowedError())
    assert errors_list == [
        {
            "loc": "field",
            "type": "type_error.none.not_allowed",
            "msg": NoneIsNotAllowedError.msg_template,
        }
    ]


def test_duplicate_error_is_not_added_to_errors_list(errors_list):
    errors_list.add_error("field", NoneIsNotAllowedError())
    errors_list.add_error("field", NoneIsNotAllowedError())
    assert errors_list == [
        {
            "loc": "field",
            "type": "type_error.none.not_allowed",
            "msg": NoneIsNotAllowedError.msg_template,
        }
    ]


def test_two_errors_lists_can_be_combined():
    first_list = ErrorsList()
    first_list.add_error("lorem", NoneIsNotAllowedError())

    other_list = ErrorsList()
    other_list.add_error("ipsum", BoolError())

    errors_list = first_list + other_list

    assert isinstance(errors_list, ErrorsList)
    assert errors_list == [
        {
            "loc": "lorem",
            "type": "type_error.none.not_allowed",
            "msg": NoneIsNotAllowedError.msg_template,
        },
        {
            "loc": "ipsum",
            "type": "type_error.bool",
            "msg": BoolError.msg_template,
        },
    ]


def test_combining_errors_lists_removes_duplicates():
    first_list = ErrorsList()
    first_list.add_error("lorem", NoneIsNotAllowedError())
    first_list.add_error("ipsum", BoolError())

    other_list = ErrorsList()
    other_list.add_error("lorem", NoneIsNotAllowedError())

    errors_list = first_list + other_list
    assert errors_list == [
        {
            "loc": "lorem",
            "type": "type_error.none.not_allowed",
            "msg": NoneIsNotAllowedError.msg_template,
        },
        {
            "loc": "ipsum",
            "type": "type_error.bool",
            "msg": BoolError.msg_template,
        },
    ]


def test_root_error_is_added_to_errors_list(errors_list):
    errors_list.add_root_error(BoolError())
    assert errors_list == [
        {
            "loc": "__root__",
            "type": "type_error.bool",
            "msg": BoolError.msg_template,
        }
    ]


def test_has_root_errors_property_returns_false_if_no_errors_are_present(
    errors_list,
):
    assert not errors_list.has_root_errors


def test_has_root_errors_property_returns_false_if_no_root_error_is_present(
    errors_list,
):
    errors_list.add_error("field", BoolError())
    assert not errors_list.has_root_errors


def test_has_root_errors_property_returns_true_if_root_error_is_present(errors_list):
    errors_list.add_root_error(BoolError())
    assert errors_list.has_root_errors
