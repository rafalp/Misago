from django.db import transaction
from django.utils import timezone

from misago.threads.models import Post, Thread
from misago.threads.permissions import exclude_invisible_posts, exclude_invisible_threads

from .dates import get_cutoff_date
from .models import CategoryRead, ThreadRead


def make_read_aware(user, categories):
    if not categories:
        return

    if not hasattr(categories, '__iter__'):
        categories = [categories]

    make_read(categories)

    if user.is_anonymous:
        return

    threads = Thread.objects.filter(category__in=categories)
    threads = exclude_invisible_threads(user, categories, threads)

    queryset = Post.objects.filter(
        category__in=categories,
        thread__in=threads,
        posted_on__gt=get_cutoff_date(user),
    ).values_list('category', flat=True).distinct()

    queryset = queryset.exclude(id__in=user.postread_set.values('post'))
    queryset = exclude_invisible_posts(user, categories, queryset)

    unread_categories = list(queryset)

    for category in categories:
        if category.pk in unread_categories:
            category.is_read = False
            category.is_new = True


def make_read(threads):
    for thread in threads:
        thread.is_read = True
        thread.is_new = False


# Deprecated stuff goes here
def start_record(user, category):
    from misago.core import deprecations
    deprecations.warn("categoriestracker.start_record has been deprecated")


def sync_record(user, category):
    from misago.core import deprecations
    deprecations.warn("categoriestracker.sync_record has been deprecated")


def read_category(user, category):
    from misago.core import deprecations
    deprecations.warn("categoriestracker.read_category has been deprecated")
