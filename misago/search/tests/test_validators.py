import pytest
from django.core.exceptions import ValidationError

from ..query import parse_search_query
from ..validators import (
    validate_search_query,
    validate_search_query_is_selective,
    validate_search_query_length,
    validate_search_query_term_length,
)


def test_validate_search_query_length_passes_valid_query():
    validate_search_query_length("search query", 20)


def test_validate_search_query_length_fails_too_long_query():
    with pytest.raises(ValidationError) as exc_info:
        validate_search_query_length("search query", 5)

    assert exc_info.value.code == "max_length"


def test_validate_search_query_term_length_passes_valid_query():
    validate_search_query_term_length("lorem ipsum 'dolor met'", 5)


def test_validate_search_query_term_length_fails_too_short_term():
    with pytest.raises(ValidationError) as exc_info:
        validate_search_query_term_length("lorem elit 'dolor met'", 5)

    assert exc_info.value.code == "min_length"
    assert exc_info.value.params == {"term": "elit", "min_length": 5}


def test_validate_search_query_term_length_fails_too_short_phrase():
    with pytest.raises(ValidationError) as exc_info:
        validate_search_query_term_length("lorem ipsum 'met'", 5)

    assert exc_info.value.code == "min_length"
    assert exc_info.value.params == {"term": "met", "min_length": 5}


def test_validate_search_query_passes_valid_query():
    query = parse_search_query("docker ('not compose' | -compose)")
    validate_search_query(query)


def test_validate_search_query_fails_too_broad_query():
    query = parse_search_query("-keyword")

    with pytest.raises(ValidationError) as exc_info:
        validate_search_query(query)

    assert exc_info.value.code == "too_broad"


def test_validate_search_query_is_selective_passes_keyword():
    query = parse_search_query("keyword")
    validate_search_query_is_selective(query)


def test_validate_search_query_is_selective_passes_phrase():
    query = parse_search_query("'lorem ipsum'")
    validate_search_query_is_selective(query)


def test_validate_search_query_is_selective_fails_not_keyword():
    query = parse_search_query("-keyword")

    with pytest.raises(ValidationError):
        validate_search_query_is_selective(query)


def test_validate_search_query_is_selective_fails_not_phrase():
    query = parse_search_query("-keyword")

    with pytest.raises(ValidationError):
        validate_search_query_is_selective(query)


def test_validate_search_query_is_selective_passes_keyword_and_keyword():
    query = parse_search_query("lorem ipsum")
    validate_search_query_is_selective(query)


def test_validate_search_query_is_selective_passes_keyword_and_not_keyword():
    query = parse_search_query("lorem -ipsum")
    validate_search_query_is_selective(query)


def test_validate_search_query_is_selective_fails_not_keyword_and_not_keyword():
    query = parse_search_query("-lorem -ipsum")

    with pytest.raises(ValidationError):
        validate_search_query_is_selective(query)


def test_validate_search_query_is_selective_passes_keyword_or_keyword():
    query = parse_search_query("lorem | ipsum")
    validate_search_query_is_selective(query)


def test_validate_search_query_is_selective_fails_keyword_or_not_keyword():
    query = parse_search_query("lorem | -ipsum")

    with pytest.raises(ValidationError):
        validate_search_query_is_selective(query)


def test_validate_search_query_is_selective_passes_keyword_and_phrase_or_not_keyword():
    query = parse_search_query("docker ('not compose' | -compose)")
    validate_search_query_is_selective(query)
