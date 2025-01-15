# `get_categories_page_component_hook`

This hook wraps the standard function that Misago uses to build a `dict` with data for the categories list component, used to display the list of categories on the categories page.


## Location

This hook can be imported from `misago.categories.hooks`:

```python
from misago.categories.hooks import get_categories_page_component_hook
```


## Filter

```python
def custom_get_categories_page_component_filter(
    action: GetCategoriesPageComponentHookAction, request: HttpRequest
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetCategoriesPageComponentHookAction`

A standard Misago function used to build a `dict` with data for the categories list component, used to display the list of categories on the categories page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


### Return value

A Python `dict` with data for the categories list component.


## Action

```python
def get_categories_page_component_action(request: HttpRequest) -> dict:
    ...
```

A standard Misago function used to build a `dict` with data for the categories list component, used to display the list of categories on the categories page.


### Arguments

#### `request: HttpRequest`

The request object.


### Return value

A Python `dict` with data for the categories list component.

Must have at least two keys: `categories` and `template_name`:

```python
{
    "categories": ...,
    "template_name": "misago/categories/list.html"
}
```


## Example

The code below implements a custom filter function that replaces default categories component with a custom one.

```python
from django.http import HttpRequest
from misago.categories.hooks import get_categories_component_hook


@get_categories_component_hook.append_filter
def custom_categories_list(action, request: HttpRequest) -> dict:
    return {
        "categories": [],
        "template_name": "plugin/categories_list.html",
    }
```