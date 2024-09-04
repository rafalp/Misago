from django.http import HttpRequest
from django.db.models import F, Q

from ..categories.models import Category
from ..permissions.privatethreads import filter_private_threads_queryset
from .readtime import get_default_read_time
from .tracker import annotate_threads_read_time


def are_private_threads_read(request: HttpRequest, category: Category) -> bool:
    read_time = get_default_read_time(request.settings, request.user)

    queryset = (
        filter_private_threads_queryset(
            request.user_permissions,
            annotate_threads_read_time(
                request.user, category.thread_set, with_category=False
            ),
        )
        .filter(last_post_on__gt=read_time)
        .filter(Q(last_post_on__gt=F("read_time")) | Q(read_time__isnull=True))
    )

    return not queryset.exists()
