# `get_threads_moderation_actions_hook`

This hook wraps the standard function that Misago uses to get available moderation actions for the threads list.


## Location

This hook can be imported from `misago.moderation.hooks`:

```python
from misago.moderation.hooks import get_threads_moderation_actions_hook
```


## Filter

```python
def custom_get_threads_moderation_actions_filter(
    action: GetThreadsModerationActionsHookAction,
    permissions: UserPermissionsProxy,
    request: HttpRequest | None=None,
) -> list[type['ThreadsModerationAction']]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadsModerationActionsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A Python `list` with `ThreadsModerationAction` types.


## Action

```python
def get_threads_moderation_actions_action(
    permissions: UserPermissionsProxy, request: HttpRequest | None=None
) -> list[type['ThreadsModerationAction']]:
    ...
```

Misago function used to get available moderation actions for the threads list.


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A Python `list` with `ThreadsModerationAction` types.


## Example

The code below implements a custom filter function that includes a new moderation action for users with a special permission only:

```python
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from misago.moderation.actions import (
    ModerationActionResult,
    ThreadsModerationAction,
)
from misago.moderation.hooks import get_threads_moderation_actions_hook


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


@get_threads_moderation_actions_hook.append_filter
def include_custom_moderation_action(
    action, request: HttpRequest | None = None
) -> list[type[ThreadsModerationAction]]:
    moderation_actions = action(request)
    if request.permissions.is_global_moderator:
        moderation_actions.append(ShadowBanModerationAction)
    return moderation_actions
```