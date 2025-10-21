from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.filters import ThreadsFilter


class GetPrivateThreadListFiltersHookAction(Protocol):
    """
    Misago function used to get available filters for
    the private thread list view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `list` with `ThreadsFilter` instances.
    """

    def __call__(self, request: HttpRequest) -> list[ThreadsFilter]: ...


class GetPrivateThreadListFiltersHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadListFiltersHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A Python `list` with `ThreadsFilter` instances.
    """

    def __call__(
        self,
        action: GetPrivateThreadListFiltersHookAction,
        request: HttpRequest,
    ) -> list[ThreadsFilter]: ...


class GetPrivateThreadListFiltersHook(
    FilterHook[
        GetPrivateThreadListFiltersHookAction,
        GetPrivateThreadListFiltersHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get available
    filters for the private thread list view.

    # Example

    The code below implements a custom filter function that includes a new filter:

    ```python
    from django.http import HttpRequest
    from misago.privatethreads.hooks import get_private_thread_list_filters_hook
    from misago.threads.filters import ThreadsFilter


    class CustomFilter(ThreadsFilter):
        name: str = "Custom filter"
        slug: str = "custom"

        def __callable__(self, queryset):
            if not self.request.user.is_authenticated:
                return queryset

            return queryset.filter(plugin_data__custom=True)


    @get_private_thread_list_filters_hook.append_filter
    def include_custom_filter(action, request: HttpRequest) -> list[ThreadsFilter]:
        filters = action(request)
        filters.append(CustomFilter(request))
        return filters
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetPrivateThreadListFiltersHookAction,
        request: HttpRequest,
    ) -> list[ThreadsFilter]:
        return super().__call__(action, request)


get_private_thread_list_filters_hook = GetPrivateThreadListFiltersHook(cache=False)
