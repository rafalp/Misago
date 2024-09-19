from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..forms.start import StartThreadFormset


class GetStartPrivateThreadPageFormsetHookAction(Protocol):
    """
    A standard function that Misago uses to create a new
    `StartThreadFormset` instance for the start a new private thread page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartThreadFormset` instance with forms to display
    on the start a new private thread page.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
    ) -> "StartThreadFormset": ...


class GetStartPrivateThreadPageFormsetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetStartPrivateThreadPageFormsetHookAction`

    A standard function that Misago uses to create a new
    `StartThreadFormset` instance for the start a new private thread page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartThreadFormset` instance with forms to display
    on the start a new private thread page.
    """

    def __call__(
        self,
        action: GetStartPrivateThreadPageFormsetHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartThreadFormset": ...


class GetStartPrivateThreadPageFormsetHook(
    FilterHook[
        GetStartPrivateThreadPageFormsetHookAction,
        GetStartPrivateThreadPageFormsetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `StartThreadFormset` instance for the start a new private thread page.

    # Example

    The code below implements a custom filter function that adds custom form to
    the start a new private thread page:

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.posting.hooks import get_start_private_thread_page_formset_hook
    from misago.posting.forms.start import StartThreadFormset

    from .forms import SelectUserForm


    @get_start_private_thread_page_formset_hook.append_filter
    def add_select_user_form(
        action, request: HttpRequest, category: Category
    ) -> StartThreadFormset:
        formset = action(request, category)

        if request.method == "POST":
            form = SelectUserForm(request.POST, prefix="select-user")
        else:
            form = SelectUserForm(prefix="select-user")

        formset.add_form(form)
        return formset
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetStartPrivateThreadPageFormsetHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartThreadFormset":
        return super().__call__(action, request, category)


get_start_private_thread_page_formset_hook = GetStartPrivateThreadPageFormsetHook(
    cache=False
)
