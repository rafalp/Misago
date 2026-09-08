from typing import TYPE_CHECKING, Protocol, Union

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...categories.models import Category
    from ...categories.proxy import CategoryProxy
    from ..proxy import UserPermissionsProxy


class GetThreadsPostsQueriesHookAction(Protocol):
    """
    Standard Misago function used to get the names of predefined database `WHERE` clauses
    (represented as `Q` object instances) to use by other functions to retrieve
    posts from given categories.

    Standard `WHERE` clauses implemented by Misago can be retrieved from the
    `ThreadPostsQuery` `StrEnum`:

    ```python
    from misago.permissions.enums import ThreadPostsQuery
    ```

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `categories: list[Category | CategoryProxy]`

    A list of `Category` and `CategoryProxy` instances.

    # Return value

    A dict of sets of category ids grouped by `ThreadPostsQuery`.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Union["Category", "CategoryProxy"],
    ) -> dict[str, set[int]]: ...


class GetThreadsPostsQueriesHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadsPostsQueriesHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `categories: list[Category | CategoryProxy]`

    A list of `Category` and `CategoryProxy` instances.

    # Return value

    A dict of sets of category ids grouped by `ThreadPostsQuery`.
    """

    def __call__(
        self,
        action: GetThreadsPostsQueriesHookAction,
        permissions: "UserPermissionsProxy",
        category: Union["Category", "CategoryProxy"],
    ) -> dict[str, set[int]]: ...


class GetThreadsPostsQueriesHook(
    FilterHook[
        GetThreadsPostsQueriesHookAction,
        GetThreadsPostsQueriesHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get the names of
    predefined database `WHERE` clauses, represented as `Q` object instances,
    for use by other functions to retrieve posts from given categories.

    # Example

    The code below implements a custom filter function that removes a category
    from the queries if its muted by user

    ```python
    from misago.categories.models import Category
    from misago.categories.proxy import CategoryProxy
    from misago.permissions.hooks import get_threads_posts_queries_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @get_threads_posts_queries_hook.append_filter
    def get_threads_posts_queries(
        action,
        permissions: UserPermissionsProxy,
        categories: list[Category | CategoryProxy],
    ) -> dict[str, set[int]]:
        if permissions.user.is_authenticated:
            muted_categories = permissions.user.plugin_data.get("muted_categories", [])
            categories = [
                category for category in categories
                if category.id not in muted_categories
            ]

        return action(permissions, categories)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadsPostsQueriesHookAction,
        permissions: "UserPermissionsProxy",
        categories: list[Union["Category", "CategoryProxy"]],
    ) -> dict[str, set[int]]:
        return super().__call__(action, permissions, categories)


get_threads_posts_queries_hook = GetThreadsPostsQueriesHook()
