from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...users.models import User


class SetPostsFeedRelatedObjectsHookAction(Protocol):
    """
    Misago function used to set related objects on dicts containing
    posts feed data.

    # Arguments

    ## `feed: list[dict]`

    A list of `dict` objects with post feed items. This function updates these
    dicts with objects from the `related_objects` dictionary.

    ## `related_objects: dict`

    A `dict` with objects related to the feed's items.
    """

    def __call__(self, feed: list[dict], related_objects: dict): ...


class SetPostsFeedRelatedObjectsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SetPostsFeedRelatedObjectsHookAction`

    Misago function used to set related objects on dicts containing
    posts feed data.

    See the [action](#action) section for details.

    ## `feed: list[dict]`

    A list of `dict` objects with post feed items. This function updates these
    dicts with objects from the `related_objects` dictionary.

    ## `related_objects: dict`

    A `dict` with objects related to the feed's items.
    """

    def __call__(
        self,
        action: SetPostsFeedRelatedObjectsHookAction,
        feed: list[dict],
        related_objects: dict,
    ): ...


class SetPostsFeedRelatedObjectsHook(
    FilterHook[
        SetPostsFeedRelatedObjectsHookAction, SetPostsFeedRelatedObjectsHookFilter
    ]
):
    """
    This hook wraps the standard function that Misago uses to set related objects
    on dicts containing posts feed data.

    # Example

    The code below implements a custom filter function that populates feed's items
    with plugin objects

    ```python
    from misago.threads.hooks import set_posts_feed_related_objects_hook


    @set_posts_feed_related_objects_hook.append_filter
    def replace_post_poster(
        action, feed: list[dict], related_objects: dict
    ):
        action(feed, related_objects)

        for item in feed:
            if item["type"] == "post":
                plugin_obj = related_objects["plugin_objects"].get(
                    item["post"].plugin_data["plugin_relation_id"]
                )
                item["plugin_attr"] = plugin_obj
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SetPostsFeedRelatedObjectsHookAction,
        feed: list[dict],
        related_objects: dict,
    ):
        return super().__call__(action, feed, related_objects)


set_posts_feed_related_objects_hook = SetPostsFeedRelatedObjectsHook(cache=False)
