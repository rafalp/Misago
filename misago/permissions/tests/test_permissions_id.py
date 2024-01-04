from ..permissionsid import get_permissions_id


def test_permissions_id_is_created_from_groups_ids():
    assert get_permissions_id([1])
    assert get_permissions_id([1, 6, 9])


def test_permissions_id_is_stable():
    assert get_permissions_id([1]) == get_permissions_id([1])
    assert get_permissions_id([1, 6, 9]) == get_permissions_id([1, 6, 9])
    assert get_permissions_id([1]) != get_permissions_id([1, 6, 9])
