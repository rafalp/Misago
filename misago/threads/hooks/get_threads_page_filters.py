from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..filters import ThreadsFilter


class GetThreadsPageFiltersHookAction(Protocol):
    """
    A standard Misago function used to get available filters for the threads list.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `list` with `ThreadsFilter` instances.
    """

    def __call__(self, request: HttpRequest) -> list[ThreadsFilter]: ...


class GetThreadsPageFiltersHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadsPageFiltersHookAction`

    A standard Misago function used to get available filters for the threads list.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `list` with `ThreadsFilter` instances.
    """

    def __call__(
        self,
        action: GetThreadsPageFiltersHookAction,
        request: HttpRequest,
    ) -> list[ThreadsFilter]: ...


class GetThreadsPageFiltersHook(
    FilterHook[GetThreadsPageFiltersHookAction, GetThreadsPageFiltersHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get available
    filters for the threads list.

    # Example

    The code below implements a custom filter function that includes a new filter
    available to signed-in users only:

    ```python
    from django.http import HttpRequest
    from misago.threads.filters import ThreadsFilter
    from misago.threads.hooks import get_threads_page_filters_hook


    class CustomFilter(ThreadsFilter):
        name: str = "Custom filter"
        slug: str = "custom"

        def __callable__(self, queryset):
            if not self.request.user.is_authenticated:
                return queryset

            return queryset.filter(plugin_data__custom=True)


    @get_threads_page_filters_hook.append_filter
    def include_custom_filter(action, request: HttpRequest) -> list[ThreadsFilter]:
        filters = action(request)
        filters.append(CustomFilter(request))
        return filters
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadsPageFiltersHookAction,
        request: HttpRequest,
    ) -> list[ThreadsFilter]:
        return super().__call__(action, request)


get_threads_page_filters_hook = GetThreadsPageFiltersHook(cache=False)
