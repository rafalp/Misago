# `get_threads_page_moderation_actions_hook`

This hook wraps the standard function that Misago uses to get available moderation actions for the threads list.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_threads_page_moderation_actions_hook
```


## Filter

```python
def custom_get_threads_page_moderation_actions_filter(
    action: GetThreadsPageModerationActionsHookAction,
    request: HttpRequest,
) -> list[Type[ThreadsBulkModerationAction]]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadsPageModerationActionsHookAction`

A standard Misago function used to get available filters for the threads list.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


### Return value

A Python `list` with `ThreadsBulkModerationAction` types.


## Action

```python
def get_threads_page_moderation_actions_action(request: HttpRequest) -> list[Type[ThreadsBulkModerationAction]]:
    ...
```

A standard Misago function used to get available moderation actions for the threads list.


### Arguments

#### `request: HttpRequest`

The request object.


### Return value

A Python `list` with `ThreadsBulkModerationAction` types.


## Example

The code below implements a custom filter function that includes a new moderation action for users with a special permission only:

```python
from django.http import HttpRequest
from misago.moderation.threads import ModerationResult, ThreadsBulkModerationAction
from misago.threads.hooks import get_threads_page_moderation_actions_hook
from misago.threads.models import Thread


class CustomModerationAction(ThreadsBulkModerationAction):
    id: str = "custom"
    name: str = "Custom"

    def __call__(
        self, request: HttpRequest, threads: list[Thread]
    ) -> ModerationResult | None:
        ...


@get_threads_page_moderation_actions_hook.append_filter
def include_custom_moderation_action(
    action, request: HttpRequest
) -> list[Type[ThreadsBulkModerationAction]]:
    moderation_actions = action(request)
    if request.user_permissions.is_global_moderator:
        moderation_actions.append(ThreadsBulkModerationAction)
    return moderation_actions
```