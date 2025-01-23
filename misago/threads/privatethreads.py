from typing import Iterable

from .models import Thread, ThreadParticipant


def prefetch_private_thread_member_ids(threads: Iterable[Thread]):
    threads_members: dict[int : list[int]] = {t.id: [] for t in threads}

    queryset = (
        ThreadParticipant.objects.filter(thread__in=threads)
        .order_by("-is_owner")
        .values_list("thread_id", "user_id")
    )
    for thread_id, user_id in queryset:
        threads_members[thread_id].append(user_id)

    for thread in threads:
        thread.private_thread_member_ids = threads_members[thread.id]
