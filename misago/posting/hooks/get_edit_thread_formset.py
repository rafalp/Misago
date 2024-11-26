from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..formsets.edit import EditThreadFormset


class GetEditThreadFormsetHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `EditThreadFormset`
    instance with forms for editing a thread.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditThreadFormset` instance with forms for editing a thread.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
    ) -> "EditThreadFormset": ...


class GetEditThreadFormsetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetEditThreadFormsetHookAction`

    A standard function that Misago uses to create a new `EditThreadFormset`
    instance with forms for editing a thread.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditThreadFormset` instance with forms for editing a thread.
    """

    def __call__(
        self,
        action: GetEditThreadFormsetHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditThreadFormset": ...


class GetEditThreadFormsetHook(
    FilterHook[
        GetEditThreadFormsetHookAction,
        GetEditThreadFormsetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `EditThreadFormset` instance with forms for editing a thread.

    # Example

    The code below implements a custom filter function that adds custom form to
    the edit thread formset:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import EditThreadFormset
    from misago.posting.hooks import get_edit_thread_formset_hook
    from misago.threads.models import Post

    from .forms import SelectUserForm


    @get_edit_thread_formset_hook.append_filter
    def add_select_user_form(
        action, request: HttpRequest, post: Post
    ) -> EditThreadFormset:
        formset = action(request, post)

        if request.method == "POST":
            form = SelectUserForm(request.POST, prefix="select-user")
        else:
            form = SelectUserForm(prefix="select-user")

        formset.add_form(form, before="posting-post")
        return formset
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetEditThreadFormsetHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditThreadFormset":
        return super().__call__(action, request, post)


get_edit_thread_formset_hook = GetEditThreadFormsetHook()
