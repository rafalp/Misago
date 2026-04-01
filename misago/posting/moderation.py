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


def require_thread_moderation(state: ThreadStartState) -> bool:
    return False


def require_private_thread_moderation(state: PrivateThreadStartState) -> bool:
    return False


def require_thread_reply_moderation(state: ThreadReplyState) -> bool:
    return False


def require_private_thread_reply_moderation(state: PrivateThreadReplyState) -> bool:
    return False


def require_thread_edit_moderation(state: ThreadPostEditState) -> bool:
    return False


def require_private_thread_edit_moderation(state: PrivateThreadPostEditState) -> bool:
    return False
