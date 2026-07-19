# `get_thread_detail_view_moderation_result_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the moderation result in the thread detail view.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_detail_view_moderation_result_data_hook
```


## Filter

```python
def custom_get_thread_detail_view_moderation_result_data_filter(
    action: GetThreadDetailViewModerationResultDataHookAction,
    request: HttpRequest,
    thread: Thread,
    result: ModerationResult,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadDetailViewModerationResultDataHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `result: ModerationResult`

The `ModerationResult` instance returned by a moderation action.


### Return value

A Python `dict` with context data to use to `render` the moderation result.


## Action

```python
def get_thread_detail_view_moderation_result_data_action(
    request: HttpRequest, thread: Thread, result: ModerationResult
) -> dict:
    ...
```

Misago function used to get the template context data for a moderation result in the thread detail view.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `result: ModerationResult`

The `ModerationResult` instance returned by a moderation action.


### Return value

A Python `dict` with context data to use to `render` the moderation result.


## Example

The code below implements a custom filter function that injects a template component into the thread moderation result:

```python
from django.http import HttpRequest
from misago.moderation.actions import ModerationResult
from misago.threads.hooks import (
    get_thread_detail_view_moderation_result_data_hook
)
from misago.threads.models import Thread


@get_thread_detail_view_moderation_result_data_hook.append_filter
def include_plugin_component(
    action, request: HttpRequest, thread: Thread, result: ModerationResult
) -> dict:
    context = action(request, thread, result)

    if result.context.get("plugin"):
        context["extra_components"].append({
            "id": "plugin_component",
            "template_name": "myplugin/component.html"
        })

    return context
```