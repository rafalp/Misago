from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..filters import ThreadsFilter


class GetPrivateThreadsPageFiltersHookAction(Protocol):
    """
    A standard Misago function used to get available filters for
    the private threads list.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `list` with `ThreadsFilter` instances.
    """

    def __call__(self, request: HttpRequest) -> list[ThreadsFilter]: ...


class GetPrivateThreadsPageFiltersHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadsPageFiltersHookAction`

    A standard Misago function used to get available filters for
    the private threads list.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `list` with `ThreadsFilter` instances.
    """

    def __call__(
        self,
        action: GetPrivateThreadsPageFiltersHookAction,
        request: HttpRequest,
    ) -> list[ThreadsFilter]: ...


class GetPrivateThreadsPageFiltersHook(
    FilterHook[
        GetPrivateThreadsPageFiltersHookAction,
        GetPrivateThreadsPageFiltersHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get available
    filters for the private threads list.

    # Example

    The code below implements a custom filter function that includes a new filter:

    ```python
    from django.http import HttpRequest
    from misago.threads.filters import ThreadsFilter
    from misago.threads.hooks import get_private_threads_page_filters_hook


    class CustomFilter(ThreadsFilter):
        name: str = "Custom filter"
        slug: str = "custom"

        def __callable__(self, queryset):
            if not self.request.user.is_authenticated:
                return queryset

            return queryset.filter(plugin_data__custom=True)


    @get_private_threads_page_filters_hook.append_filter
    def include_custom_filter(action, request: HttpRequest) -> list[ThreadsFilter]:
        filters = action(request)
        filters.append(CustomFilter(request))
        return filters
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadsPageFiltersHookAction,
        request: HttpRequest,
    ) -> list[ThreadsFilter]:
        return super().__call__(action, request)


get_private_threads_page_filters_hook = GetPrivateThreadsPageFiltersHook(cache=False)
