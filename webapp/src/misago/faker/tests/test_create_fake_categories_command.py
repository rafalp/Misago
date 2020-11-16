from io import StringIO

from django.core.management import call_command

from ...acl import ACL_CACHE
from ...cache.test import assert_invalidates_cache
from ..management.commands import createfakecategories


def test_management_command_creates_fake_categories(root_category):
    call_command(createfakecategories.Command(), categories=5, stdout=StringIO())
    root_category.refresh_from_db()
    assert root_category.get_descendant_count() == 6  # 5 fakes + 1 default


def test_management_command_updates_categories_tree_after_creation(root_category):
    call_command(createfakecategories.Command(), categories=5, stdout=StringIO())
    root_category.refresh_from_db()
    assert root_category.rght == root_category.lft + 13  # 6 child items


def test_management_command_creates_categories_at_minimal_depth(default_category):
    call_command(
        createfakecategories.Command(),
        categories=5,
        minlevel=default_category.level,
        stdout=StringIO(),
    )

    default_category.refresh_from_db()
    assert default_category.get_descendant_count() == 5


def test_management_command_copies_default_category_acl(default_category):
    call_command(
        createfakecategories.Command(),
        categories=5,
        minlevel=default_category.level,
        stdout=StringIO(),
    )

    default_category.refresh_from_db()
    default_acls_count = default_category.category_role_set.count()

    for fake_category in default_category.get_descendants():
        assert fake_category.category_role_set.count() == default_acls_count


def test_management_command_invalidates_acl_cache(db):
    with assert_invalidates_cache(ACL_CACHE):
        call_command(createfakecategories.Command(), categories=5, stdout=StringIO())
