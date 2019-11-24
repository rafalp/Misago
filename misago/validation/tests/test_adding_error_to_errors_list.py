from ..errors import UsernameIsInvalidError
from ..validation import add_error_to_list


def test_extra_error_is_added_to_errors_list():
    errors_list = []
    add_error_to_list(errors_list, "username", UsernameIsInvalidError())
    assert errors_list == [
        {
            "loc": ("username",),
            "msg": UsernameIsInvalidError.msg_template,
            "type": UsernameIsInvalidError.code,
        }
    ]


def test_extra_error_with_complex_location_is_added_to_errors_list():
    errors_list = []
    add_error_to_list(errors_list, [1, "username"], UsernameIsInvalidError())
    assert errors_list == [
        {
            "loc": (1, "username",),
            "msg": UsernameIsInvalidError.msg_template,
            "type": UsernameIsInvalidError.code,
        }
    ]
