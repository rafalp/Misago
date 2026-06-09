from typing import Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ..enums import ThreadPinned
from ..models import Thread


class CreateThreadHookAction(Protocol):
    """
    Misago function for creating an empty thread.

    This function does not create any posts for the thread, nor does it update
    the category the thread is created in. It is always used as a subroutine
    by moderation actions and other features that need to create a new thread
    and later populate it with content.

    After creating the thread, you should add posts to it, then use
    `synchronize_thread` to update the thread's statistics and `synchronize_category`
    to update the category's statistics.

    # Arguments

    ## `category: Category`

    A `Category` to create the thread in.

    ## `title: str`

    A `str` with the thread title.

    ## `pinned: ThreadPinned = ThreadPinned.NONE`

    Whether the thread should be pinned.

    Defaults to `ThreadPinned.None`.

    ## `is_locked: bool = False`

    Whether the thread should be locked.

    Defaults to `False`.

    ## `is_hidden: bool = False`

    Whether the thread should be hidden.

    Defaults to `False`.

    ## `commit: bool = True`

    Whether the thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `Thread` instance.
    """

    def __call__(
        self,
        category: Category,
        title: str,
        *,
        pinned: ThreadPinned = ThreadPinned.NONE,
        is_locked: bool = False,
        is_hidden: bool = False,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> Thread: ...


class CreateThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CreateThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `category: Category`

    A `Category` to create the thread in.

    ## `title: str`

    A `str` with the thread title.

    ## `pinned: ThreadPinned = ThreadPinned.NONE`

    Whether the thread should be pinned.

    Defaults to `ThreadPinned.None`.

    ## `is_locked: bool = False`

    Whether the thread should be locked.

    Defaults to `False`.

    ## `is_hidden: bool = False`

    Whether the thread should be hidden.

    Defaults to `False`.

    ## `commit: bool = True`

    Whether the thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `Thread` instance.
    """

    def __call__(
        self,
        action: CreateThreadHookAction,
        category: Category,
        title: str,
        *,
        pinned: ThreadPinned = ThreadPinned.NONE,
        is_locked: bool = False,
        is_hidden: bool = False,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> Thread: ...


class CreateThreadHook(
    FilterHook[
        CreateThreadHookAction,
        CreateThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    create an empty thread.

    # Example

    Record metadata about thread's creation:

    ```python
    from django.http import HttpRequest
    from django.utils import timezone
    from misago.categories.models import Category
    from misago.threads.enums import ThreadPinned
    from misago.threads.hooks import create_thread_hook
    from misago.threads.models import Thread


    @create_thread_hook.append_filter
    def record_thread_creator(
        action,
        category: Category,
        title: str,
        *,
        pinned: ThreadPinned = ThreadPinned.NONE,
        is_locked: bool = False,
        is_hidden: bool = False,
        commit: bool = True,
        request: HttpRequest | None = None,
    ):
        thread = action(
            category,
            title,
            pinned=pinned,
            is_locked=is_locked,
            is_hidden=is_hidden,
            commit=False,
            request=request,
        )

        thread.plugin_data["created_at"] = str(timezone.now())
        if request:
            thread.plugin_data["creator_id"] = request.user.id

        if commit:
            thread.save()

        return thread
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CreateThreadHookAction,
        category: Category,
        title: str,
        *,
        pinned: ThreadPinned = ThreadPinned.NONE,
        is_locked: bool = False,
        is_hidden: bool = False,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> Thread:
        return super().__call__(
            action,
            category,
            title,
            pinned=pinned,
            is_locked=is_locked,
            is_hidden=is_hidden,
            commit=commit,
            request=request,
        )


create_thread_hook = CreateThreadHook()
