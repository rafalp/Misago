from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..formsets.edit import PrivateThreadPostEditFormset


class GetPrivateThreadPostEditFormsetHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `PrivateThreadPostEditFormset`
    instance with forms for editing a private thread post.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `PrivateThreadPostEditFormset` instance with forms for editing
    a private thread post.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
    ) -> "PrivateThreadPostEditFormset": ...


class GetPrivateThreadPostEditFormsetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadPostEditFormsetHookAction`

    The next function registered in this hook, either a custom function or
    Misago’s default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `PrivateThreadPostEditFormset` instance with forms for editing
    a private thread post.
    """

    def __call__(
        self,
        action: GetPrivateThreadPostEditFormsetHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "PrivateThreadPostEditFormset": ...


class GetPrivateThreadPostEditFormsetHook(
    FilterHook[
        GetPrivateThreadPostEditFormsetHookAction,
        GetPrivateThreadPostEditFormsetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `PrivateThreadPostEditFormset` instance with forms for editing
    a private thread post.

    # Example

    The code below implements a custom filter function that adds custom form to
    the edit private thread post formset:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import PrivateThreadPostEditFormset
    from misago.posting.hooks import get_private_thread_post_edit_formset_hook
    from misago.threads.models import Post

    from .forms import SelectUserForm


    @get_private_thread_post_edit_formset_hook.append_filter
    def add_select_user_form(
        action, request: HttpRequest, post: Post
    ) -> PrivateThreadPostEditFormset:
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
        action: GetPrivateThreadPostEditFormsetHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "PrivateThreadPostEditFormset":
        return super().__call__(action, request, post)


get_private_thread_post_edit_formset_hook = GetPrivateThreadPostEditFormsetHook()
