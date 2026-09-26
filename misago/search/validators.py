from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext

from .hooks import validate_search_query_hook
from .query import (
    SearchQuery,
    SearchQueryAnd,
    SearchQueryKeyword,
    SearchQueryNot,
    SearchQueryOr,
    SearchQueryPhrase,
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
