from django.db.models import F
from django.utils import timezone

from misago.threads.permissions import exclude_invisible_threads

from . import signals
from .dates import get_cutoff_date, is_date_tracked
from .models import CategoryRead


def make_read_aware(user, categories):
    if not hasattr(categories, '__iter__'):
        categories = [categories]

    if user.is_anonymous:
        make_read(categories)
        return None

    categories_dict = {}
    for category in categories:
        category.last_read_on = user.joined_on
        category.is_read = not is_date_tracked(category.last_post_on, user)
        if not category.is_read:
            categories_dict[category.pk] = category

    if categories_dict:
        categories_records = user.categoryread_set.filter(category__in=categories_dict.keys())

        for record in categories_records:
            category = categories_dict[record.category_id]
            category.last_read_on = record.last_read_on
            category.is_read = category.last_read_on >= category.last_post_on


def make_read(categories):
    now = timezone.now()
    for category in categories:
        category.last_read_on = now
        category.is_read = True


def start_record(user, category):
    user.categoryread_set.create(
        category=category,
        last_read_on=user.joined_on,
    )


def sync_record(user, category):
    cutoff_date = get_cutoff_date()
    if user.joined_on > cutoff_date:
        cutoff_date = user.joined_on

    try:
        category_record = user.categoryread_set.get(category=category)
        if category_record.last_read_on > cutoff_date:
            cutoff_date = category_record.last_read_on
    except CategoryRead.DoesNotExist:
        category_record = None

    all_threads = category.thread_set.filter(last_post_on__gt=cutoff_date)
    all_threads_count = exclude_invisible_threads(user, [category], all_threads).count()

    read_threads_count = user.threadread_set.filter(
        category=category,
        thread__in=all_threads,
        last_read_on__gt=cutoff_date,
        thread__last_post_on__lte=F("last_read_on"),
    ).count()

    category_is_read = read_threads_count == all_threads_count

    if category_is_read:
        signals.category_read.send(sender=user, category=category)

    if category_record:
        if category_is_read:
            category_record.last_read_on = timezone.now()
        else:
            category_record.last_read_on = cutoff_date
        category_record.save(update_fields=['last_read_on'])
    else:
        if category_is_read:
            last_read_on = timezone.now()
        else:
            last_read_on = cutoff_date
        category_record = user.categoryread_set.create(
            category=category, last_read_on=last_read_on
        )


def read_category(user, category):
    categories = [category.pk]
    if not category.is_leaf_node():
        categories += category.get_descendants().filter(
            id__in=user.acl_cache['visible_categories'],
        ).values_list(
            'id',
            flat=True,
        )

    user.categoryread_set.filter(category_id__in=categories).delete()
    user.threadread_set.filter(category_id__in=categories).delete()

    now = timezone.now()
    new_reads = []
    for category in categories:
        new_reads.append(CategoryRead(
            user=user,
            category_id=category,
            last_read_on=now,
        ))

    if new_reads:
        CategoryRead.objects.bulk_create(new_reads)

    signals.category_read.send(sender=user, category=category)
