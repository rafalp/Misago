from datetime import datetime

from django.http import HttpRequest
from django.db.models import F, Q

from ..categories.models import Category
from ..permissions.threads import filter_category_threads_queryset
from ..threads.models import Thread
from .readtime import get_default_read_time
from .tracker import annotate_threads_read_time


def is_category_read(
    request: HttpRequest, category: Category, category_read_time: datetime | None
) -> bool:
    read_time = get_default_read_time(request.settings, request.user)

    if category_read_time:
        read_time = max(read_time, category_read_time)

    queryset = (
        filter_category_threads_queryset(
            request.user_permissions,
            request.categories.categories[category.id],
            annotate_threads_read_time(
                request.user, Thread.objects, with_category=False
            ),
        )
        .filter(last_post_on__gt=read_time)
        .filter(Q(last_post_on__gt=F("read_time")) | Q(read_time__isnull=True))
    )

    return not queryset.exists()
