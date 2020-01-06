from ....validation import PASSWORD_MAX_LENGTH
from ..settings import resolve_password_max_length


def test_password_max_length_resolver_returns_max_password_length():
    value = resolve_password_max_length()
    assert value == PASSWORD_MAX_LENGTH
