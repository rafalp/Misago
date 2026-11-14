import pytest

from ..groupsproxy import GroupProxy, GroupsProxy, serialize_group_plugin_data
from ..models import Group


def get_group_proxy(group: Group) -> GroupProxy:
    return GroupProxy(
        id=group.id,
        name=group.name,
        slug=group.slug,
        user_title=group.user_title,
        color=group.color,
        icon=group.icon,
        css_suffix=group.css_suffix,
        is_page=group.is_page,
        is_hidden=group.is_hidden,
        plugin_data=serialize_group_plugin_data(group.plugin_data),
    )


def test_groups_proxy_loads_groups(members_group, cache_versions):
    proxy = GroupsProxy(cache_versions)
    assert members_group in proxy


def test_groups_proxy_skips_database_read_if_cache_exists(
    mocker, django_assert_num_queries, admins_group, members_group, cache_versions
):
    cache_get = mocker.patch(
        "django.core.cache.cache.get",
        return_value=[
            get_group_proxy(admins_group).as_dict(),
            get_group_proxy(members_group).as_dict(),
        ],
    )

    with django_assert_num_queries(0):
        assert GroupsProxy(cache_versions)

    cache_get.assert_called_once()


def test_groups_proxy_caches_data_if_database_is_used(
    mocker, django_assert_num_queries, db, cache_versions
):
    cache_set = mocker.patch("django.core.cache.cache.set")

    with django_assert_num_queries(1):
        assert GroupsProxy(cache_versions)

    cache_set.assert_called_once()


def test_groups_proxy_evaluates_to_true_if_it_contains_groups(db, cache_versions):
    assert GroupsProxy(cache_versions)


def test_groups_proxy_contains_returns_true_for_contained_group(
    members_group, cache_versions
):
    proxy = GroupsProxy(cache_versions)
    assert proxy

    assert members_group in proxy
    assert members_group.id in proxy


def test_groups_proxy_contains_returns_false_for_non_contained_group(
    members_group, cache_versions
):
    proxy = GroupsProxy(cache_versions)
    assert proxy

    new_group = Group.objects.create(name="Test Group")

    assert new_group not in proxy
    assert new_group.id not in proxy


def test_groups_proxy_getitem_returns_group_proxy_object_by_id(
    members_group, cache_versions
):
    proxy = GroupsProxy(cache_versions)

    assert proxy[members_group.id] == get_group_proxy(members_group)


def test_groups_proxy_getitem_raises_key_error_for_nonexisting_id(
    guests_group, cache_versions
):
    proxy = GroupsProxy(cache_versions)

    with pytest.raises(KeyError):
        proxy[guests_group.id + 1000]


def test_groups_proxy_iter_returns_groups_ids_iterator(
    admins_group, moderators_group, members_group, guests_group, cache_versions
):
    proxy = GroupsProxy(cache_versions)

    assert list(proxy) == [
        admins_group.id,
        moderators_group.id,
        members_group.id,
        guests_group.id,
    ]


def test_groups_proxy_len_returns_groups_number(db, cache_versions):
    proxy = GroupsProxy(cache_versions)

    assert len(proxy) == 4


def test_groups_proxy_keys_returns_groups_ids_view(
    admins_group, moderators_group, members_group, guests_group, cache_versions
):
    proxy = GroupsProxy(cache_versions)

    assert list(proxy.keys()) == [
        admins_group.id,
        moderators_group.id,
        members_group.id,
        guests_group.id,
    ]


def test_groups_proxy_values_returns_category_proxies_view(
    admins_group, moderators_group, members_group, guests_group, cache_versions
):
    proxy = GroupsProxy(cache_versions)

    assert list(proxy.values()) == [
        get_group_proxy(admins_group),
        get_group_proxy(moderators_group),
        get_group_proxy(members_group),
        get_group_proxy(guests_group),
    ]


def test_groups_proxy_items_returns_groups_id_and_proxy_view(
    admins_group, moderators_group, members_group, guests_group, cache_versions
):
    proxy = GroupsProxy(cache_versions)

    assert list(proxy.items()) == [
        (admins_group.id, get_group_proxy(admins_group)),
        (moderators_group.id, get_group_proxy(moderators_group)),
        (members_group.id, get_group_proxy(members_group)),
        (guests_group.id, get_group_proxy(guests_group)),
    ]


def test_groups_proxy_get_returns_group_proxy(members_group, cache_versions):
    proxy = GroupsProxy(cache_versions)

    assert proxy.get(members_group.id) == get_group_proxy(members_group)


def test_groups_proxy_get_returns_none_for_nonexisting_group(
    guests_group, cache_versions
):
    proxy = GroupsProxy(cache_versions)

    assert proxy.get(guests_group.id + 1000) is None
