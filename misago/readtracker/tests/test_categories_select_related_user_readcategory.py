from django.utils import timezone

from ...categories.models import Category
from ..models import ReadCategory
from ..tracker import categories_select_related_user_readcategory


def test_categories_select_related_user_readcategory_is_noop_for_anonymous_user(
    db, anonymous_user
):
    queryset = categories_select_related_user_readcategory(
        Category.objects.all(), anonymous_user
    )

    category = queryset.get(slug="first-category")
    assert not hasattr(category, "user_readcategory")


def test_categories_select_related_user_readcategory_doesnt_set_user_readcategory_for_user_without_one(
    user,
):
    queryset = categories_select_related_user_readcategory(Category.objects.all(), user)

    category = queryset.get(slug="first-category")
    assert not hasattr(category, "user_readcategory")


def test_categories_select_related_user_readcategory_sets_user_readcategory_if_it_exists(
    user, default_category
):
    read_time = timezone.now().replace(year=2012)

    readcategory = ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=read_time,
    )

    queryset = categories_select_related_user_readcategory(Category.objects.all(), user)

    category = queryset.get(slug="first-category")
    assert category.user_readcategory == readcategory
