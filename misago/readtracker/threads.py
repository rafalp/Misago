from datetime import datetime

from django.http import HttpRequest
from django.db.models import F, Q

from ..categories.models import Category
from ..permissions.threads import filter_category_threads_queryset
from ..threads.models import Thread
from .readtime import get_default_read_time
from .tracker import threads_select_related_user_readthread


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
            threads_select_related_user_readthread(Thread.objects, request.user),
        )
        .filter(last_post_on__gt=read_time)
        .filter(
            Q(last_post_on__gt=F("user_readthread__read_time"))
            | Q(user_readthread__isnull=True)
        )
    )
    print(list(t.last_post_on for t in queryset))
    print(category_read_time)
    return not queryset.exists()
