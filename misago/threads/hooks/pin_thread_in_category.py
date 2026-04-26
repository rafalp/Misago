from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class PinThreadInCategoryHookAction(Protocol):
    """
    Misago function for pinning a thread in a category.

    # Arguments

    ## `thread: Thread`

    A `Thread` to pin in a category.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was pinned, `False` otherwise.
    """

    def __call__(
        self,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class PinThreadInCategoryHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: PinThreadInCategoryHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    A `Thread` to pin in a category.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was pinned, `False` otherwise.
    """

    def __call__(
        self,
        action: PinThreadInCategoryHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class PinThreadInCategoryHook(
    FilterHook[
        PinThreadInCategoryHookAction,
        PinThreadInCategoryHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    pin a thread in a category.

    # Example

    Register user who pinned the thread.

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import pin_thread_in_category_hook
    from misago.threads.models import Thread


    @pin_thread_in_category_hook.append_filter
    def register_user_that_pinned_thread_in_category(
        action,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        if not action(thread, commit=False, request=request):
            return False

        if request:
            thread.plugin_data["pinned_in_category_by"] = request.user.id

        if commit:
            thread.save()

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: PinThreadInCategoryHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        return super().__call__(
            action,
            thread,
            commit,
            request,
        )


pin_thread_in_category_hook = PinThreadInCategoryHook()
