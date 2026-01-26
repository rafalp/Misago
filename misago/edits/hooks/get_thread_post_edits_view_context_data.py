from typing import Protocol

from django.core.paginator import Page
from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post


class GetThreadPostEditsViewContextDataHookAction(Protocol):
    """
    Misago function used to get the template context data
    for the thread post edits page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    A `Post` instance whose edits are being displayed.

    ## `page: Page`

    A `Page` instance that may or may not include a `PostEdit` instance in
    its `object_list` attribute.

    # Returns

    A Python `dict` with context data to use to `render` the post edits page.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
        page: Page,
    ) -> dict: ...


class GetThreadPostEditsViewContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadPostEditsViewContextDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    A `Post` instance whose edits are being displayed.

    ## `page: Page`

    A `Page` instance that may or may not include a `PostEdit` instance in
    its `object_list` attribute.

    # Returns

    A Python `dict` with context data to use to `render` the post edits page.
    """

    def __call__(
        self,
        action: GetThreadPostEditsViewContextDataHookAction,
        request: HttpRequest,
        post: Post,
        page: Page,
    ) -> dict: ...


class GetThreadPostEditsViewContextDataHook(
    FilterHook[
        GetThreadPostEditsViewContextDataHookAction,
        GetThreadPostEditsViewContextDataHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to get the template context
    data for the thread post edits page.

    # Example

    The code below implements a custom filter function that displays a template
    with the editor’s IP address in the `post_edit_diff_plugins_top` plugin outlet.

    ```python
    from django.core.paginator import Page
    from django.http import HttpRequest
    from misago.edits.hooks import get_thread_post_edits_view_context_data_hook
    from misago.edits.models import PostEdit
    from misago.threads.models import Post

    @get_thread_post_edits_view_context_data_hook.append_filter
    def set_thread_post_edits_view_editor_ip_address(
        action,
        request: HttpRequest,
        post: Post,
        page: Page,
    ) -> dict:
        context = action(request, post, page)

        if not page.object_list:
            return context

        post_edit = page.object_list[0]
        context["post_edit_diff_plugins_top"].append({
            "template_name": "my_plugin/post_edit_diff.html",
            "user_ip": post_edit.plugin_data.get("user_ip"),
        })

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadPostEditsViewContextDataHookAction,
        request: HttpRequest,
        post: Post,
        page: Page,
    ) -> dict:
        return super().__call__(action, request, post, page)


get_thread_post_edits_view_context_data_hook = GetThreadPostEditsViewContextDataHook(
    cache=False
)
