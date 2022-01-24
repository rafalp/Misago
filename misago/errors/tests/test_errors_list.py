import pytest

from .. import NotAdminError, NotAuthorizedError
from ..errorslist import ErrorsList


@pytest.fixture
def errors_list():
    return ErrorsList()


def test_error_is_added_to_errors_list(errors_list):
    errors_list.add_error("auth", NotAuthorizedError())
    assert errors_list == [
        {
            "loc": "auth",
            "msg": NotAuthorizedError.msg_template,
            "type": "auth_error.not_authorized",
        }
    ]


def test_duplicate_error_is_not_added_to_errors_list(errors_list):
    errors_list.add_error("auth", NotAuthorizedError())
    errors_list.add_error("auth", NotAuthorizedError())
    assert errors_list == [
        {
            "loc": "auth",
            "msg": NotAuthorizedError.msg_template,
            "type": "auth_error.not_authorized",
        }
    ]


def test_two_errors_lists_can_be_combined():
    first_list = ErrorsList()
    first_list.add_error("admin", NotAdminError())

    other_list = ErrorsList()
    other_list.add_error("auth", NotAuthorizedError())

    errors_list = first_list + other_list

    assert isinstance(errors_list, ErrorsList)
    assert errors_list == [
        {
            "loc": "admin",
            "msg": NotAdminError.msg_template,
            "type": "auth_error.not_admin",
        },
        {
            "loc": "auth",
            "msg": NotAuthorizedError.msg_template,
            "type": "auth_error.not_authorized",
        },
    ]


def test_combining_errors_lists_removes_duplicates():
    first_list = ErrorsList()
    first_list.add_error("admin", NotAdminError())
    first_list.add_error("auth", NotAuthorizedError())

    other_list = ErrorsList()
    other_list.add_error("auth", NotAuthorizedError())

    errors_list = first_list + other_list
    assert errors_list == [
        {
            "loc": "admin",
            "msg": NotAdminError.msg_template,
            "type": "auth_error.not_admin",
        },
        {
            "loc": "auth",
            "msg": NotAuthorizedError.msg_template,
            "type": "auth_error.not_authorized",
        },
    ]


def test_root_error_is_added_to_errors_list(errors_list):
    errors_list.add_root_error(NotAuthorizedError())
    assert errors_list == [
        {
            "loc": "__root__",
            "msg": NotAuthorizedError.msg_template,
            "type": "auth_error.not_authorized",
        }
    ]


def test_has_root_errors_property_returns_false_if_no_errors_are_present(
    errors_list,
):
    assert not errors_list.has_root_errors


def test_has_root_errors_property_returns_false_if_no_root_error_is_present(
    errors_list,
):
    errors_list.add_error("auth", NotAuthorizedError())
    assert not errors_list.has_root_errors


def test_has_root_errors_property_returns_true_if_root_error_is_present(errors_list):
    errors_list.add_root_error(NotAuthorizedError())
    assert errors_list.has_root_errors
