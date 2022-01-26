import pytest
from pydantic.errors import StrRegexError

from ..validators import threadtitlestr

settings = {"thread_title_min_length": 2, "thread_title_max_length": 5}


def test_threadtitlestr_constraint_returns_string_type():
    type_ = threadtitlestr(settings)
    assert issubclass(type_, str)


def test_threadtitlestr_constraint_validates_valid_title():
    type_ = threadtitlestr(settings)
    type_.validate("Test!")


def test_threadtitlestr_constraint_raises_regex_error_if_str_is_not_sluggable():
    type_ = threadtitlestr(settings)
    with pytest.raises(StrRegexError):
        type_.validate("!!!")
