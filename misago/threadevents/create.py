from typing import TYPE_CHECKING, Union

from django.db.models import Model
from django.http import HttpRequest
from django.utils import timezone

from ..categories.models import Category
from ..core.utils import slugify
from ..polls.models import Poll
from ..threads.models import Thread
from .enums import ThreadEventTypeName
from .hooks import create_thread_event_hook
from .models import ThreadEvent

if TYPE_CHECKING:
    from ..users.models import User


def create_thread_event(
    thread: Thread,
    event_type: str,
    actor: Union["User", str, None] = None,
    *,
    detail: str | None = None,
    content_object: Model | None = None,
    items: int | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event_hook(
        _create_thread_event_action,
        thread,
        event_type,
        actor,
        detail=detail,
        content_object=content_object,
        items=items,
        commit=commit,
        request=request,
    )


def _create_thread_event_action(
    thread: Thread,
    event_type: str,
    actor: Union["User", None, str] = None,
    *,
    detail: str | None = None,
    content_object: Model | None = None,
    items: int | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    actor_id = None
    actor_name = None
    actor_slug = None
    # content_type = None
    # object_id = None

    if isinstance(actor, str):
        actor_name = actor
        actor_slug = slugify(actor)
    elif actor:
        actor_id = actor.id
        actor_name = actor.username
        actor_slug = actor.slug

    # if content_object:
    #     content_type = ".".join(
    #         (
    #             content_object._meta.app_label,
    #             content_object._meta.model_name,
    #         )
    #     )
    #     object_id = content_object.id

    thread_event = ThreadEvent(
        category_id=thread.category_id,
        thread_id=thread.id,
        actor_id=actor_id,
        actor_name=actor_name,
        actor_slug=actor_slug,
        event_type=event_type,
        detail=detail,
        # content_type=content_type,
        # context_id=object_id,
        content_object=content_object,
        items=items,
        created_at=timezone.now(),
    )

    if commit:
        thread_event.save()

    return thread_event


def create_test_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    detail: str | None = None,
    content_object: Model | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventTypeName.TEST,
        actor,
        detail=detail,
        content_object=content_object,
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
        ThreadEventTypeName.PINNED_EVERYWHERE,
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
        ThreadEventTypeName.PINNED_CATEGORY,
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
        ThreadEventTypeName.UNPINNED,
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
        ThreadEventTypeName.LOCKED,
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
        ThreadEventTypeName.UNLOCKED,
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
        ThreadEventTypeName.HIDDEN,
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
        ThreadEventTypeName.UNHIDDEN,
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
        ThreadEventTypeName.APPROVED,
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
        ThreadEventTypeName.REQUIRED_REPLY_APPROVAL,
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
        ThreadEventTypeName.REMOVED_REPLY_APPROVAL,
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
        ThreadEventTypeName.MOVED,
        actor,
        detail=old_category.name,
        content_object=old_category,
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
        ThreadEventTypeName.MERGED,
        actor,
        detail=other_thread.title,
        content_object=other_thread,
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
        ThreadEventTypeName.CHANGED_TITLE,
        actor,
        detail=old_title,
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
        ThreadEventTypeName.MOVED_POSTS_TO,
        actor,
        detail=other_thread.title,
        content_object=other_thread,
        items=posts,
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
        ThreadEventTypeName.MOVED_POSTS_FROM,
        actor,
        detail=other_thread.title,
        content_object=other_thread,
        items=posts,
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
        ThreadEventTypeName.SPLIT_POSTS_INTO,
        actor,
        detail=other_thread.title,
        content_object=other_thread,
        items=posts,
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
        ThreadEventTypeName.SPLIT_POSTS_FROM,
        actor,
        detail=other_thread.title,
        content_object=other_thread,
        items=posts,
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
        ThreadEventTypeName.DELETED_POSTS,
        actor,
        items=posts,
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
        ThreadEventTypeName.STARTED_POLL,
        actor,
        detail=poll.question,
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
        ThreadEventTypeName.CLOSED_POLL,
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
        ThreadEventTypeName.OPENED_POLL,
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
        ThreadEventTypeName.DELETED_POLL,
        actor,
        detail=poll.question,
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
        ThreadEventTypeName.TOOK_OWNERSHIP,
        actor,
        commit=commit,
        request=request,
    )


def create_member_joined_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventTypeName.MEMBER_JOINED,
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
        ThreadEventTypeName.ADDED_MEMBER,
        actor,
        detail=member.username,
        content_object=member,
        commit=commit,
        request=request,
    )


def create_member_left_thread_event(
    thread: Thread,
    actor: Union["User", str, None] = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> ThreadEvent:
    return create_thread_event(
        thread,
        ThreadEventTypeName.MEMBER_LEFT,
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
        ThreadEventTypeName.REMOVED_MEMBER,
        actor,
        detail=member.username,
        content_object=member,
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
        ThreadEventTypeName.CHANGED_OWNER,
        actor,
        detail=new_owner.username,
        content_object=new_owner,
        commit=commit,
        request=request,
    )
