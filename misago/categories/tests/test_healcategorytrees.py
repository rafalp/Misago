from io import StringIO

from django.core.management import call_command

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ..management.commands import healcategorytrees
from ..models import Category


def run_command():
    """Run the management command"""
    command = healcategorytrees.Command()
    out = StringIO()
    call_command(command, stdout=out)


def test_heal_category_trees_command_rebuilds_trees(default_category):
    category = Category.objects.create(
        name="Test", slug="test", parent=default_category
    )

    Category.objects.filter(id=default_category.id).update(lft=2, rght=2)
    Category.objects.filter(id=category.id).update(lft=10, rght=3)

    run_command()

    default_category.refresh_from_db()
    assert default_category.lft == 2
    assert default_category.rght == 5

    category.refresh_from_db()
    assert category.lft == 3
    assert category.rght == 4


def test_heal_category_trees_command_invalidates_caches(db):
    with assert_invalidates_cache(CacheName.CATEGORIES):
        run_command()
