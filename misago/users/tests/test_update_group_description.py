import pytest

from ..groups import update_group_description


def test_update_group_description_updates_group_description_attribute(custom_group):
    update_group_description(custom_group, meta="Updated")
    assert custom_group.description.meta == "Updated"


def test_update_group_description_updates_group_description_in_database(custom_group):
    update_group_description(custom_group, meta="Updated")

    custom_group.description.refresh_from_db()
    assert custom_group.description.meta == "Updated"


def test_update_group_description_raises_type_error_for_invalid_attribute(custom_group):
    with pytest.raises(TypeError):
        update_group_description(custom_group, invalid_attr=True)
