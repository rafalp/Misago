from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class GetThreadDetailViewModerationResultDataHookAction(Protocol):
    """
    Misago function used to get the template context data
    for the moderation result in the thread detail view.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    A `Thread` instance.

    # Return value

    A Python `dict` with context data to use to `render` the moderation result.
    """

    def __call__(self, request: HttpRequest, thread: Thread) -> dict: ...


class GetThreadDetailViewModerationResultDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadDetailViewModerationResultDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    A `Thread` instance.

    # Return value

    A Python `dict` with context data to use to `render` the moderation result.
    """

    def __call__(
        self,
        action: GetThreadDetailViewModerationResultDataHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> dict: ...


class GetThreadDetailViewModerationResultDataHook(
    FilterHook[
        GetThreadDetailViewModerationResultDataHookAction,
        GetThreadDetailViewModerationResultDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the template context data for the moderation result in the thread detail view.

    # Example

    The code below implements a custom filter function that injects a template
    component into the thread moderation result:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import (
        get_thread_detail_view_moderation_result_data_hook
    )
    from misago.threads.models import Thread


    @get_thread_detail_view_moderation_result_data_hook.append_filter
    def include_plugin_component(
        action, request: HttpRequest, thread: Thread
    ) -> dict:
        context = action(request, thread)
        context["extra_components"].append({
            "id": "plugin_component",
            "template_name": "myplugin/component.html"
        })

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadDetailViewModerationResultDataHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> dict:
        return super().__call__(action, request, thread)


get_thread_detail_view_moderation_result_data_hook = (
    GetThreadDetailViewModerationResultDataHook(cache=False)
)
