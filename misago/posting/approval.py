from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .state import (
        PrivateThreadPostEditState,
        PrivateThreadReplyState,
        PrivateThreadStartState,
        ThreadPostEditState,
        ThreadReplyState,
        ThreadStartState,
    )


def require_thread_approval(state: "ThreadStartState") -> bool:
    if state.user_permissions.bypass_content_approval:
        return False

    return state.category.require_threads_approval


def require_private_thread_approval(state: "PrivateThreadStartState") -> bool:
    return False


def require_thread_reply_approval(state: "ThreadReplyState") -> bool:
    if state.user_permissions.bypass_content_approval:
        return False

    return state.category.require_replies_approval


def require_private_thread_reply_approval(state: "PrivateThreadReplyState") -> bool:
    return False


def require_thread_post_edit_approval(state: "ThreadPostEditState") -> bool:
    if state.user_permissions.bypass_content_approval:
        return False

    return state.category.require_edits_approval


def require_private_thread_post_edit_approval(
    state: "PrivateThreadPostEditState",
) -> bool:
    return False
