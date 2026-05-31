# `get_private_thread_detail_view_moderation_result_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the moderation result in the private thread detail view.


## Location

This hook can be imported from `misago.privatethreads.hooks`:

```python
from misago.privatethreads.hooks import get_private_thread_detail_view_moderation_result_data_hook
```


## Filter

```python
def custom_get_private_thread_detail_view_moderation_result_data_filter(
    action: GetPrivateThreadDetailViewModerationResultDataHookAction,
    request: HttpRequest,
    thread: Thread,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetPrivateThreadDetailViewModerationResultDataHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

A `Thread` instance.


### Return value

A Python `dict` with context data to use to `render` the moderation result.


## Action

```python
def get_private_thread_detail_view_moderation_result_data_action(request: HttpRequest, thread: Thread) -> dict:
    ...
```

Misago function used to get the template context data for the moderation result in the private thread detail view.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

A `Thread` instance.


### Return value

A Python `dict` with context data to use to `render` the moderation result.


## Example

The code below implements a custom filter function that injects a template component into the thread moderation result:

```python
from django.http import HttpRequest
from misago.privatethreads.hooks import (
    get_private_thread_detail_view_moderation_result_data_hook
)
from misago.threads.models import Thread


@get_private_thread_detail_view_moderation_result_data_hook.append_filter
def include_plugin_component(
    action, request: HttpRequest, thread: Thread
) -> dict:
    context = action(request, thread)
    context["extra_components"].append({
        "id": "plugin_component",
        "template_name": "myplugin/component.html"
    })

    return context
```