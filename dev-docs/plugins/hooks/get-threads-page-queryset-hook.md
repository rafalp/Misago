# `get_threads_page_queryset_hook`

This hook wraps the standard function that Misago uses to get base threads queryset for the threads page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_threads_page_queryset_hook
```


## Filter

```python
def custom_get_threads_page_queryset_filter(
    action: GetThreadsPageQuerysetHookAction, request: HttpRequest
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadsPageQuerysetHookAction`

A standard Misago function used to get the base threads queryset for the threads page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


### Return value

A `QuerySet` instance that will return `Threads`.


## Action

```python
def get_threads_page_queryset_action(request: HttpRequest) -> QuerySet:
    ...
```

A standard Misago function used to get the base threads queryset for the threads page.


### Arguments

#### `request: HttpRequest`

The request object.


### Return value

A `QuerySet` instance that will return `Threads`.


## Example

The code below implements a custom filter function that joins first post to every returned thread.

```python
from django.db.models import QuerySet
from django.http import HttpRequest
from misago.threads.hooks import get_threads_page_queryset_hook


@get_threads_page_queryset_hook.append_filter
def select_first_post(action, request: HttpRequest) -> QuerySet:
    queryset = action(request)
    return queryset.select_related("first_post")
```