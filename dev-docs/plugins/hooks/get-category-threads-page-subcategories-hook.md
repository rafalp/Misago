# `get_category_threads_page_subcategories_hook`

This hook wraps the standard function that Misago uses to build a `dict` with data for the categories list component, used to display the list of subcategories on the category threads page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_category_threads_page_subcategories_hook
```


## Filter

```python
def custom_get_category_threads_page_subcategories_filter(
    action: GetCategoryThreadsPageSubcategoriesHookAction,
    request: HttpRequest,
    category: Category,
) -> dict | None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetCategoryThreadsPageSubcategoriesHookAction`

A standard Misago function used to build a `dict` with data for the categories list component, used to display the list of subcategories on the category threads page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

A category instance.


### Return value

A Python `dict` with data for the categories list component.

Must have at least two keys: `categories` and `template_name`:

```python
{
    "categories": ...,
    "template_name": "misago/category/subcategories.html"
}
```

To suppress categories lists on a page, return `None`.


## Action

```python
def get_category_threads_page_subcategories_action(request: HttpRequest, category: Category) -> dict | None:
    ...
```

A standard Misago function used to build a `dict` with data for the categories list component, used to display the list of subcategories on the category threads page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

A category instance.


### Return value

A Python `dict` with data for the categories list component.

Must have at least two keys: `categories` and `template_name`:

```python
{
    "categories": ...,
    "template_name": "misago/category/subcategories.html"
}
```

To suppress categories lists on a page, return `None`.


## Example

The code below implements a custom filter function that replaces full subcategories component's template with a custom one

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.threads.hooks import get_category_threads_page_subcategories_hook


@get_category_threads_page_subcategories_hook.append_filter
def customize_subcategories_template(
    action, request: HttpRequest, category: Category
) -> dict | None:
    data = action(request, category)
    data["template_name"] = "plugin/subcategories.html"
    return data
```