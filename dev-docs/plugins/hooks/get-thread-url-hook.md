# `get_thread_url_hook`

This hook wraps the standard function that Misago useds to retrieve a thread URL based on its category type.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_url_hook
```


## Filter

```python
def custom_get_thread_url_filter(
    action: GetThreadUrlHookAction,
    thread: Thread,
    category: Category | None=None,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadUrlHookAction`

A standard Misago function used to retrieve a thread URL based on its category type.

See the [action](#action) section for details.


#### `thread: Thread`

A `Thread` instance.


#### `category: Category`

A `Category` instance, if `thread.category` was not populated using `select_related` or `prefetch_related`. Otherwise it's `None` and `thread.category` should be used instead.


### Return value

An `str` with URL.


## Action

```python
def get_thread_url_action(thread: Thread, category: Category | None=None) -> QuerySet:
    ...
```

A standard Misago function used to retrieve a thread URL based on its category type.


### Arguments

#### `thread: Thread`

A `Thread` instance.


#### `category: Category`

A `Category` instance, if `thread.category` was not populated using `select_related` or `prefetch_related`. Otherwise it's `None` and `thread.category` should be used instead.


### Return value

An `str` with URL.


## Example

The code below implements a custom filter function that returns thread's URL for custom category type:

```python
from django.urls import reverse
from misago.categories.models import Category
from misago.threads.hooks import get_thread_url_hook
from misago.threads.models import Thread


@get_thread_url_hook.append_filter
def get_thread_blog_url(
    action, thread: Thread, category: Category | None = None
):
    if (category or thread.category).plugin_data.get("is_blog"):
        return reverse(
            "blog", kwargs={"id": thread.id, "slug": thread.slug}
        )

    return = action(thread, category)
```