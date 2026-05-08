from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...permissions.proxy import UserPermissionsProxy
from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..actions import ThreadModerationAction


class GetPrivateThreadModerationActionsHookAction(Protocol):
    """
    Misago function used to retrieve available moderation actions
    for a private thread.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A thread instance to return moderation actions for.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A Python `list` with `ThreadModerationAction` types.
    """

    def __call__(
        self,
        permissions: UserPermissionsProxy,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> list[type["ThreadModerationAction"]]: ...


class GetPrivateThreadModerationActionsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadModerationActionsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A thread instance to return moderation actions for.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A Python `list` with `ThreadModerationAction` types.
    """

    def __call__(
        self,
        action: GetPrivateThreadModerationActionsHookAction,
        permissions: UserPermissionsProxy,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> list[type["ThreadModerationAction"]]: ...


class GetPrivateThreadModerationActionsHook(
    FilterHook[
        GetPrivateThreadModerationActionsHookAction,
        GetPrivateThreadModerationActionsHookFilter,
    ]
):
    """
    This hook wraps the standard function Misago uses to retrieve available
    moderation actions for a private thread.

    # Example

    The code below implements a custom filter function that includes a new moderation
    action for users with a special permission only:

    ```python
    from django.contrib import messages
    from django.core.exceptions import ValidationError
    from django.http import HttpRequest
    from misago.moderation.actions import (
        ModerationActionResult,
        ThreadModerationAction,
    )
    from misago.moderation.hooks import get_private_thread_moderation_actions_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread


    class ShadowBanModerationAction(ThreadModerationAction):
        id: "shadow_ban"
        button_label: "Shadow ban"

        def validate(self):
            if not self.thread.plugin_data.get("shadow_banned"):
                raise ValidationError("Thread is already shadow banned.")

        def execute(self) -> ModerationActionResult:
            self.thread.plugin_data["shadow_banned] = True
            self.thread.save()

            messages.success(self.request, "Thread shadow banned")

            return ModerationActionResult(
                updated_items=[self.thread.id]
            )


    @get_private_thread_moderation_actions_hook.append_filter
    def include_custom_moderation_action(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> list[type[ThreadModerationAction]]:
        moderation_actions = action(thread, request)
        if request.permissions.is_global_moderator:
            moderation_actions.append(ShadowBanModerationAction)
        return moderation_actions
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadModerationActionsHookAction,
        permissions: UserPermissionsProxy,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> list[type["ThreadModerationAction"]]:
        return super().__call__(action, permissions, thread, request)


get_private_thread_moderation_actions_hook = GetPrivateThreadModerationActionsHook()
