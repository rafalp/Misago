from typing import TYPE_CHECKING, Optional, Protocol, Union

from django.db.models import Model
from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..query import SearchQuery


class ParseSearchQueryHookAction(Protocol):
    """
    Misago function used to parse a `str` to a `SearchQuery` object.

    # Arguments

    ## `query: str`

    A search query `str`.

    # Return value

    A `SearchQuery` object, or `None` if the query couldn't be parsed.
    """

    def __call__(self, query: str) -> Optional["SearchQuery"]: ...


class ParseSearchQueryHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ParseSearchQueryHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `query: str`

    A search query `str`.

    # Return value

    A `SearchQuery` object, or `None` if the query couldn't be parsed.
    """

    def __call__(
        self,
        action: ParseSearchQueryHookAction,
        query: str,
    ) -> Optional["SearchQuery"]: ...


class ParseSearchQueryHook(
    FilterHook[
        ParseSearchQueryHookAction,
        ParseSearchQueryHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to parse a search query
    for the forum search.

    It returns a 'SearchQuery' object that search backends can translate to
    a backend-specific search query.

    # Example
    
    Add a naive cache for queries shorter than a specified length:

    ```python
    from misago.search.hooks import parse_search_query_hook
    from misago.search.query import SearchQuery

    CACHED_QUERY_LEN = 100

    _search_query_cache: dict[str, SearchQuery] = {}

    @parse_search_query_hook.append_filter
    def cache_parsed_query(action, query: str) -> SearchQuery | None:
        if len(query) > CACHED_QUERY_LEN:
            return action(query)

        if query not in _search_query_cache:
            _search_query_cache[query] = action(query)

        return _search_query_cache[query]
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ParseSearchQueryHookAction,
        query: str,
    ) -> Optional["SearchQuery"]:
        return super().__call__(action, query)


parse_search_query_hook = ParseSearchQueryHook()
