import pytest

from ...categories.proxy import CategoriesProxy
from ...threads.models import Thread
from ...threads.test import post_thread
from ..proxy import UserPermissionsProxy
from ..threads import ThreadsQuerysetFilter


@pytest.fixture
def filter_factory(cache_versions):
    def filter_factory_function(user):
        permissions = UserPermissionsProxy(user, cache_versions)
        categories = CategoriesProxy(permissions, cache_versions)
        return ThreadsQuerysetFilter(permissions, categories.categories_list)

    return filter_factory_function


def test_threads_queryset_excludes_category_without_any_permissions(
    filter_factory,
    category_thread,
    user,
):
    threads_filter = filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    assert not queryset.exists()


def test_threads_queryset_excludes_category_with_only_see_permission(
    filter_factory,
    category_thread,
    category_members_see_permission,
    user,
):
    threads_filter = filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    assert not queryset.exists()


def test_threads_queryset_includes_category_with_see_and_browse_permission(
    filter_factory,
    category_thread,
    category_members_see_permission,
    category_members_browse_permission,
    user,
):
    threads_filter = filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset
