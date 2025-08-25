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
    request: HttpRequest | None = None,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update_hook(
        _create_thread_update_action,
        thread,
        action,
        actor,
        request=request,
        context=context,
        context_object=context_object,
        is_hidden=is_hidden,
        plugin_data={},
    )


def _create_thread_update_action(
    thread: Thread,
    action: str,
    actor: Union["User", None, str] = None,
    *,
    request: HttpRequest | None = None,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
    plugin_data: dict,
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

    return ThreadUpdate.objects.create(
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
        plugin_data=plugin_data,
    )


def create_test_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    context: str | None = None,
    context_object: Model | None = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.TEST,
        actor,
        context=context,
        context_object=context_object,
        request=request,
        is_hidden=is_hidden,
    )


def create_approved_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.APPROVED,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_pinned_globally_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.PINNED_GLOBALLY,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_pinned_in_category_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.PINNED_IN_CATEGORY,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_unpinned_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.UNPINNED,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_locked_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.LOCKED,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_opened_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.OPENED,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_moved_thread_update(
    thread: Thread,
    old_category: Category,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.MOVED,
        actor,
        request=request,
        context=old_category.name,
        context_object=old_category,
        is_hidden=is_hidden,
    )


def create_merged_thread_update(
    thread: Thread,
    other_thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.MERGED,
        actor,
        request=request,
        context=other_thread.title,
        context_object=other_thread,
        is_hidden=is_hidden,
    )


def create_split_thread_update(
    thread: Thread,
    other_thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.SPLIT,
        actor,
        request=request,
        context=other_thread.title,
        context_object=other_thread,
        is_hidden=is_hidden,
    )


def create_hid_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.HID,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_unhid_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.UNHID,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_changed_title_thread_update(
    thread: Thread,
    old_title: str,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.CHANGED_TITLE,
        actor,
        request=request,
        context=old_title,
        is_hidden=is_hidden,
    )


def create_started_poll_thread_update(
    thread: Thread,
    poll: Poll,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.STARTED_POLL,
        actor,
        request=request,
        context=poll.question,
        is_hidden=is_hidden,
    )


def create_closed_poll_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.CLOSED_POLL,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_opened_poll_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.OPENED_POLL,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_deleted_poll_thread_update(
    thread: Thread,
    poll: Poll,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.DELETED_POLL,
        actor,
        request=request,
        context=poll.question,
        is_hidden=is_hidden,
    )


def create_took_ownership_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.TOOK_OWNERSHIP,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_joined_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.JOINED,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_added_member_thread_update(
    thread: Thread,
    member: "User",
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.ADDED_MEMBER,
        actor,
        request=request,
        context=member.username,
        context_object=member,
        is_hidden=is_hidden,
    )


def create_left_thread_update(
    thread: Thread,
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.LEFT,
        actor,
        request=request,
        is_hidden=is_hidden,
    )


def create_removed_member_thread_update(
    thread: Thread,
    member: "User",
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.REMOVED_MEMBER,
        actor,
        request=request,
        context=member.username,
        context_object=member,
        is_hidden=is_hidden,
    )


def create_changed_owner_thread_update(
    thread: Thread,
    new_owner: "User",
    actor: Union["User", str, None] = None,
    request: HttpRequest | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update(
        thread,
        ThreadUpdateActionName.CHANGED_OWNER,
        actor,
        request=request,
        context=new_owner.username,
        context_object=new_owner,
        is_hidden=is_hidden,
    )
