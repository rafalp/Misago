from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class RequireThreadReplyApprovalHookAction(Protocol):
    """
    Misago function for making all new replies in a thread require approval.

    # Arguments

    ## `thread: Thread`

    A `Thread` to require reply approval for.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was updated, `False` otherwise.
    """

    def __call__(
        self,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class RequireThreadReplyApprovalHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RequireThreadReplyApprovalHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    Misago function for making all new replies in a thread require approval.

    # Arguments

    ## `thread: Thread`

    A `Thread` to require reply approval for.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was updated, `False` otherwise.
    """

    def __call__(
        self,
        action: RequireThreadReplyApprovalHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class RequireThreadReplyApprovalHook(
    FilterHook[
        RequireThreadReplyApprovalHookAction,
        RequireThreadReplyApprovalHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to make all
    new replies in a thread require approval

    # Example

    Register user who enabled the approval of new replies in a thread.

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import require_thread_reply_approval_hook
    from misago.threads.models import Thread


    @require_thread_reply_approval_hook.append_filter
    def register_user_that_set_require_thread_reply_approval(
        action,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        if not action(thread, commit=False, request=request):
            return False

        if request:
            thread.plugin_data["set_require_reply_approval"] = request.user.id

        if commit:
            thread.save()

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: RequireThreadReplyApprovalHookAction,
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


require_thread_reply_approval_hook = RequireThreadReplyApprovalHook()
