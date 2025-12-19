from typing import Iterable, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ..models import Thread


class MoveThreadsHookAction(Protocol):
    """
    Misago function for moving threads to a new category.

    # Arguments

    ## `threads: Iterable[Thread]`

    The iterable of threads to move.

    ## `new_category: category`

    A `Category` to move threads to.

    ## `commit: bool`

    Whether the threads' `category` field should be updated directly in
    the database using `QuerySet.update()`.

    When True, only the category column is saved. If other fields need updating,
    set this to False and handle updates manually.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        threads: Iterable[Thread],
        new_category: Category,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class MoveThreadsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: MoveThreadsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `threads: Iterable[Thread]`

    The iterable of threads to move.

    ## `new_category: category`

    A `Category` to move threads to.

    ## `commit: bool`

    Whether the threads' `category` field should be updated directly in
    the database using `QuerySet.update()`.

    When True, only the category column is saved. If other fields need updating,
    set this to False and handle updates manually.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: MoveThreadsHookAction,
        threads: Iterable[Thread],
        new_category: Category,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class MoveThreadsHook(
    FilterHook[
        MoveThreadsHookAction,
        MoveThreadsHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    move threads to a new category.

    # Example

    Update `category` attribute on plugin model:

    ```python
    from typing import Iterable

    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.threads.hooks import move_threads_hook
    from misago.threads.models import Thread

    from .models import PluginModel


    @move_threads_hook.append_filter
    def move_plugin_models_to_new_category(
        action,
        threads: Iterable[Thread],
        new_category: Category,
        commit: bool = True,
        request: HttpRequest | None = None,
    ):
        action(thread, data, commit, request)

        PluginModel.objects.filter(
            thread__in=threads
        ).update(category=new_category)
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: MoveThreadsHookAction,
        threads: Iterable[Thread],
        new_category: Category,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(
            action,
            threads,
            new_category,
            commit,
            request,
        )


move_threads_hook = MoveThreadsHook()
