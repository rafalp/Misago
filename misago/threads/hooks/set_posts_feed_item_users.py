from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...users.models import User


class SetPostFeedItemUsersHookAction(Protocol):
    """
    A standard Misago function used to set `User` instances on a `dict` with
    thread posts feed item's data.

    # Arguments

    ## `users: dict[int, "User"]`

    A `dict` of `User` instances, indexed by their IDs.

    ## `item: dict`

    A `dict` with posts feed item's data. Hook should update it using the `User`
    instances from the `users`.
    """

    def __call__(self, users: dict[int, "User"], item: dict): ...


class SetPostFeedItemUsersHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SetPostFeedItemUsersHookAction`

    A standard Misago function used to set `User` instances on a `dict` with
    thread posts feed item's data.

    See the [action](#action) section for details.

    ## `users: dict[int, "User"]`

    A `dict` of `User` instances, indexed by their IDs.

    ## `item: dict`

    A `dict` with posts feed item's data. Hook should update it using the `User`
    instances from the `users`.
    """

    def __call__(
        self,
        action: SetPostFeedItemUsersHookAction,
        users: dict[int, "User"],
        item: dict,
    ): ...


class SetPostFeedItemUsersHook(
    FilterHook[SetPostFeedItemUsersHookAction, SetPostFeedItemUsersHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to set `User` instances
    on a `dict` with thread posts feed item's data.

    # Example

    The code below implements a custom filter function that replaces post's real
    author with other one:

    ```python
    from typing import TYPE_CHECKING

    from misago.threads.hooks import set_posts_feed_item_users_hook

    if TYPE_CHECKING:
        from misago.users.models import User


    @set_posts_feed_item_users_hook.append_filter
    def replace_post_poster(
        action, users: dict[int, "User"], item: dict
    ):
        action(users, item)

        if item["type"] == "post":
            if override_poster := item["post"].plugin_data.get("poster_id"):
                item["poster"] = users[override_poster]
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SetPostFeedItemUsersHookAction,
        users: dict[int, "User"],
        item: dict,
    ):
        return super().__call__(action, users, item)


set_posts_feed_item_users_hook = SetPostFeedItemUsersHook(cache=False)
