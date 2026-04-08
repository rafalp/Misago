from typing import TYPE_CHECKING

from .hooks import (
    require_private_thread_approval_hook,
    require_private_thread_reply_approval_hook,
    require_thread_approval_hook,
    require_thread_reply_approval_hook,
)

if TYPE_CHECKING:
    from .state import (
        PrivateThreadReplyState,
        PrivateThreadStartState,
        ThreadReplyState,
        ThreadStartState,
    )


def require_thread_approval(state: "ThreadStartState") -> bool:
    return require_thread_approval_hook(_require_thread_approval_action, state)


def _require_thread_approval_action(state: "ThreadStartState") -> bool:
    if state.user.require_content_approval:
        return True

    if state.user_permissions.bypass_content_approval:
        return False

    if state.category.require_threads_approval:
        return True

    return False


def require_private_thread_approval(state: "PrivateThreadStartState") -> bool:
    return require_private_thread_approval_hook(
        _require_private_thread_approval_action, state
    )


def _require_private_thread_approval_action(state: "PrivateThreadStartState") -> bool:
    return state.user.require_content_approval


def require_thread_reply_approval(state: "ThreadReplyState") -> bool:
    return require_thread_reply_approval_hook(
        _require_thread_reply_approval_action, state
    )


def _require_thread_reply_approval_action(state: "ThreadReplyState") -> bool:
    if state.user.require_content_approval:
        return True

    if state.user_permissions.bypass_content_approval:
        return False

    if state.category.require_replies_approval:
        return True

    return False


def require_private_thread_reply_approval(state: "PrivateThreadReplyState") -> bool:
    return require_private_thread_reply_approval_hook(
        _require_private_thread_reply_approval_action, state
    )


def _require_private_thread_reply_approval_action(
    state: "PrivateThreadReplyState",
) -> bool:
    return state.user.require_content_approval
