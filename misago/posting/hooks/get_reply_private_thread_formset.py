from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..formsets.reply import ReplyPrivateThreadFormset


class GetReplyPrivateThreadFormsetHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `ReplyPrivateThreadFormset`
    instance with forms for posting a new private thread reply.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    # Return value

    A `ReplyPrivateThreadFormset` instance with forms for posting
    a new private thread reply.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> "ReplyPrivateThreadFormset": ...


class GetReplyPrivateThreadFormsetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetReplyPrivateThreadFormsetHookAction`

    A standard function that Misago uses to create a new `ReplyPrivateThreadFormset`
    instance with forms for posting a new private thread reply.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    # Return value

    A `ReplyPrivateThreadFormset` instance with forms for posting
    a new private thread reply.
    """

    def __call__(
        self,
        action: GetReplyPrivateThreadFormsetHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> "ReplyPrivateThreadFormset": ...


class GetReplyPrivateThreadFormsetHook(
    FilterHook[
        GetReplyPrivateThreadFormsetHookAction,
        GetReplyPrivateThreadFormsetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `ReplyPrivateThreadFormset` instance with forms for posting a new private
    thread reply.

    # Example

    The code below implements a custom filter function that adds custom form to
    the new private thread reply formset:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import ReplyPrivateThreadFormset
    from misago.posting.hooks import get_reply_private_thread_formset_hook
    from misago.threads.models import Thread

    from .forms import SelectUserForm


    @get_reply_private_thread_formset_hook.append_filter
    def add_select_user_form(
        action, request: HttpRequest, thread: Thread
    ) -> ReplyPrivateThreadFormset:
        formset = action(request, thread)

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
        action: GetReplyPrivateThreadFormsetHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> "ReplyPrivateThreadFormset":
        return super().__call__(action, request, thread)


get_reply_private_thread_formset_hook = GetReplyPrivateThreadFormsetHook()
