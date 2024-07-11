# Threads filters

Threads filters are small strategy classes that add new filtering options to threads lists. Plugin authors can use the plugin system to add new or replace existing options.


## Writing a custom filter

Custom threads filters should extend the `ThreadsFilter` class defined in `misago.threads.filters`:

```python
from misago.threads.filters import ThreadsFilter

class CustomFilter(ThreadsFilter):
    ...
```

This class should define `name` and `slug` string attributes:

```python
from django.utils.translation import pgettext_lazy
from misago.threads.filters import ThreadsFilter

class CustomFilter(ThreadsFilter):
    name = pgettext_lazy("threads filter", "Custom threads")
    slug = "custom"
```

It should also define the `__call__` method that will be called with a single argument, the threads queryset instance:

```python
from django.utils.translation import pgettext_lazy
from misago.threads.filters import ThreadsFilter

class CustomFilter(ThreadsFilter):
    name = pgettext_lazy("threads filter", "Custom threads")
    slug = "custom"

    def __call__(self, queryset):
        return queryset.filter(...)
```

## Using the filter

Each threads list page has a dedicated plugin hook that enables developers to add custom filters to it:

- [`get_threads_page_filters_hook`](./hooks/get-threads-filters-page-hook.md)
- [`get_category_threads_page_filters_hook`](./hooks/get-category-threads-page-filters-hook.md)
- [`get_private_threads_page_filters_hook`](./hooks/get-private-threads-page_filters-hook.md)
