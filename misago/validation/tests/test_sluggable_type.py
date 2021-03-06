import pytest
from pydantic.errors import StrRegexError

from ..types import sluggablestr


def test_sluggablestr_constraint_returns_string_type():
    type_ = sluggablestr(min_length=5, max_length=15)
    assert issubclass(type_, str)


def test_sluggablestr_constraint_validates_sluggable_strs():
    type_ = sluggablestr(min_length=5, max_length=15)
    type_.validate("I'm sluggable str!")
    type_.validate("42")


def test_sluggablestr_constraint_raises_regex_error_if_str_is_not_sluggable():
    type_ = sluggablestr(min_length=5, max_length=15)
    with pytest.raises(StrRegexError):
        type_.validate("!!!")
