# `get_thread_replies_page_thread_queryset_hook`

This hook wraps the standard function that Misago uses to get a queryset used to get a thread for the thread replies page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_replies_page_thread_queryset_hook
```


## Filter

```python
def custom_get_thread_replies_page_thread_queryset_filter(
    action: GetThreadRepliesPageThreadQuerysetHookAction,
    request: HttpRequest,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadRepliesPageThreadQuerysetHookAction`

A standard Misago function used to get a queryset used to get a thread for the thread replies page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


### Return value

A `QuerySet` instance to use in the `get_object_or_404` call.


## Action

```python
def get_thread_replies_page_thread_queryset_action(request: HttpRequest) -> QuerySet:
    ...
```

A standard Misago function used to get a queryset used to get a thread for the thread replies page.


### Arguments

#### `request: HttpRequest`

The request object.


### Return value

A `QuerySet` instance to use in the `get_object_or_404` call.


## Example

The code below implements a custom filter function that joins plugin's table with `select_related`:

```python
from django.http import HttpRequest
from misago.threads.hooks import get_thread_replies_page_thread_queryset_hook


@get_thread_replies_page_thread_queryset_hook.append_filter
def select_related_plugin_data(action, request: HttpRequest):
    queryset = action(request)
    return queryset.select_related("plugin")
```