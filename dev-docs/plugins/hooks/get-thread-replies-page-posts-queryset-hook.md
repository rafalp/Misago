# `get_thread_replies_page_posts_queryset_hook`

This hook wraps the standard function that Misago uses to get a queryset with posts to display on the thread replies page.

This hook should be used only to add new joins with `select_related`. To filter posts, use the `filter_thread_posts_queryset` hook instead.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_replies_page_posts_queryset_hook
```


## Filter

```python
def custom_get_thread_replies_page_posts_queryset_filter(
    action: GetThreadRepliesPagePostsQuerysetHookAction,
    request: HttpRequest,
    thread: Thread,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadRepliesPagePostsQuerysetHookAction`

A standard Misago function used to get a queryset used to get posts displayed on the thread replies page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


### Return value

An unfiltered `QuerySet` instance to use to get posts displayed on the thread replies page.


## Action

```python
def get_thread_replies_page_posts_queryset_action(request: HttpRequest, thread: Thread) -> QuerySet:
    ...
```

A standard Misago function used to get a queryset used to get posts displayed on the thread replies page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

A `Thread` instance.


### Return value

An unfiltered `QuerySet` instance to use to get posts displayed on the thread replies page.


## Example

The code below implements a custom filter function that joins plugin's table with `select_related`:

```python
from django.http import HttpRequest
from misago.threads.hooks import get_thread_replies_page_posts_queryset_hook
from misago.threads.models import Thread


@get_thread_replies_page_posts_queryset_hook.append_filter
def select_related_plugin_data(
    action, request: HttpRequest, thread: Thread
):
    queryset = action(request, thread)
    return queryset.select_related("plugin")
```