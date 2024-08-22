from typing import Protocol

from django.db.models import QuerySet
from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class GetThreadRepliesPagePostsQuerysetHookAction(Protocol):
    """
    A standard Misago function used to get a queryset used to get posts displayed
    on the thread replies page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    A `Thread` instance.

    # Return value

    An unfiltered `QuerySet` instance to use to get posts displayed on
    the thread replies page.
    """

    def __call__(self, request: HttpRequest, thread: Thread) -> QuerySet: ...


class GetThreadRepliesPagePostsQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadRepliesPagePostsQuerysetHookAction`

    A standard Misago function used to get a queryset used to get posts displayed
    on the thread replies page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    An unfiltered `QuerySet` instance to use to get posts displayed on
    the thread replies page.
    """

    def __call__(
        self,
        action: GetThreadRepliesPagePostsQuerysetHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> QuerySet: ...


class GetThreadRepliesPagePostsQuerysetHook(
    FilterHook[
        GetThreadRepliesPagePostsQuerysetHookAction,
        GetThreadRepliesPagePostsQuerysetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get a queryset
    with posts to display on the thread replies page.

    This hook should be used only to add new joins with `select_related`. To filter
    posts, use the `filter_thread_posts_queryset` hook instead.

    # Example

    The code below implements a custom filter function that joins plugin's table
    with `select_related`:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_thread_replies_page_posts_queryset_hook
    from misago.threads.models import Thread


    @get_thread_replies_page_posts_queryset_hook.append_filter
    def select_related_plugin_data(
        action, request: HttpRequest, thread: Thread
    ):
        queryset = action(request, thread)
        return queryset.select_related("plugin")
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadRepliesPagePostsQuerysetHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> dict:
        return super().__call__(action, request, thread)


get_thread_replies_page_posts_queryset_hook = GetThreadRepliesPagePostsQuerysetHook()
