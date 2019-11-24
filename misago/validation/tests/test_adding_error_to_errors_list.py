from ..errors import UsernameIsNotAvailableError
from ..validation import add_error_to_list


def test_extra_error_is_added_to_errors_list():
    errors_list = []
    add_error_to_list(errors_list, "username", UsernameIsNotAvailableError())
    assert errors_list == [
        {
            "loc": ("username",),
            "msg": UsernameIsNotAvailableError.msg_template,
            "type": UsernameIsNotAvailableError.code,
        }
    ]
