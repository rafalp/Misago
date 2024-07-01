import pytest

from ...categories.proxy import CategoriesProxy
from ...threads.models import Thread
from ...threads.test import post_thread
from ..proxy import UserPermissionsProxy
from ..threads import CategoryThreadsQuerysetFilter


def test_category_threads_queryset_includes_category_with_see_and_browse_permission(
    category_threads_filter_factory,
    category,
    category_thread,
    category_members_see_permission,
    category_members_browse_permission,
    user,
):
    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset


def test_category_threads_queryset_includes_child_category_with_see_and_browse_permission(
    category_threads_filter_factory,
    category,
    category_thread,
    child_category_thread,
    category_members_see_permission,
    category_members_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    user,
):
    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset
    assert child_category_thread in queryset


def test_category_threads_queryset_excludes_child_category_with_see_and_browse_permission(
    category_threads_filter_factory,
    category,
    category_thread,
    child_category_thread,
    category_members_see_permission,
    category_members_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    user,
):
    category.list_children_threads = False
    category.save()

    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset
    assert child_category_thread not in queryset


def test_category_threads_queryset_excludes_sibling_category_with_see_and_browse_permission(
    category_threads_filter_factory,
    category,
    category_thread,
    sibling_category_thread,
    category_members_see_permission,
    category_members_browse_permission,
    sibling_category_members_see_permission,
    sibling_category_members_browse_permission,
    user,
):
    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset
    assert sibling_category_thread not in queryset


def test_child_category_threads_queryset_excludes_parent_category_with_see_and_browse_permission(
    category_threads_filter_factory,
    child_category,
    category_thread,
    child_category_thread,
    category_members_see_permission,
    category_members_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    user,
):
    threads_filter = category_threads_filter_factory(user, child_category)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread not in queryset
    assert child_category_thread in queryset
