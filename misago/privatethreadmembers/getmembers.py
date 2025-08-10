from typing import TYPE_CHECKING, Optional

from ..threads.models import Thread
from .models import PrivateThreadMember

if TYPE_CHECKING:
    from ..users.models import User


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
        PrivateThreadMember.objects.filter(thread=thread).select_related("user")
        .order_by("-is_owner", "id")
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
