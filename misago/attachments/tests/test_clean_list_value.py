# pylint: disable=use-implicit-booleaness-not-comparison
from ..models import clean_list_value


def test_none_is_cleaned_to_empty_list():
    assert clean_list_value(None) == []


def test_empty_strings_are_removed_on_cleaning():
    assert clean_list_value([" ", ""]) == []


def test_strings_whitespaces_are_trimmed_on_cleaning():
    assert clean_list_value([" a", "b"]) == ["a", "b"]


def test_strings_are_sorted_on_cleaning():
    assert clean_list_value([" c", "a", "b"]) == ["a", "b", "c"]


def test_duplicates_are_removed_cleaning():
    assert clean_list_value([" c", "a", "c  "]) == ["a", "c"]


def test_empty_list_is_cleaned():
    assert clean_list_value([]) == []
