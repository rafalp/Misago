# `get_private_threads_breadcrumbs_hook`

This hook allows plugins to replace or extend the logic used to retrieve the private threads list breadcrumbs.


## Location

This hook can be imported from `misago.privatethreads.hooks`:

```python
from misago.privatethreads.hooks import get_private_threads_breadcrumbs_hook
```


## Filter

```python
def custom_get_private_threads_breadcrumbs_filter(
    action: GetPrivateThreadsBreadcrumbsHookAction,
    request: HttpRequest,
    category: Category,
) -> list[dict]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetPrivateThreadsBreadcrumbsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` to retrieve breadcrumbs for.


### Return value

A list of `dict`s representing the category's breadcrumbs.


## Action

```python
def get_private_threads_breadcrumbs_action(request: HttpRequest, category: Category) -> list[dict]:
    ...
```

Misago function for retrieving a private threads's breadcrumbs.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` to retrieve breadcrumbs for.


### Return value

A list of `dict`s representing the category's breadcrumbs.


## Example

Include extra data in the private threads list breadcrumbs:

```python
from django.http import HttpRequest
from misago.privatethreads.hooks import get_private_threads_breadcrumbs_hook
from misago.categories.models import Category


@get_private_threads_breadcrumbs_hook.append_filter
def set_private_threads_breadcrumb_icon(
    action, request: HttpRequest, category: Category
) -> list[dict]:
    breadcrumbs = action(request, category)
    breadcrumbs[0]["icon"] = "tabler/lock.svg"
    return breadcrumbs