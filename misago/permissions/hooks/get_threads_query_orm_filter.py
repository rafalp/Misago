from typing import Protocol

from django.db.models import Q

from ...plugins.hooks import FilterHook
from ..enums import CategoryThreadsQuery


class GetThreadsQueryORMFilterHookAction(Protocol):
    """
    A standard Misago function used to get Django's `Q` object instance to
    retrieve threads using a specified query.

    # Arguments

    ## `query: CategoryThreadsQuery | str`

    A `CategoryThreadsQuery` `StrEnum` or a `str` with the name of a query to use.

    ## `categories: set[int]`

    A `set` of `int`s with category IDs.

    ## `user_id: int | None`

    An `int` with the currently authenticated user ID, or `None` if the user
    is anonymous.

    # Return value

    A `Q` object instance to pass to the threads queryset's `filter()`.
    """

    def __call__(
        self,
        query: CategoryThreadsQuery | str,
        categories: set[int],
        user_id: int | None,
    ) -> Q | None: ...


class GetThreadsQueryORMFilterHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadsQueryORMFilterHookAction`

    A standard Misago function used to get Django's `Q` object instance to
    retrieve threads using a specified query.

    See the [action](#action) section for details.

    ## `query: CategoryThreadsQuery | str`

    A `CategoryThreadsQuery` `StrEnum` or a `str` with the name of a query to use.

    ## `categories: set[int]`

    A `set` of `int`s with category IDs.

    ## `user_id: int | None`

    An `int` with the currently authenticated user ID, or `None` if the user
    is anonymous.

    # Return value

    A `Q` object instance to pass to the threads queryset's `filter()`.
    """

    def __call__(
        self,
        action: GetThreadsQueryORMFilterHookAction,
        query: CategoryThreadsQuery | str,
        categories: list[int],
        user_id: int | None,
    ) -> Q | None: ...


class GetThreadsQueryORMFilterHook(
    FilterHook[GetThreadsQueryORMFilterHookAction, GetThreadsQueryORMFilterHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get Django's `Q`
    object instance to retrieve threads using a specified query.

    # Example

    The code below implements a custom filter function that specifies a custom
    query to use when retrieving the threads list:

    ```python
    from django.db.models import Q
    from misago.permissions.hooks import get_threads_query_orm_filter_hook

    @get_threads_query_orm_filter_hook.append_filter
    def get_category_access_level(
        action,
        query: str,
        categories: set[int],
        user_id: int | None,
    ) -> Q | None:
        # Show user only their unapproved threads
        if query == "unapproved_only":
            return Q(
                category_id__in=categories,
                starter_id=user_id,
                is_unapproved=True,
            )

        return action(query, categories, user_id)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadsQueryORMFilterHookAction,
        query: CategoryThreadsQuery | str,
        categories: set[int],
        user_id: int | None,
    ) -> Q | None:
        return super().__call__(action, query, categories, user_id)


get_threads_query_orm_filter_hook = GetThreadsQueryORMFilterHook()
