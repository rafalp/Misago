import re

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import npgettext, pgettext

from .hooks import validate_search_query_hook
from .query import (
    SearchQuery,
    SearchQueryAnd,
    SearchQueryKeyword,
    SearchQueryNot,
    SearchQueryOr,
    SearchQueryPhrase,
)


def validate_search_query_length(query: str, max_length: int):
    query_length = len(query)

    if query_length > max_length:
        raise ValidationError(
            message=npgettext(
                "search query validator",
                "Search query cannot be longer than %(max_length)d character (it has %(query_length)d).",
                "Search query cannot be longer than %(max_length)d characters (it has %(query_length)d).",
                query_length,
            ),
            code="max_length",
            params={
                "max_length": max_length,
                "query_length": query_length,
            }
        )


KEYWORD_RE = re.compile(r"[^\W_]+")
PHRASE_RE = re.compile(r"'[^']*'")


def validate_search_query_term_length(query: str, min_length: int):
    phrases = [phrase[1:-1].strip() for phrase in PHRASE_RE.findall(query)]
    query = PHRASE_RE.sub(" ", query)
    terms: list[str] = phrases + KEYWORD_RE.findall(query)

    if not terms:
        raise ValidationError(
            message=npgettext(
                "search query validator",
                "Search query must contain at least one term no shorter than %(min_length)d character.",
                "Search query must contain at least one term no shorter than %(min_length)d characters.",
                min_length,
            ),
            code="min_length",
            params={
                "min_length": min_length,
            }
        )

    for term in terms:
        if len(term) < min_length:
            raise ValidationError(
                message=npgettext(
                    "search query validator",
                    'Search term "%(term)s" is shorter than the required %(min_length)d character.',
                    'Search term "%(term)s" is shorter than the required %(min_length)d characters.',
                    min_length,
                ),
                code="min_length",
                params={
                    "term": term,
                    "min_length": min_length,
                }
            )


def validate_search_query(query: SearchQuery, request: HttpRequest | None = None):
    validate_search_query_hook(_validate_search_query_action, query, request)


def _validate_search_query_action(
    query: SearchQuery, request: HttpRequest | None = None
):
    validate_search_query_is_selective(query)


def validate_search_query_is_selective(query: SearchQuery):
    if not is_search_query_selective(query):
        raise ValidationError(
            message=pgettext(
                "search query validator",
                "This search query is too broad.",
            ),
            code="too_broad",
        )


def is_search_query_selective(query: SearchQuery) -> bool:
    if isinstance(query, (SearchQueryKeyword, SearchQueryPhrase)):
        return True

    if isinstance(query, SearchQueryNot):
        return False

    if isinstance(query, SearchQueryAnd):
        for sub_query in query.value:
            if is_search_query_selective(sub_query):
                return True
        else:
            return False

    if isinstance(query, SearchQueryOr):
        for sub_query in query.value:
            if not is_search_query_selective(sub_query):
                return False
        else:
            return True
