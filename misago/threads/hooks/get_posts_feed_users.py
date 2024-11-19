from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...users.models import User


class GetThreadPostsFeedUsersHookAction(Protocol):
    """
    A standard Misago function used to get a `dict` of `User` instances used
    to display thread posts feed. Users have their `group` field already populated.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `user_ids: set[int]`

    A set of IDs of `User` objects to retrieve from the database

    ## Return value

    A `dict` of `User` instances, indexed by their IDs.
    """

    def __call__(
        self,
        request: HttpRequest,
        user_ids: set[int],
    ) -> dict[int, "User"]: ...


class GetPostsFeedUsersHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadPostsFeedUsersHookAction`

    A standard Misago function used to get a `dict` of `User` instances used
    to display thread posts feed. Users have their `group` field populated.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `user_ids: set[int]`

    A set of IDs of `User` objects to retrieve from the database

    ## Return value

    A `dict` of `User` instances, indexed by their IDs.
    """

    def __call__(
        self,
        action: GetThreadPostsFeedUsersHookAction,
        request: HttpRequest,
        user_ids: set[int],
    ) -> dict[int, "User"]: ...


class GetPostsFeedUsersHook(
    FilterHook[GetThreadPostsFeedUsersHookAction, GetPostsFeedUsersHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get a `dict` of
    `User` instances used to display thread posts feed. Users have their `group`
    field already populated.

    # Example

    The code below implements a custom filter function that removes some users
    from the dictionary, making them display on a posts feed as deleted users.

    ```python
    from typing import TYPE_CHECKING

    from django.http import HttpRequest
    from misago.threads.hooks import get_posts_feed_users_hook

    if TYPE_CHECKING:
        from misago.users.models import User


    @get_posts_feed_users_hook.append_filter
    def replace_post_poster(
        action, request: HttpRequest, user_ids: set[int]
    ) -> dict[int, "User"]:
        users = action(request, user_ids)

        for user_id, user in list(users.items())
            if user.plugin_data.get("is_hidden"):
                del users[user_id]

        return users
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadPostsFeedUsersHookAction,
        request: HttpRequest,
        user_ids: set[int],
    ) -> dict[int, "User"]:
        return super().__call__(action, request, user_ids)


get_posts_feed_users_hook = GetPostsFeedUsersHook(cache=False)
