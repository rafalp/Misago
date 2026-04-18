from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.reply import ThreadReplyState


class RequireThreadReplyApprovalHookAction(Protocol):
    """
    A standard function that Misago uses to check if
    a new thread should require moderator approval.

    # Arguments

    ## `state: ThreadReplyState`

    A `ThreadReplyState` instance containing data used to create a new thread reply.

    # Return value

    `True` if the new thread reply should require moderator approval, or `False` otherwise.
    """

    def __call__(
        self,
        state: "ThreadReplyState",
    ) -> bool: ...


class RequireThreadReplyApprovalHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RequireThreadReplyApprovalHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `state: ThreadReplyState`

    A `ThreadReplyState` instance containing data used to create a new thread reply.

    # Return value

    `True` if the new thread reply should require moderator approval, or `False` otherwise.
    """

    def __call__(
        self,
        action: RequireThreadReplyApprovalHookAction,
        state: "ThreadReplyState",
    ) -> bool: ...


class RequireThreadReplyApprovalHook(
    FilterHook[
        RequireThreadReplyApprovalHookAction, RequireThreadReplyApprovalHookFilter
    ]
):
    """
    This hook wraps the standard function Misago uses to check if
    a new thread reply should require moderator approval.

    # Example

    The code below implements a custom filter function that flags a new thread
    reply for moderator approval if it contains links and the user recently joined.

    ```python
    from django.utils import timezone
    from misago.posting.hooks import require_thread_reply_approval_hook
    from misago.posting.state import ThreadReplyState


    @require_thread_reply_approval_hook.append_filter
    def require_thread_reply_approval(
        action, state: ThreadReplyState
    ) -> bool:
        if action(state):
            return True

        if state.user_permissions.bypass_content_approval:
            return False

        return bool(
            (timezone.now() - state.user.joined_on).total_seconds() < 72 * 3600
            and "<a" in state.post.parsed
        )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: RequireThreadReplyApprovalHookAction,
        state: "ThreadReplyState",
    ) -> bool:
        return super().__call__(action, state)


require_thread_reply_approval_hook = RequireThreadReplyApprovalHook()
