from datetime import timedelta

from django.utils import timezone

from ..models import ReadCategory
from ..tracker import mark_category_read


def test_mark_category_read_creates_read_category_for_category_without_user_readcategory(
    user, default_category
):
    default_category.last_posted_at = timezone.now()
    default_category.save()

    mark_category_read(user, default_category)

    ReadCategory.objects.get(
        user=user,
        category=default_category,
        read_time=default_category.last_posted_at,
    )


def test_mark_category_read_updates_read_category_for_category_with_user_readcategory(
    user, default_category
):
    read_time = timezone.now()
    old_read_time = read_time - timedelta(hours=24 * 5)

    read_category = ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=old_read_time,
    )

    default_category.last_posted_at = read_time
    default_category.save()

    default_category.user_readcategory = read_category

    mark_category_read(user, default_category)

    read_category.refresh_from_db()
    assert read_category.read_time == read_time


def test_mark_category_read_updates_read_category_for_category_in_forced_update(
    user, default_category
):
    read_time = timezone.now()
    old_read_time = read_time - timedelta(hours=24 * 5)

    read_category = ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=old_read_time,
    )

    default_category.last_posted_at = read_time
    default_category.save()

    mark_category_read(user, default_category, force_update=True)

    read_category.refresh_from_db()
    assert read_category.read_time == read_time


def test_mark_category_read_creates_missing_read_category_for_category_in_forced_update(
    user, default_category
):
    read_time = timezone.now()

    default_category.last_posted_at = read_time
    default_category.save()

    mark_category_read(user, default_category, force_update=True)

    ReadCategory.objects.get(
        user=user,
        category=default_category,
        read_time=read_time,
    )
