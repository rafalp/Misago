from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..formsets.edit import EditPrivateThreadFormset


class GetEditPrivateThreadFormsetHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `EditPrivateThreadFormset`
    instance with forms for editing a private thread.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditPrivateThreadFormset` instance with forms for editing a private thread.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
    ) -> "EditPrivateThreadFormset": ...


class GetEditPrivateThreadFormsetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetEditPrivateThreadFormsetHookAction`

    A standard function that Misago uses to create a new `EditPrivateThreadFormset`
    instance with forms for editing a private thread.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditPrivateThreadFormset` instance with forms for editing a private thread.
    """

    def __call__(
        self,
        action: GetEditPrivateThreadFormsetHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditPrivateThreadFormset": ...


class GetEditPrivateThreadFormsetHook(
    FilterHook[
        GetEditPrivateThreadFormsetHookAction,
        GetEditPrivateThreadFormsetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `EditPrivateThreadFormset` instance with forms for editing a private thread.

    # Example

    The code below implements a custom filter function that adds custom form to
    the edit private thread formset:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import EditPrivateThreadFormset
    from misago.posting.hooks import get_edit_private_thread_formset_hook
    from misago.threads.models import Post

    from .forms import SelectUserForm


    @get_edit_private_thread_formset_hook.append_filter
    def add_select_user_form(
        action, request: HttpRequest, post: Post
    ) -> EditPrivateThreadFormset:
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
        action: GetEditPrivateThreadFormsetHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditPrivateThreadFormset":
        return super().__call__(action, request, post)


get_edit_private_thread_formset_hook = GetEditPrivateThreadFormsetHook()
