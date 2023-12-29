import pytest

from ..groups import update_group


def test_update_group_updates_group_attribute(custom_group):
    update_group(custom_group, is_hidden=True)
    assert custom_group.is_hidden


def test_update_group_updates_group_in_database(custom_group):
    update_group(custom_group, name="Hello")

    custom_group.refresh_from_db()
    assert custom_group.name == "Hello"


def test_update_group_updates_slug_attribute_from_name(custom_group):
    update_group(custom_group, name="New Name")
    assert custom_group.slug == "new-name"


def test_update_group_updates_slug_attribute_separately_from_name(custom_group):
    update_group(custom_group, name="New Name", slug="old-slug")
    assert custom_group.slug == "old-slug"


def test_update_group_raises_type_error_for_invalid_attribute(custom_group):
    with pytest.raises(TypeError):
        update_group(custom_group, invalid_attr=True)
