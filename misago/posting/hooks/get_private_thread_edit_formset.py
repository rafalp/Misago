from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..formsets.edit import PrivateThreadEditFormset


class GetPrivateThreadEditFormsetHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `PrivateThreadEditFormset`
    instance with forms for editing a private thread.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `PrivateThreadEditFormset` instance with forms for editing a private thread.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
    ) -> "PrivateThreadEditFormset": ...


class GetPrivateThreadEditFormsetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadEditFormsetHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `PrivateThreadEditFormset` instance with forms for editing a private thread.
    """

    def __call__(
        self,
        action: GetPrivateThreadEditFormsetHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "PrivateThreadEditFormset": ...


class GetPrivateThreadEditFormsetHook(
    FilterHook[
        GetPrivateThreadEditFormsetHookAction,
        GetPrivateThreadEditFormsetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `PrivateThreadEditFormset` instance with forms for editing a private thread.

    # Example

    The code below implements a custom filter function that adds custom form to
    the edit private thread formset:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import PrivateThreadEditFormset
    from misago.posting.hooks import get_private_thread_edit_formset_hook
    from misago.threads.models import Post

    from .forms import SelectUserForm


    @get_private_thread_edit_formset_hook.append_filter
    def add_select_user_form(
        action, request: HttpRequest, post: Post
    ) -> PrivateThreadEditFormset:
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
        action: GetPrivateThreadEditFormsetHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "PrivateThreadEditFormset":
        return super().__call__(action, request, post)


get_private_thread_edit_formset_hook = GetPrivateThreadEditFormsetHook()
