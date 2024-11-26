from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..formsets.start import StartThreadFormset


class GetStartThreadFormsetHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `StartThreadFormset`
    instance with forms for posting a new thread.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartThreadFormset` instance with forms for posting a new thread.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
    ) -> "StartThreadFormset": ...


class GetStartThreadFormsetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetStartThreadFormsetHookAction`

    A standard function that Misago uses to create a new `StartThreadFormset`
    instance with forms for posting a new thread.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartThreadFormset` instance with forms for posting a new thread.
    """

    def __call__(
        self,
        action: GetStartThreadFormsetHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartThreadFormset": ...


class GetStartThreadFormsetHook(
    FilterHook[
        GetStartThreadFormsetHookAction,
        GetStartThreadFormsetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `StartThreadFormset` instance with forms for posting a new thread.

    # Example

    The code below implements a custom filter function that adds custom form to
    the start new thread formset:

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.posting.formsets import StartThreadFormset
    from misago.posting.hooks import get_start_thread_formset_hook

    from .forms import SelectUserForm


    @get_start_thread_formset_hook.append_filter
    def add_select_user_form(
        action, request: HttpRequest, category: Category
    ) -> StartThreadFormset:
        formset = action(request, category)

        if request.method == "POST":
            form = SelectUserForm(request.POST, prefix="select-user")
        else:
            form = SelectUserForm(prefix="select-user")

        formset.add_form(form, before="posting-title")
        return formset
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetStartThreadFormsetHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartThreadFormset":
        return super().__call__(action, request, category)


get_start_thread_formset_hook = GetStartThreadFormsetHook()
