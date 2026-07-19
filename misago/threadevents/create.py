from typing import TYPE_CHECKING, Union

from django.db.models import Model
from django.http import HttpRequest
from django.utils import timezone

from ..categories.models import Category
from ..core.utils import slugify
from ..polls.models import Poll
from ..threads.models import Thread
from .enums import ThreadEventActionName
from .hooks import create_thread_event_hook
from .models import ThreadEvent

if TYPE_CHECKING:
    from ..users.models import User


def create_thread_event(
    thread: Thread,
    action: str,
    actor: Union["User", str, None] = None,
    *,
    context: str | None = None,
    context_object: Model | None = None,
    context_items: int | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event_hook(
        _create_thread_event_action,
        thread,
        action,
        actor,
        context=context,
        context_object=context_object,
        context_items=context_items,
        commit=commit,
        request=request,
    )


def _create_thread_event_action(
    thread: Thread,
    action: str,
    actor: Union["User", None, str] = None,
    *,
    context: str | None = None,
    context_object: Model | None = None,
    context_items: int | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    actor_id = None
    actor_name = None
    actor_slug = None
    context_type = None
    context_id = None

    if isinstance(actor, str):
        actor_name = actor
        actor_slug = slugify(actor)
    elif actor:
        actor_id = actor.id
        actor_name = actor.username
        actor_slug = actor.slug

    if context_object:
        context_type = ".".join(
            (
                context_object._meta.app_label,
                context_object._meta.model_name,
            )
        )
        context_id = context_object.id

    thread_event = ThreadEvent(
        category_id=thread.category_id,
        thread_id=thread.id,
        actor_id=actor_id,
        actor_name=actor_name,
        actor_slug=actor_slug,
        action=action,
        context=context,
        context_type=context_type,
        context_id=context_id,
        context_items=context_items,
        created_at=timezone.now(),
    )

    if commit:
        thread_event.save()

    return thread_event


def create_test_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    context: str | None = None,
    context_object: Model | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.TEST,
        actor,
        context=context,
        context_object=context_object,
        commit=commit,
        request=request,
    )


def create_pinned_everywhere_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.PINNED_EVERYWHERE,
        actor,
        commit=commit,
        request=request,
    )


def create_pinned_category_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.PINNED_CATEGORY,
        actor,
        commit=commit,
        request=request,
    )


def create_unpinned_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.UNPINNED,
        actor,
        commit=commit,
        request=request,
    )


def create_locked_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.LOCKED,
        actor,
        commit=commit,
        request=request,
    )


def create_unlocked_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.UNLOCKED,
        actor,
        commit=commit,
        request=request,
    )


def create_hidden_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.HIDDEN,
        actor,
        commit=commit,
        request=request,
    )


def create_unhidden_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.UNHIDDEN,
        actor,
        commit=commit,
        request=request,
    )


def create_approved_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.APPROVED,
        actor,
        commit=commit,
        request=request,
    )


def create_required_reply_approval_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.REQUIRED_REPLY_APPROVAL,
        actor,
        commit=commit,
        request=request,
    )


def create_removed_reply_approval_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.REMOVED_REPLY_APPROVAL,
        actor,
        commit=commit,
        request=request,
    )


def create_moved_thread_event(
    thread: Thread,
    old_category: Category,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.MOVED,
        actor,
        context=old_category.name,
        context_object=old_category,
        commit=commit,
        request=request,
    )


def create_merged_thread_event(
    thread: Thread,
    other_thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.MERGED,
        actor,
        context=other_thread.title,
        context_object=other_thread,
        commit=commit,
        request=request,
    )


def create_changed_title_thread_event(
    thread: Thread,
    old_title: str,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.CHANGED_TITLE,
        actor,
        context=old_title,
        commit=commit,
        request=request,
    )


def create_moved_posts_to_thread_event(
    thread: Thread,
    other_thread: Thread,
    posts: int,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.MOVED_POSTS_TO,
        actor,
        context=other_thread.title,
        context_object=other_thread,
        context_items=posts,
        commit=commit,
        request=request,
    )


def create_moved_posts_from_thread_event(
    thread: Thread,
    other_thread: Thread,
    posts: int,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.MOVED_POSTS_FROM,
        actor,
        context=other_thread.title,
        context_object=other_thread,
        context_items=posts,
        commit=commit,
        request=request,
    )


def create_split_posts_into_thread_event(
    thread: Thread,
    other_thread: Thread,
    posts: int | None = None,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.SPLIT_POSTS_INTO,
        actor,
        context=other_thread.title,
        context_object=other_thread,
        context_items=posts,
        commit=commit,
        request=request,
    )


def create_split_posts_from_thread_event(
    thread: Thread,
    other_thread: Thread,
    posts: int | None = None,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.SPLIT_POSTS_FROM,
        actor,
        context=other_thread.title,
        context_object=other_thread,
        context_items=posts,
        commit=commit,
        request=request,
    )


def create_deleted_posts_thread_event(
    thread: Thread,
    posts: int,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.DELETED_POSTS,
        actor,
        context_items=posts,
        commit=commit,
        request=request,
    )


def create_started_poll_thread_event(
    thread: Thread,
    poll: Poll,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.STARTED_POLL,
        actor,
        context=poll.question,
        commit=commit,
        request=request,
    )


def create_closed_poll_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.CLOSED_POLL,
        actor,
        commit=commit,
        request=request,
    )


def create_opened_poll_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.OPENED_POLL,
        actor,
        commit=commit,
        request=request,
    )


def create_deleted_poll_thread_event(
    thread: Thread,
    poll: Poll,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.DELETED_POLL,
        actor,
        context=poll.question,
        commit=commit,
        request=request,
    )


def create_took_ownership_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.TOOK_OWNERSHIP,
        actor,
        commit=commit,
        request=request,
    )


def create_joined_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.JOINED,
        actor,
        commit=commit,
        request=request,
    )


def create_added_member_thread_event(
    thread: Thread,
    member: "User",
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.ADDED_MEMBER,
        actor,
        context=member.username,
        context_object=member,
        commit=commit,
        request=request,
    )


def create_left_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.LEFT,
        actor,
        commit=commit,
        request=request,
    )


def create_removed_member_thread_event(
    thread: Thread,
    member: "User",
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.REMOVED_MEMBER,
        actor,
        context=member.username,
        context_object=member,
        commit=commit,
        request=request,
    )


def create_changed_owner_thread_event(
    thread: Thread,
    new_owner: "User",
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventActionName.CHANGED_OWNER,
        actor,
        context=new_owner.username,
        context_object=new_owner,
        commit=commit,
        request=request,
    )
