# `get_private_thread_detail_view_posts_queryset_hook`

This hook wraps the standard function that Misago uses to get a queryset with posts to display on the private thread detail view.

This hook should be used only to add new joins with `select_related`. To filter posts, use the `filter_private_thread_posts_queryset` hook instead.


## Location

This hook can be imported from `misago.privatethreads.hooks`:

```python
from misago.privatethreads.hooks import get_private_thread_detail_view_posts_queryset_hook
```


## Filter

```python
def custom_get_private_thread_detail_view_posts_queryset_filter(
    action: GetPrivateThreadDetailViewPostsQuerysetHookAction,
    request: HttpRequest,
    thread: Thread,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetPrivateThreadDetailViewPostsQuerysetHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


### Return value

An unfiltered `QuerySet` instance to use to get posts displayed on the private thread detail view.


## Action

```python
def get_private_thread_detail_view_posts_queryset_action(request: HttpRequest, thread: Thread) -> QuerySet:
    ...
```

Misago function used to get a queryset used to get posts displayed on the private thread detail view.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

A `Thread` instance.


### Return value

An unfiltered `QuerySet` instance to use to get posts displayed on the private thread detail view.


## Example

The code below implements a custom filter function that joins plugin's table with `select_related`:

```python
from django.http import HttpRequest
from misago.privatethreads.hooks import get_private_thread_detail_view_posts_queryset_hook
from misago.threads.models import Thread


@get_private_thread_detail_view_posts_queryset_hook.append_filter
def select_related_plugin_data(
    action, request: HttpRequest, thread: Thread
):
    queryset = action(request, thread)
    return queryset.select_related("plugin")
```