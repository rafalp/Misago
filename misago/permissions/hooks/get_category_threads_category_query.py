from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ..enums import CategoryQueryContext

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class GetCategoryThreadsCategoryQueryHookAction(Protocol):
    """
    A standard Misago function used to get the name of the predefined database
    `WHERE` clause (represented as a `Q` object instance) to use to retrieve
    threads from the given category for displaying on the category threads page.

    Standard `WHERE` clauses implemented by Misago can be retrieved from the
    `CategoryThreadsQuery` `StrEnum`:

    ```python
    from misago.permissions.enums import CategoryThreadsQuery
    ```

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: dict`

    A `dict` with category data.

    ## `context: CategoryQueryContext`

    A `CategoryQueryContext` `StrEnum` member describing the `category` position
    in the categories tree.

    Possible values:

    - `CURRENT`: the category for which the threads list is retrieved.
    - `CHILD`: a child (or other descendant) category of the current category.
    - `OTHER`: a category located elsewhere in the categories tree.

    # Return value

    A `CategoryThreadsQuery` member or a `str` with a custom clause name. If
    `None`, the query retrieving threads will skip this category. If multiple
    clauses should be `OR`ed together, a list of strings or `CategoryThreadsQuery`
    members can be returned.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: dict,
        context: CategoryQueryContext,
    ) -> str | list[str] | None: ...


class GetCategoryThreadsCategoryQueryHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetCategoryThreadsCategoryQueryHookAction`

    A standard Misago function used to get the name of the predefined database
    `WHERE` clause (represented as a `Q` object instance) to use to retrieve
    threads from the given category for displaying on the category threads page.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: dict`

    A `dict` with category data.

    ## `context: CategoryQueryContext`

    A `CategoryQueryContext` `StrEnum` member describing the `category` position
    in the categories tree.

    Possible values:

    - `CURRENT`: the category for which the threads list is retrieved.
    - `CHILD`: a child (or other descendant) category of the current category.
    - `OTHER`: a category located elsewhere in the categories tree.

    # Return value

    A `CategoryThreadsQuery` member or a `str` with a custom clause name. If
    `None`, the query retrieving threads will skip this category. If multiple
    clauses should be `OR`ed together, a list of strings or `CategoryThreadsQuery`
    members can be returned.
    """

    def __call__(
        self,
        action: GetCategoryThreadsCategoryQueryHookAction,
        permissions: "UserPermissionsProxy",
        category: dict,
        context: CategoryQueryContext,
    ) -> str | list[str] | None: ...


class GetCategoryThreadsCategoryQueryHook(
    FilterHook[
        GetCategoryThreadsCategoryQueryHookAction,
        GetCategoryThreadsCategoryQueryHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get the name of
    the predefined database `WHERE` clause (represented as a `Q` object instance)
    to use to retrieve threads from the given category for displaying on
    the category threads page.

    # Example

    The code below implements a custom filter function that specifies a custom
    `WHERE` clause supported by the `get_threads_query_orm_filter_hook`.

    ```python
    from misago.permissions.enums import CategoryQueryContext
    from misago.permissions.hooks import get_category_threads_category_query_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @get_category_threads_category_query_hook.append_filter
    def get_category_threads_category_query(
        action,
        permissions: UserPermissionsProxy,
        category: dict,
        context: CategoryQueryContext,
    ) -> str | list[str] | None:
        if (
            category.get("plugin_flag") and context == CategoryQueryContext.CURRENT
        ):
            return "plugin-where"

        return action(permissions, category, context)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetCategoryThreadsCategoryQueryHookAction,
        permissions: "UserPermissionsProxy",
        category: dict,
        context: CategoryQueryContext,
    ) -> str | list[str] | None:
        return super().__call__(action, permissions, category, context)


get_category_threads_category_query_hook = GetCategoryThreadsCategoryQueryHook()
