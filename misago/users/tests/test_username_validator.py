import pytest

from ..errors import UsernameError
from ..validators import usernamestr

settings = {"username_min_length": 1, "username_max_length": 4}


def test_usernamestr_constraint_returns_string_type():
    type_ = usernamestr(settings)
    assert issubclass(type_, str)


def test_usernamestr_constraint_raises_username_error_if_username_is_invalid():
    type_ = usernamestr(settings)
    with pytest.raises(UsernameError):
        type_.validate("not!")
