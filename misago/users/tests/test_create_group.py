import pytest

from ..groups import create_group
from ..models import Group


def test_create_group_creates_new_group(db):
    new_group = create_group(name="Top Users")
    assert new_group.id

    group_from_db = Group.objects.get(id=new_group.id)
    assert group_from_db.name == "Top Users"


def test_create_group_sets_default__slug_from_name(db):
    new_group = create_group(name="Top Users")
    assert new_group.name == "Top Users"
    assert new_group.slug == "top-users"


def test_create_group_sets_ordering(db):
    new_group = create_group(name="Top Users")
    assert new_group.ordering == 4


def test_create_group_saves_custom_plugin_data(db):
    new_group = create_group(name="Top Users", plugin_data={"plugin": "ok"})
    assert new_group.plugin_data == {"plugin": "ok"}


def test_create_group_accepts_request_kwarg(db):
    new_group = create_group(name="Top Users", request=True)
    assert new_group


def test_create_group_accepts_form_kwarg(db):
    new_group = create_group(name="Top Users", request=True)
    assert new_group


def test_create_group_raises_value_error_if_name_is_not_set(db):
    with pytest.raises(ValueError):
        create_group()
