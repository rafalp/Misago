# `get_category_threads_page_threads_hook`

This hook wraps the standard function that Misago uses to get complete threads data for the category threads page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_category_threads_page_threads_hook
```


## Filter

```python
def custom_get_category_threads_page_threads_filter(
    action: GetCategoryThreadsPageThreadsHookAction,
    request: HttpRequest,
    category: Category,
    kwargs: dict,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetCategoryThreadsPageThreadsHookAction`

A standard Misago function used to get the complete threads data for the category threads page. Returns a `dict` that is included in the template context under the `threads` key.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

A category instance.


#### `kwargs: dict`

A `dict` with `kwargs` this view was called with.


### Return value

A `dict` with the template context.


## Action

```python
def get_category_threads_page_threads_action(
    request: HttpRequest, category: Category, kwargs: dict
) -> dict:
    ...
```

A standard Misago function used to get the complete threads data for the category threads page. Returns a `dict` that is included in the template context under the `threads` key.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

A category instance.


#### `kwargs: dict`

A `dict` with `kwargs` this view was called with.


### Return value

A `dict` with the template context.


## Example

The code below implements a custom filter function makes view use a different threads list template instead of the default one.

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.threads.hooks import get_category_threads_page_threads_hook


@get_category_threads_page_threads_hook.append_filter
def replace_threads_list_template(
    action, request: HttpRequest, category: Category, kwargs: dict
) -> dict:
    data = action(request, kwargs)
    data["template_name"] = "plugin/threads_list.html"
    return data
```