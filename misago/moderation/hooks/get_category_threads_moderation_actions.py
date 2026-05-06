from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...permissions.proxy import UserPermissionsProxy
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..actions import ThreadsModerationAction


class GetCategoryThreadsModerationActionsHookAction(Protocol):
    """
    Misago function used to get available moderation actions for
    a category's threads list.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category instance to return moderation actions for.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A Python `list` with `ThreadsModerationAction` types.
    """

    def __call__(
        self,
        permissions: UserPermissionsProxy,
        category: Category,
        request: HttpRequest | None = None,
    ) -> list[type["ThreadsModerationAction"]]: ...


class GetCategoryThreadsModerationActionsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetCategoryThreadsModerationActionsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category instance to return moderation actions for.

    ## `request: HttpRequest | None = None`

    The request object or `None` if not available.

    # Return value

    A Python `list` with `ThreadsModerationAction` types.
    """

    def __call__(
        self,
        action: GetCategoryThreadsModerationActionsHookAction,
        permissions: UserPermissionsProxy,
        category: Category,
        request: HttpRequest | None = None,
    ) -> list[type["ThreadsModerationAction"]]: ...


class GetCategoryThreadsModerationActionsHook(
    FilterHook[
        GetCategoryThreadsModerationActionsHookAction,
        GetCategoryThreadsModerationActionsHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get available
    moderation actions for a category's threads list.

    # Example

    The code below implements a custom filter function that includes a new moderation
    action for users with a special permission only:

    ```python
    from django.contrib import messages
    from django.core.exceptions import ValidationError
    from django.http import HttpRequest
    from misago.category.models import Category
    from misago.moderation.actions import (
        ModerationActionResult,
        ThreadsModerationAction,
    )
    from misago.moderation.hooks import get_category_threads_moderation_actions_hook
    from misago.permissions.proxy import UserPermissionsProxy


    class ShadowBanModerationAction(ThreadsModerationAction):
        id: "shadow_ban"
        button_label: "Shadow ban"

        def validate(self):
            for thread in self.threads:
                if not thread.plugin_data.get("shadow_banned"):
                    return

            raise ValidationError("Threads are already shadow banned.")

        def execute(self) -> ModerationActionResult:
            valid_threads = [
                thread for thread in self.threads
                if not thread.plugin_data.get("shadow_banned")
            ]

            for thread in valid_threads:
                thread.plugin_data["shadow_banned] = True
                thread.save()

            messages.success(self.request, "Threads shadow banned")

            return ModerationActionResult(
                updated_items=[thread.id for thread in valid_threads]
            )


    @get_category_threads_moderation_actions_hook.append_filter
    def include_custom_moderation_action(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
        request: HttpRequest | None = None,
    ) -> list[type[ThreadsModerationAction]]:
        moderation_actions = action(category, request)
        if request.permissions.is_global_moderator:
            moderation_actions.append(ShadowBanModerationAction)
        return moderation_actions
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetCategoryThreadsModerationActionsHookAction,
        permissions: UserPermissionsProxy,
        category: Category,
        request: HttpRequest | None = None,
    ) -> list[type["ThreadsModerationAction"]]:
        return super().__call__(action, permissions, category, request)


get_category_threads_moderation_actions_hook = GetCategoryThreadsModerationActionsHook()
