from ..groups import set_default_group


def test_default_group_is_changed(members_group, custom_group):
    assert members_group.is_default
    assert not custom_group.is_default

    set_default_group(custom_group)

    custom_group.refresh_from_db()
    assert custom_group.is_default

    members_group.refresh_from_db()
    assert not members_group.is_default
