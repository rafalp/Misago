from typing import Protocol

from django.db.models import QuerySet
from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ..models import Thread


class GetThreadUrlHookAction(Protocol):
    """
    A standard Misago function used to retrieve a thread URL based on its category type.

    # Arguments

    ## `thread: Thread`

    A `Thread` instance.

    ## `category: Category`

    A `Category` instance, if `thread.category` was not populated using `select_related`
    or `prefetch_related`. Otherwise it's `None` and `thread.category`
    should be used instead.

    # Return value

    An `str` with URL.
    """

    def __call__(
        self, thread: Thread, category: Category | None = None
    ) -> QuerySet: ...


class GetThreadUrlHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadUrlHookAction`

    A standard Misago function used to retrieve a thread URL based on its category type.

    See the [action](#action) section for details.

    ## `thread: Thread`

    A `Thread` instance.

    ## `category: Category`

    A `Category` instance, if `thread.category` was not populated using `select_related`
    or `prefetch_related`. Otherwise it's `None` and `thread.category`
    should be used instead.

    # Return value

    An `str` with URL.
    """

    def __call__(
        self,
        action: GetThreadUrlHookAction,
        thread: Thread,
        category: Category | None = None,
    ) -> QuerySet: ...


class GetThreadUrlHook(
    FilterHook[
        GetThreadUrlHookAction,
        GetThreadUrlHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago useds to retrieve
    a thread URL based on its category type.

    # Example

    The code below implements a custom filter function that returns thread's URL
    for custom category type:

    ```python
    from django.urls import reverse
    from misago.categories.models import Category
    from misago.threads.hooks import get_thread_url_hook
    from misago.threads.models import Thread


    @get_thread_url_hook.append_filter
    def get_thread_blog_url(
        action, thread: Thread, category: Category | None = None
    ):
        if (category or thread.category).plugin_data.get("is_blog"):
            return reverse(
                "blog", kwargs={"id": thread.id, "slug": thread.slug}
            )

        return = action(thread, category)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadUrlHookAction,
        thread: Thread,
        category: Category | None = None,
    ) -> dict:
        return super().__call__(action, thread, category)


get_thread_url_hook = GetThreadUrlHook()
