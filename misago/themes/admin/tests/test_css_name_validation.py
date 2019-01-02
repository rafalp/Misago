import pytest
from django.forms import ValidationError

from ..validators import validate_css_name


def test_validation_fails_if_name_is_missing_css_extension():
    with pytest.raises(ValidationError):
        validate_css_name("filename")


def test_extension_validation_is_case_insensitive():
    validate_css_name("filename.CsS")


def test_validation_fails_if_name_starts_with_period():
    with pytest.raises(ValidationError):
        validate_css_name(".filename.css")


def test_validation_fails_if_name_contains_css_extension_only():
    with pytest.raises(ValidationError):
        validate_css_name(".css")


def test_validation_fails_if_name_contains_special_characters():
    with pytest.raises(ValidationError):
        validate_css_name("test().css")


def test_validation_fails_if_name_lacks_latin_characters_or_numbers():
    with pytest.raises(ValidationError):
        validate_css_name("_-.css")


def test_name_can_contain_underscores_scores_and_periods():
    validate_css_name("some_css-final2.dark.css")
