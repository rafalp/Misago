from typing import TYPE_CHECKING, Iterable, Optional, Union

from django.db import transaction
from django.http import HttpRequest

from ..threads.models import Thread
from ..threadupdates.create import (
    create_changed_owner_thread_update,
    create_left_thread_update,
    create_removed_member_thread_update,
    create_took_ownership_thread_update,
)
from ..threadupdates.models import ThreadUpdate
from .hooks import (
    change_private_thread_owner_hook,
    remove_private_thread_member_hook,
)
from .models import PrivateThreadMember

if TYPE_CHECKING:
    from ..users.models import User


def prefetch_private_thread_member_ids(threads: Iterable[Thread]):
    threads_owners: dict[int:int] = {t.id: None for t in threads}
    threads_members: dict[int : list[int]] = {t.id: [] for t in threads}

    queryset = (
        PrivateThreadMember.objects.filter(thread__in=threads)
        .order_by("id")
        .values_list("thread_id", "user_id", "is_owner")
    )
    for thread_id, user_id, is_owner in queryset:
        if is_owner:
            threads_owners[thread_id] = user_id
        threads_members[thread_id].append(user_id)

    for thread in threads:
        thread.private_thread_owner_id = threads_owners.get(thread.id)
        thread.private_thread_member_ids = threads_members[thread.id]


def get_private_thread_members(thread: Thread) -> tuple[Optional["User"], list["User"]]:
    """Get the owner and member list of a private thread.

    Returns:
        tuple:
            - The thread owner (`User`) or `None` if the owner is missing.
            - A list of `User` objects for all thread members.

    Side effects:
        Sets `private_thread_owner_id` and `private_thread_member_ids` attributes
        on the given `thread` instance.
    """

    queryset = (
        PrivateThreadMember.objects.filter(thread=thread)
        .select_related("user")
        .order_by("id")
    )

    owner: Optional["User"] = None
    members: list["User"] = []

    for member in queryset:
        if member.is_owner:
            owner = member.user
        members.append(member.user)

    thread.private_thread_owner_id = None
    thread.private_thread_member_ids = []

    if owner:
        thread.private_thread_owner_id = owner.id
    if members:
        thread.private_thread_member_ids = [member.id for member in members]

    return owner, members


def change_private_thread_owner(
    actor: Union["User", str, None],
    thread: Thread,
    new_owner: "User",
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return change_private_thread_owner_hook(
        _change_private_thread_owner_action, actor, thread, new_owner, request
    )


def _change_private_thread_owner_action(
    actor: Union["User", str, None],
    thread: Thread,
    new_owner: "User",
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    with transaction.atomic():
        PrivateThreadMember.objects.filter(thread=thread).update(is_owner=False)
        PrivateThreadMember.objects.filter(thread=thread, user=new_owner).update(
            is_owner=True
        )

    if actor == new_owner:
        return create_took_ownership_thread_update(thread, actor, request)

    return create_changed_owner_thread_update(thread, new_owner, actor, request)


def remove_private_thread_member(
    actor: Union["User", str, None],
    thread: Thread,
    member: "User",
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    return remove_private_thread_member_hook(
        _remove_private_thread_member_action, actor, thread, member, request
    )


def _remove_private_thread_member_action(
    actor: Union["User", str, None],
    thread: Thread,
    member: "User",
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    PrivateThreadMember.objects.filter(thread=thread, user=member).delete()

    if actor == member:
        return create_left_thread_update(thread, actor, request)

    return create_removed_member_thread_update(thread, member, actor, request)


def private_thread_has_members(thread: Thread) -> bool:
    return PrivateThreadMember.objects.filter(thread=thread).exists()
