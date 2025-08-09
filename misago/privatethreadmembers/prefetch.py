from typing import Iterable

from ..threads.models import Thread
from .models import PrivateThreadMember


def prefetch_private_thread_member_ids(threads: Iterable[Thread]):
    threads_owners: dict[int:int] = {t.id: None for t in threads}
    threads_members: dict[int : list[int]] = {t.id: [] for t in threads}

    queryset = (
        PrivateThreadMember.objects.filter(thread__in=threads)
        .order_by("-is_owner", "id")
        .values_list("thread_id", "user_id", "is_owner")
    )
    for thread_id, user_id, is_owner in queryset:
        if is_owner:
            threads_owners[thread_id] = user_id
        threads_members[thread_id].append(user_id)

    for thread in threads:
        thread.private_thread_owner_id = threads_owners.get(thread.id)
        thread.private_thread_member_ids = threads_members[thread.id]
