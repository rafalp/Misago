from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..query import SearchQuery


class ValidateSearchQueryHookAction(Protocol):
    """
    Misago function used to validate a `SearchQuery` object.

    Raises `ValidationError` if query is not valid.

    # Arguments

    ## `search_query: SearchQuery`

    A `SearchQuery` object to validate.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self, search_query: "SearchQuery", request: HttpRequest | None = None
    ) -> None: ...


class ValidateSearchQueryHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ValidateSearchQueryHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `search_query: SearchQuery`

    A `SearchQuery` object to validate.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: ValidateSearchQueryHookAction,
        search_query: "SearchQuery",
        request: HttpRequest | None = None,
    ) -> None: ...


class ValidateSearchQueryHook(
    FilterHook[
        ValidateSearchQueryHookAction,
        ValidateSearchQueryHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to validate a search query
    for the forum search.

    It returns nothing, but should raise `ValidationError` if the query fails to
    validate.

    # Example

    Validate that search doesn't contain too many keywords:

    ```python
    from django.core.exceptions import ValidationError
    from misago.search.hooks import validate_search_query_hook
    from misago.search.query import SearchQuery

    @validate_search_query_hook.append_filter
    def validate_search_query_keywords(action, search_query: SearchQuery):
        action(query)

        if count_keywords(query) > 5:
            raise ValidationError(
                "Search query can't contain more than 5 keywords."
            )


    def count_keywords(query: SearchQuery) -> int:
        ...  # Implemented by a plugin...
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ValidateSearchQueryHookAction,
        search_query: "SearchQuery",
        request: HttpRequest | None = None,
    ) -> None:
        super().__call__(action, search_query, request)


validate_search_query_hook = ValidateSearchQueryHook()
