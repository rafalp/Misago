from typing import TYPE_CHECKING, Union

from django.db.models import Model
from django.http import HttpRequest
from django.utils import timezone

from ..categories.models import Category
from ..polls.models import Poll
from ..threads.models import Thread
from .enums import ThreadUpdateActionName
from .hooks import create_thread_update_hook
from .models import ThreadUpdate

if TYPE_CHECKING:
    from ..users.models import User


def create_thread_update(
    thread: Thread,
    action: str,
    actor: Union["User", str, None] = None,
    *,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update_hook(
        _create_thread_update_action,
        thread,
        action,
        actor,
        context=context,
        context_object=context_object,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def _create_thread_update_action(
    thread: Thread,
    action: str,
    actor: Union["User", None, str] = None,
    *,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    actor_id = None
    actor_name = None
    context_type = None
    context_id = None

    if isinstance(actor, str):
        actor_name = actor
    elif actor:
        actor_id = actor.id
        actor_name = actor.username

    if context_object:
        context_type = ".".join(
            (
                context_object._meta.app_label,
                context_object._meta.model_name,
            )
        )
        context_id = context_object.id

    thread_update = ThreadUpdate(
        category_id=thread.category_id,
        thread_id=thread.id,
        actor_id=actor_id,
        actor_name=actor_name,
        action=action,
        context=context,
        context_type=context_type,
        context_id=context_id,
        created_at=timezone.now(),
        is_hidden=is_hidden,
    )

    if commit:
        thread_update.save()

    return thread_update


def create_test_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.TEST,
        actor,
        context=context,
        context_object=context_object,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_approved_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.APPROVED,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_pinned_globally_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.PINNED_GLOBALLY,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_pinned_in_category_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.PINNED_IN_CATEGORY,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_unpinned_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.UNPINNED,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_locked_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.LOCKED,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_opened_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.OPENED,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_moved_thread_update(
    thread: Thread,
    old_category: Category,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.MOVED,
        actor,
        context=old_category.name,
        context_object=old_category,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_merged_thread_update(
    thread: Thread,
    other_thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.MERGED,
        actor,
        context=other_thread.title,
        context_object=other_thread,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_split_thread_update(
    thread: Thread,
    other_thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.SPLIT,
        actor,
        context=other_thread.title,
        context_object=other_thread,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_hid_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.HID,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_unhid_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.UNHID,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_changed_title_thread_update(
    thread: Thread,
    old_title: str,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.CHANGED_TITLE,
        actor,
        context=old_title,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_started_poll_thread_update(
    thread: Thread,
    poll: Poll,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.STARTED_POLL,
        actor,
        context=poll.question,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_closed_poll_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.CLOSED_POLL,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_opened_poll_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.OPENED_POLL,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_deleted_poll_thread_update(
    thread: Thread,
    poll: Poll,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.DELETED_POLL,
        actor,
        context=poll.question,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_took_ownership_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.TOOK_OWNERSHIP,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_joined_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.JOINED,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_added_member_thread_update(
    thread: Thread,
    member: "User",
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.ADDED_MEMBER,
        actor,
        context=member.username,
        context_object=member,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_left_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.LEFT,
        actor,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_removed_member_thread_update(
    thread: Thread,
    member: "User",
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.REMOVED_MEMBER,
        actor,
        context=member.username,
        context_object=member,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def create_changed_owner_thread_update(
    thread: Thread,
    new_owner: "User",
    actor: Union["User", str, None] = None,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.CHANGED_OWNER,
        actor,
        context=new_owner.username,
        context_object=new_owner,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )
