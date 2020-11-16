from ..threads.models import Post, Thread
from ..threads.permissions import exclude_invisible_posts, exclude_invisible_threads
from .cutoffdate import get_cutoff_date


def make_read_aware(request, categories):
    if not categories:
        return

    if not hasattr(categories, "__iter__"):
        categories = [categories]

    make_read(categories)

    if request.user.is_anonymous:
        return

    threads = Thread.objects.filter(category__in=categories)
    threads = exclude_invisible_threads(request.user_acl, categories, threads)

    queryset = (
        Post.objects.filter(
            category__in=categories,
            thread__in=threads,
            posted_on__gt=get_cutoff_date(request.settings, request.user),
        )
        .values_list("category", flat=True)
        .distinct()
    )

    queryset = queryset.exclude(id__in=request.user.postread_set.values("post"))
    queryset = exclude_invisible_posts(request.user_acl, categories, queryset)

    unread_categories = list(queryset)

    for category in categories:
        if category.pk in unread_categories:
            category.is_read = False
            category.is_new = True


def make_read(threads):
    for thread in threads:
        thread.is_read = True
        thread.is_new = False
