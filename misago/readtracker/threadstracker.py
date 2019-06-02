from ..threads.models import Post
from ..threads.permissions import exclude_invisible_posts
from .cutoffdate import get_cutoff_date


def make_read_aware(request, threads):
    if not threads:
        return

    if not hasattr(threads, "__iter__"):
        threads = [threads]

    make_read(threads)

    if request.user.is_anonymous:
        return

    categories = [t.category for t in threads]
    cutoff_date = get_cutoff_date(request.settings, request.user)

    queryset = (
        Post.objects.filter(thread__in=threads, posted_on__gt=cutoff_date)
        .values_list("thread", flat=True)
        .distinct()
    )

    queryset = queryset.exclude(id__in=request.user.postread_set.values("post"))
    queryset = exclude_invisible_posts(request.user_acl, categories, queryset)

    unread_threads = list(queryset)

    for thread in threads:
        if thread.pk in unread_threads:
            thread.is_read = False
            thread.is_new = True


def make_read(threads):
    for thread in threads:
        thread.is_read = True
        thread.is_new = False
