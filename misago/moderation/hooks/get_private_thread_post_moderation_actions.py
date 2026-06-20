from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...permissions.proxy import UserPermissionsProxy
from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..actions import PostModerationAction


class GetPrivateThreadPostModerationActionsHookAction(Protocol):
    """
    Misago function used to retrieve available moderation actions
    for a private thread’s posts.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `post: Post`

    A post instance to return moderation actions for.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A Python `list` with `PostModerationAction` types.
    """

    def __call__(
        self,
        permissions: UserPermissionsProxy,
        post: Post,
        request: HttpRequest | None = None,
    ) -> list[type["PostModerationAction"]]: ...


class GetPrivateThreadPostModerationActionsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadPostModerationActionsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `post: Post`

    A post instance to return moderation actions for.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A Python `list` with `PostModerationAction` types.
    """

    def __call__(
        self,
        action: GetPrivateThreadPostModerationActionsHookAction,
        permissions: UserPermissionsProxy,
        post: Post,
        request: HttpRequest | None = None,
    ) -> list[type["PostModerationAction"]]: ...


class GetPrivateThreadPostModerationActionsHook(
    FilterHook[
        GetPrivateThreadPostModerationActionsHookAction,
        GetPrivateThreadPostModerationActionsHookFilter,
    ]
):
    """
    This hook wraps the standard function Misago uses to retrieve available
    moderation actions for a private thread’s post.

    # Example

    The code below implements a custom filter function that includes a new moderation
    action for users with a special permission only:

    ```python
    from django.contrib import messages
    from django.core.exceptions import ValidationError
    from django.http import HttpRequest
    from misago.moderation.actions import (
        ModerationResult,
        PostModerationAction,
    )
    from misago.moderation.hooks import (
        get_private_thread_post_moderation_actions_hook,
    )
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread


    class ShadowBanModerationAction(PostModerationAction):
        id: "shadow_ban"
        button_label: "Shadow ban"

        def validate(self):
            if self.post.plugin_data.get("shadow_banned"):
                raise ValidationError("Post is already shadow banned.")

        def execute(self) -> ModerationResult:
            self.post.plugin_data["shadow_banned] = True
            self.post.save()

            messages.success(self.request, "Post shadow banned")

            return ModerationResult(
                updated_items=[self.post.id]
            )


    @get_private_thread_post_moderation_actions_hook.append_filter
    def include_custom_moderation_action(
        action,
        permissions: UserPermissionsProxy,
        post: Post,
        request: HttpRequest | None = None,
    ) -> list[type[PostModerationAction]]:
        moderation_actions = action(post, request)
        if request.permissions.is_global_moderator:
            moderation_actions.append(ShadowBanModerationAction)
        return moderation_actions
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadPostModerationActionsHookAction,
        permissions: UserPermissionsProxy,
        post: Post,
        request: HttpRequest | None = None,
    ) -> list[type["PostModerationAction"]]:
        return super().__call__(action, permissions, post, request)


get_private_thread_post_moderation_actions_hook = (
    GetPrivateThreadPostModerationActionsHook()
)
