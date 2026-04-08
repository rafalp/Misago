from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.reply import PrivateThreadReplyState


class RequirePrivateThreadReplyApprovalHookAction(Protocol):
    """
    A standard function that Misago uses to check if
    a new private thread reply should require moderator approval.

    # Arguments

    ## `state: PrivateThreadReplyState`

    A `PrivateThreadReplyState` instance containing data used to create a new private thread reply.

    # Return value

    `True` if the new private thread reply should require moderator approval, or `False` otherwise.
    """

    def __call__(
        self,
        state: "PrivateThreadReplyState",
    ) -> bool: ...


class RequirePrivateThreadReplyApprovalHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: RequirePrivateThreadReplyApprovalHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `state: PrivateThreadReplyState`

    A `PrivateThreadReplyState` instance containing data used to create a new private thread reply.

    # Return value

    `True` if the new private thread reply should require moderator approval, or `False` otherwise.
    """

    def __call__(
        self,
        action: RequirePrivateThreadReplyApprovalHookAction,
        state: "PrivateThreadReplyState",
    ) -> bool: ...


class RequirePrivateThreadReplyApprovalHook(
    FilterHook[
        RequirePrivateThreadReplyApprovalHookAction,
        RequirePrivateThreadReplyApprovalHookFilter,
    ]
):
    """
    This hook wraps the standard function Misago uses to check if
    a new private thread reply should require moderator approval.

    # Example

    The code below implements a custom filter function that flags a new private thread
    reply for moderator approval if it contains links and the user recently joined.

    ```python
    from django.utils import timezone
    from misago.posting.hooks import require_private_thread_reply_approval_hook
    from misago.posting.state import PrivateThreadReplyState


    @require_private_thread_reply_approval_hook.append_filter
    def require_private_thread_reply_approval(
        action, state: PrivateThreadReplyState
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
        action: RequirePrivateThreadReplyApprovalHookAction,
        state: "PrivateThreadReplyState",
    ) -> bool:
        return super().__call__(action, state)


require_private_thread_reply_approval_hook = RequirePrivateThreadReplyApprovalHook()
