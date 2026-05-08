# `get_thread_moderation_actions_hook`

This hook wraps the standard function Misago uses to retrieve available moderation actions for a thread.


## Location

This hook can be imported from `misago.moderation.hooks`:

```python
from misago.moderation.hooks import get_thread_moderation_actions_hook
```


## Filter

```python
def custom_get_thread_moderation_actions_filter(
    action: GetThreadModerationActionsHookAction,
    permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None=None,
) -> list[type['ThreadModerationAction']]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadModerationActionsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread instance to return moderation actions for.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A Python `list` with `ThreadModerationAction` types.


## Action

```python
def get_thread_moderation_actions_action(
    permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None=None,
) -> list[type['ThreadModerationAction']]:
    ...
```

Misago function used to retrieve available moderation actions for a thread.


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread instance to return moderation actions for.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A Python `list` with `ThreadModerationAction` types.


## Example

The code below implements a custom filter function that includes a new moderation action for users with a special permission only:

```python
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from misago.moderation.actions import (
    ModerationActionResult,
    ThreadModerationAction,
)
from misago.moderation.hooks import get_thread_moderation_actions_hook
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


@get_thread_moderation_actions_hook.append_filter
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