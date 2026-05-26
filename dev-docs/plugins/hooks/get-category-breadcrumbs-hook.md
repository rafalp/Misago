# `get_category_breadcrumbs_hook`

This hook allows plugins to replace or extend the logic used to retrieve a category's breadcrumbs.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_category_breadcrumbs_hook
```


## Filter

```python
def custom_get_category_breadcrumbs_filter(
    action: GetCategoryBreadcrumbsHookAction,
    request: HttpRequest,
    category: Category,
    include_category: bool=False,
) -> list[dict]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetCategoryBreadcrumbsHookAction`

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
def get_category_breadcrumbs_action(
    request: HttpRequest, category: Category, include_category: bool=False
) -> list[dict]:
    ...
```

Misago function for retrieving a category's breadcrumbs.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` to retrieve breadcrumbs for.


#### `include_category: bool = False`

Include `category` as the last breadcrumb.

Defaults to `False`.


### Return value

A list of `dict`s representing the category's breadcrumbs.


## Example

Include extra data in a category's breadcrumbs:

```python
from django.http import HttpRequest
from misago.categorys.hooks import get_category_breadcrumbs_hook
from misago.categorys.models import Category


@get_category_breadcrumbs_hook.append_filter
def set_category_breadcrumb_icon(
    action,
    request: HttpRequest,
    category: Category,
    include_category: bool = False,
) -> list[dict]:
    breadcrumbs = action(request, category, include_category)
    if include_category and category.is_locked:
        breadcrumbs[-1]["icon"] = "tabler/lock.svg"
    return breadcrumbs