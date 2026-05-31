from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...permissions.proxy import UserPermissionsProxy
from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..actions import PostsModerationAction


class GetThreadPostsModerationActionsHookAction(Protocol):
    """
    Misago function used to retrieve available moderation actions
    for a thread’s posts.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A thread instance to return posts moderation actions for.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A Python `list` with `PostsModerationAction` types.
    """

    def __call__(
        self,
        permissions: UserPermissionsProxy,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> list[type["PostsModerationAction"]]: ...


class GetThreadPostsModerationActionsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadPostsModerationActionsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A thread instance to return posts moderation actions for.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A Python `list` with `PostsModerationAction` types.
    """

    def __call__(
        self,
        action: GetThreadPostsModerationActionsHookAction,
        permissions: UserPermissionsProxy,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> list[type["PostsModerationAction"]]: ...


class GetThreadPostsModerationActionsHook(
    FilterHook[
        GetThreadPostsModerationActionsHookAction,
        GetThreadPostsModerationActionsHookFilter,
    ]
):
    """
    This hook wraps the standard function Misago uses to retrieve available
    moderation actions for a thread’s posts.

    # Example

    The code below implements a custom filter function that includes a new moderation
    action for users with a special permission only:

    ```python
    from django.contrib import messages
    from django.core.exceptions import ValidationError
    from django.http import HttpRequest
    from misago.moderation.actions import (
        ModerationActionResult,
        PostsModerationAction,
    )
    from misago.moderation.hooks import get_thread_posts_moderation_actions_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread


    class ShadowBanModerationAction(PostsModerationAction):
        id: "shadow_ban"
        button_label: "Shadow ban"

        def validate(self):
            for post in self.posts:
                if not thread.plugin_data.get("shadow_banned"):
                    return

            raise ValidationError("Posts are already shadow banned.")

        def execute(self) -> ModerationActionResult:
            valid_posts = [
                post for post in self.posts
                if not post.plugin_data.get("shadow_banned")
            ]

            for post in valid_posts:
                post.plugin_data["shadow_banned] = True
                post.save()

            messages.success(self.request, "Posts shadow banned")

            return ModerationActionResult(
                updated_items=[post.id for post in valid_posts]
            )


    @get_thread_posts_moderation_actions_hook.append_filter
    def include_custom_moderation_action(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> list[type[PostsModerationAction]]:
        moderation_actions = action(thread, request)
        if request.permissions.is_global_moderator:
            moderation_actions.append(ShadowBanModerationAction)
        return moderation_actions
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadPostsModerationActionsHookAction,
        permissions: UserPermissionsProxy,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> list[type["PostsModerationAction"]]:
        return super().__call__(action, permissions, thread, request)


get_thread_posts_moderation_actions_hook = GetThreadPostsModerationActionsHook()
