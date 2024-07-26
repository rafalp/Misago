# `get_category_threads_page_filters_hook`

This hook wraps the standard function that Misago uses to get available filters for a category's threads list.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_category_threads_page_filters_hook
```


## Filter

```python
def custom_get_category_threads_page_filters_filter(
    action: GetCategoryThreadsPageFiltersHookAction,
    request: HttpRequest,
    category: Category,
) -> list[ThreadsFilter]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetCategoryThreadsPageFiltersHookAction`

A standard Misago function used to get available filters for a category's threads list.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

A category instance.


### Return value

A Python `list` with `ThreadsFilter` instances.


## Action

```python
def get_category_threads_page_filters_action(request: HttpRequest, category: Category) -> list[ThreadsFilter]:
    ...
```

A standard Misago function used to get available filters for a category's threads list.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

A category instance.


### Return value

A Python `list` with `ThreadsFilter` instances.


## Example

The code below implements a custom filter function that includes a new filter available to signed-in users only:

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.threads.filters import ThreadsFilter
from misago.threads.hooks import get_category_threads_page_filters_hook


class CustomFilter(ThreadsFilter):
    name: str = "Custom filter"
    slug: str = "custom"

    def __callable__(self, queryset):
        if not self.request.user.is_authenticated:
            return queryset

        return queryset.filter(plugin_data__custom=True)


@get_category_threads_page_filters_hook.append_filter
def include_custom_filter(
    action, request: HttpRequest, category: Category
) -> list[ThreadsFilter]:
    filters = action(request, category)
    filters.append(CustomFilter(request))
    return filters
```