from datetime import datetime

from django.http import HttpRequest
from django.db.models import F, Q

from ..categories.models import Category
from ..permissions.privatethreads import filter_private_threads_queryset
from .readtime import get_default_read_time
from .tracker import threads_select_related_user_readthread


def unread_private_threads_exist(
    request: HttpRequest,
    category: Category,
    category_read_time: datetime | None,
) -> bool:
    queryset = get_unread_private_threads(request, category, category_read_time)
    return queryset.exists()


def get_unread_private_threads(
    request: HttpRequest,
    category: Category,
    category_read_time: datetime | None,
):
    read_time = get_default_read_time(request.settings, request.user)

    if category_read_time:
        read_time = max(read_time, category_read_time)

    return (
        filter_private_threads_queryset(
            request.user_permissions,
            threads_select_related_user_readthread(category.thread_set, request.user),
        )
        .filter(last_posted_at__gt=read_time)
        .filter(
            Q(last_posted_at__gt=F("user_readthread__read_time"))
            | Q(user_readthread__isnull=True)
        )
    )
