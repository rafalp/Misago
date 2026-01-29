from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..formsets.reply import PrivateThreadReplyFormset


class GetPrivateThreadReplyFormsetHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `PrivateThreadReplyFormset`
    instance with forms for posting a new private thread reply.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    # Return value

    A `PrivateThreadReplyFormset` instance with forms for posting
    a new private thread reply.
    """

    def __call__(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> "PrivateThreadReplyFormset": ...


class GetPrivateThreadReplyFormsetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetPrivateThreadReplyFormsetHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `thread: Thread`

    The `Thread` instance.

    # Return value

    A `PrivateThreadReplyFormset` instance with forms for posting
    a new private thread reply.
    """

    def __call__(
        self,
        action: GetPrivateThreadReplyFormsetHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> "PrivateThreadReplyFormset": ...


class GetPrivateThreadReplyFormsetHook(
    FilterHook[
        GetPrivateThreadReplyFormsetHookAction,
        GetPrivateThreadReplyFormsetHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `PrivateThreadReplyFormset` instance with forms for posting a new private
    thread reply.

    # Example

    The code below implements a custom filter function that adds custom form to
    the new private thread reply formset:

    ```python
    from django.http import HttpRequest
    from misago.posting.formsets import PrivateThreadReplyFormset
    from misago.posting.hooks import get_private_thread_reply_formset_hook
    from misago.threads.models import Thread

    from .forms import SelectUserForm


    @get_private_thread_reply_formset_hook.append_filter
    def add_select_user_form(
        action, request: HttpRequest, thread: Thread
    ) -> PrivateThreadReplyFormset:
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
        action: GetPrivateThreadReplyFormsetHookAction,
        request: HttpRequest,
        thread: Thread,
    ) -> "PrivateThreadReplyFormset":
        return super().__call__(action, request, thread)


get_private_thread_reply_formset_hook = GetPrivateThreadReplyFormsetHook()
