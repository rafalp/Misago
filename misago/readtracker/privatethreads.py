from datetime import datetime

from django.http import HttpRequest
from django.db.models import F, Q

from ..categories.models import Category
from ..permissions.privatethreads import filter_private_threads_queryset
from .readtime import get_default_read_time
from .tracker import annotate_threads_read_time


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
            annotate_threads_read_time(
                request.user, category.thread_set, with_category=False
            ),
        )
        .filter(last_post_on__gt=read_time)
        .filter(Q(last_post_on__gt=F("read_time")) | Q(read_time__isnull=True))
    )
