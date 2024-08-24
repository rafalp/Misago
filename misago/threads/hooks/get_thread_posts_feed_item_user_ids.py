from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import ActionHook
from ..models import Thread


class GetThreadPostsFeedItemUserIDsHookAction(Protocol):
    """
    A function that finds user ids in the `item` and updates `user_ids` set with
    them.

    # Arguments

    ## `item: dict`

    A `dict` with feed's item data.

    ## `user_ids: set[int]`

    A `set` of `int`s being user ids to retrieve from the database that action
    should mutate calling its `add` or `update` methods.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
        page: int | None = None,
    ): ...


class GetThreadPostsFeedItemUserIDsHook(
    ActionHook[GetThreadPostsFeedItemUserIDsHookAction]
):
    """
    This hook enables plugins to include extra user IDs stored on posts in the
    query that Misago uses to retrieve `User`s to display on thread and private
    thread replies pages.

    # Example

    The code below implements a custom function that adds

    ```python
    from misago.threads.hooks import get_thread_posts_feed_item_user_ids_hook


    @get_thread_posts_feed_item_user_ids_hook.append_action
    def include_plugin_users(
        item: dict,
        user_ids: set[int],
    ):
        if item["type"] != "post":
            return

        if linked_user_ids := item["plugin_data"].get("linked_posts_users"):
            user_ids.update(linked_user_ids)
    ```
    """

    __slots__ = ActionHook.__slots__

    def __call__(
        self,
        item: dict,
        user_ids: set[int],
    ):
        super().__call__(item, user_ids)


get_thread_posts_feed_item_user_ids_hook = GetThreadPostsFeedItemUserIDsHook()
