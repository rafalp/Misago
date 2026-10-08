import pytest
from django.core.exceptions import ValidationError

from ..forms import clean_search_query


def test_clean_search_query_normalizes_quotes():
    assert clean_search_query('lorem "ipsum"', 100, 5) == "lorem 'ipsum'"


def test_clean_search_query_validates_max_query_length():
    with pytest.raises(ValidationError) as exc_info:
        clean_search_query('lorem "ipsum"', 10, 5)

    assert exc_info.value.code == "max_length"


def test_clean_search_query_validates_min_term_length():
    with pytest.raises(ValidationError) as exc_info:
        clean_search_query('lorem "ipsum"', 100, 8)

    assert exc_info.value.code == "min_length"
