import pytest

from ..groupsproxy import GroupsProxy


def test_groups_proxy_supports_item_access(cache_versions, admins_group):
    groups_proxy = GroupsProxy(cache_versions)
    group = groups_proxy[admins_group.id]

    assert group["id"] == admins_group.id
    assert group["name"] == admins_group.name


def test_groups_proxy_raises_key_error_for_nonexisting_group(
    cache_versions, admins_group
):
    groups_proxy = GroupsProxy(cache_versions)

    with pytest.raises(KeyError):
        group = groups_proxy[admins_group.id * 100]


def test_groups_proxy_returns_items_tuples(
    cache_versions, admins_group, moderators_group, members_group, guests_group
):
    groups_proxy = GroupsProxy(cache_versions)
    groups = groups_proxy.items()

    groups_data = [(group_id, group["name"]) for group_id, group in groups]
    assert groups_data == [
        (admins_group.id, admins_group.name),
        (moderators_group.id, moderators_group.name),
        (members_group.id, members_group.name),
        (guests_group.id, guests_group.name),
    ]


def test_groups_proxy_returns_items_list(
    cache_versions, admins_group, moderators_group, members_group, guests_group
):
    groups_proxy = GroupsProxy(cache_versions)
    groups = groups_proxy.list()

    assert len(groups) == 4
    assert groups[0]["id"] == admins_group.id
    assert groups[1]["id"] == moderators_group.id
    assert groups[2]["id"] == members_group.id
    assert groups[3]["id"] == guests_group.id


def test_groups_proxy_exposes_group_display_fields_and_plugin_data(
    cache_versions, admins_group
):
    groups_proxy = GroupsProxy(cache_versions)
    group = groups_proxy[admins_group.id]

    assert group == {
        "id": admins_group.id,
        "name": admins_group.name,
        "slug": admins_group.slug,
        "user_title": admins_group.user_title,
        "color": admins_group.color,
        "icon": admins_group.icon,
        "css_suffix": admins_group.css_suffix,
        "is_page": admins_group.is_page,
        "is_hidden": admins_group.is_hidden,
        "plugin_data": admins_group.plugin_data,
    }


def test_groups_proxy_caches_data(
    django_assert_num_queries, cache_versions, admins_group, members_group
):
    groups_proxy = GroupsProxy(cache_versions)

    with django_assert_num_queries(1):
        groups_proxy[admins_group.id]
        group = groups_proxy[members_group.id]
        groups_proxy.items()
        groups_proxy.list()

    assert group["id"] == members_group.id
    assert group["name"] == members_group.name
