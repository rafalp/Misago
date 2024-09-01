from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ...categories.models import Category
from ..models import ReadCategory
from ..tracker import annotate_categories_read_time, get_unread_categories


def test_get_unread_categories_returns_empty_set_for_anonymous_user(
    dynamic_settings, default_category, anonymous_user
):
    default_category.last_post_on = timezone.now()
    default_category.save()

    request = Mock(settings=dynamic_settings, user=anonymous_user)
    queryset = annotate_categories_read_time(anonymous_user, Category.objects.all())
    unread_categories = get_unread_categories(request, queryset)

    assert not unread_categories


def test_get_unread_categories_excludes_unread_empty_category(dynamic_settings, user):
    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_categories_read_time(user, Category.objects.all())
    unread_categories = get_unread_categories(request, queryset)

    assert not unread_categories


def test_get_unread_categories_includes_unread_category_with_last_post(
    dynamic_settings, default_category, user
):
    default_category.last_post_on = timezone.now()
    default_category.save()

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_categories_read_time(user, Category.objects.all())
    unread_categories = get_unread_categories(request, queryset)

    assert default_category.id in unread_categories


def test_get_unread_categories_excludes_read_empty_category(
    dynamic_settings, default_category, user
):
    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now(),
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_categories_read_time(user, Category.objects.all())
    unread_categories = get_unread_categories(request, queryset)

    assert not unread_categories


def test_get_unread_categories_includes_read_category_with_new_last_post(
    dynamic_settings, default_category, user
):
    user.joined_on -= timedelta(days=2)
    user.save()

    default_category.last_post_on = timezone.now()
    default_category.save()

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now() - timedelta(minutes=5),
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_categories_read_time(user, Category.objects.all())
    unread_categories = get_unread_categories(request, queryset)

    assert default_category.id in unread_categories


def test_get_unread_categories_excludes_read_category(
    dynamic_settings, default_category, user
):
    user.joined_on -= timedelta(days=2)
    user.save()

    default_category.last_post_on = timezone.now()
    default_category.save()

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=default_category.last_post_on,
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_categories_read_time(user, Category.objects.all())
    unread_categories = get_unread_categories(request, queryset)

    assert default_category.id not in unread_categories


def test_get_unread_categories_excludes_unread_category_with_last_post_older_than_user(
    dynamic_settings, default_category, user
):
    user.joined_on -= timedelta(days=2)
    user.save()

    default_category.last_post_on = timezone.now() - timedelta(days=3)
    default_category.save()

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_categories_read_time(user, Category.objects.all())
    unread_categories = get_unread_categories(request, queryset)

    assert not unread_categories


def test_get_unread_categories_excludes_unread_category_with_last_post_older_than_cutoff(
    dynamic_settings, default_category, user
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    default_category.last_post_on = timezone.now().replace(year=2012)
    default_category.save()

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_categories_read_time(user, Category.objects.all())
    unread_categories = get_unread_categories(request, queryset)

    assert not unread_categories


def test_get_unread_categories_excludes_read_category_with_last_post_older_than_cutoff(
    dynamic_settings, default_category, user
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    default_category.last_post_on = timezone.now().replace(year=2012)
    default_category.save()

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now().replace(year=2011),
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_categories_read_time(user, Category.objects.all())
    unread_categories = get_unread_categories(request, queryset)

    assert not unread_categories
