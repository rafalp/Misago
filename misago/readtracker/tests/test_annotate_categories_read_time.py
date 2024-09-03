from django.utils import timezone

from ...categories.models import Category
from ..models import ReadCategory
from ..tracker import annotate_categories_read_time


def test_annotate_categories_read_time_is_noop_for_anonymous_user(db, anonymous_user):
    queryset = annotate_categories_read_time(anonymous_user, Category.objects.all())

    category = queryset.get(slug="first-category")
    assert not hasattr(category, "read_time")


def test_annotate_categories_read_time_sets_none_read_time_for_user_without_one(user):
    queryset = annotate_categories_read_time(user, Category.objects.all())

    category = queryset.get(slug="first-category")
    assert category.read_time is None


def test_annotate_categories_read_time_sets_read_time_for_user_with_one(
    user, default_category
):
    read_time = timezone.now().replace(year=2012)

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=read_time,
    )

    queryset = annotate_categories_read_time(user, Category.objects.all())

    category = queryset.get(slug="first-category")
    assert category.read_time == read_time
