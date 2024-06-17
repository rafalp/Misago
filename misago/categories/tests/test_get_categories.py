from unittest.mock import ANY

from ...permissions.enums import CategoryPermission
from ...permissions.proxy import UserPermissionsProxy
from ...testutils import grant_category_group_permissions
from ..categories import get_categories


def grant_categories_permissions(user, categories):
    for category in categories:
        grant_category_group_permissions(
            category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
        )


def test_get_categories_returns_all_categories_visible_by_user(
    cache_versions,
    user,
    default_category,
    sibling_category,
    child_category,
    other_category,
):
    grant_categories_permissions(
        user,
        [
            default_category,
            sibling_category,
            child_category,
            other_category,
        ],
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)

    categories = get_categories(user_permissions, cache_versions)
    assert categories == {
        default_category.id: {
            "id": default_category.id,
            "parent_id": None,
            "name": default_category.name,
            "short_name": default_category.short_name,
            "color": default_category.color,
            "css_class": default_category.css_class,
            "is_closed": default_category.is_closed,
            "url": default_category.get_absolute_url(),
            "lft": default_category.lft,
            "rght": default_category.rght,
        },
        sibling_category.id: {
            "id": sibling_category.id,
            "parent_id": None,
            "name": sibling_category.name,
            "short_name": sibling_category.short_name,
            "color": sibling_category.color,
            "css_class": sibling_category.css_class,
            "is_closed": sibling_category.is_closed,
            "url": sibling_category.get_absolute_url(),
            "lft": sibling_category.lft,
            "rght": sibling_category.rght,
        },
        child_category.id: {
            "id": child_category.id,
            "parent_id": child_category.parent_id,
            "name": child_category.name,
            "short_name": child_category.short_name,
            "color": child_category.color,
            "css_class": child_category.css_class,
            "is_closed": child_category.is_closed,
            "url": child_category.get_absolute_url(),
            "lft": child_category.lft,
            "rght": child_category.rght,
        },
        other_category.id: {
            "id": other_category.id,
            "parent_id": None,
            "name": other_category.name,
            "short_name": other_category.short_name,
            "color": other_category.color,
            "css_class": other_category.css_class,
            "is_closed": other_category.is_closed,
            "url": other_category.get_absolute_url(),
            "lft": other_category.lft,
            "rght": other_category.rght,
        },
    }


def test_get_categories_uses_delay_browse_check_for_child_category(
    cache_versions,
    user,
    default_category,
    sibling_category,
    child_category,
    other_category,
):
    sibling_category.delay_browse_check = True
    sibling_category.save()

    grant_categories_permissions(
        user,
        [
            default_category,
            sibling_category,
            other_category,
        ],
    )

    grant_category_group_permissions(child_category, user.group, CategoryPermission.SEE)

    user_permissions = UserPermissionsProxy(user, cache_versions)

    categories = get_categories(user_permissions, cache_versions)
    assert categories == {
        default_category.id: {
            "id": default_category.id,
            "parent_id": None,
            "name": default_category.name,
            "short_name": default_category.short_name,
            "color": default_category.color,
            "css_class": default_category.css_class,
            "is_closed": default_category.is_closed,
            "url": default_category.get_absolute_url(),
            "lft": default_category.lft,
            "rght": default_category.rght,
        },
        sibling_category.id: {
            "id": sibling_category.id,
            "parent_id": None,
            "name": sibling_category.name,
            "short_name": sibling_category.short_name,
            "color": sibling_category.color,
            "css_class": sibling_category.css_class,
            "is_closed": sibling_category.is_closed,
            "url": sibling_category.get_absolute_url(),
            "lft": sibling_category.lft,
            "rght": sibling_category.rght,
        },
        child_category.id: {
            "id": child_category.id,
            "parent_id": child_category.parent_id,
            "name": child_category.name,
            "short_name": child_category.short_name,
            "color": child_category.color,
            "css_class": child_category.css_class,
            "is_closed": child_category.is_closed,
            "url": child_category.get_absolute_url(),
            "lft": child_category.lft,
            "rght": child_category.rght,
        },
        other_category.id: {
            "id": other_category.id,
            "parent_id": None,
            "name": other_category.name,
            "short_name": other_category.short_name,
            "color": other_category.color,
            "css_class": other_category.css_class,
            "is_closed": other_category.is_closed,
            "url": other_category.get_absolute_url(),
            "lft": other_category.lft,
            "rght": other_category.rght,
        },
    }


def test_get_categories_excludes_categories_invisible_to_user(
    cache_versions,
    user,
    default_category,
    other_category,
):
    grant_categories_permissions(
        user,
        [
            default_category,
            other_category,
        ],
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)

    categories = get_categories(user_permissions, cache_versions)
    assert categories == {
        default_category.id: {
            "id": default_category.id,
            "parent_id": None,
            "name": default_category.name,
            "short_name": default_category.short_name,
            "color": default_category.color,
            "css_class": default_category.css_class,
            "is_closed": default_category.is_closed,
            "url": default_category.get_absolute_url(),
            "lft": default_category.lft,
            "rght": default_category.rght,
        },
        other_category.id: {
            "id": other_category.id,
            "parent_id": None,
            "name": other_category.name,
            "short_name": other_category.short_name,
            "color": other_category.color,
            "css_class": other_category.css_class,
            "is_closed": other_category.is_closed,
            "url": other_category.get_absolute_url(),
            "lft": other_category.lft,
            "rght": other_category.rght,
        },
    }


def test_get_categories_excludes_special_categories(
    cache_versions,
    user,
    private_threads_category,
    default_category,
    other_category,
):
    grant_categories_permissions(
        user,
        [
            private_threads_category,
            default_category,
            other_category,
        ],
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)

    categories = get_categories(user_permissions, cache_versions)
    assert categories == {
        default_category.id: {
            "id": default_category.id,
            "parent_id": None,
            "name": default_category.name,
            "short_name": default_category.short_name,
            "color": default_category.color,
            "css_class": default_category.css_class,
            "is_closed": default_category.is_closed,
            "url": default_category.get_absolute_url(),
            "lft": default_category.lft,
            "rght": default_category.rght,
        },
        other_category.id: {
            "id": other_category.id,
            "parent_id": None,
            "name": other_category.name,
            "short_name": other_category.short_name,
            "color": other_category.color,
            "css_class": other_category.css_class,
            "is_closed": other_category.is_closed,
            "url": other_category.get_absolute_url(),
            "lft": other_category.lft,
            "rght": other_category.rght,
        },
    }


def test_get_categories_skips_database_read_if_there_is_cache(
    mocker,
    django_assert_num_queries,
    cache_versions,
    user,
    default_category,
):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    user_permissions.permissions

    cache_get = mocker.patch(
        "django.core.cache.cache.get",
        return_value=[
            {
                "id": default_category.id,
                "parent_id": None,
                "name": default_category.name,
                "short_name": default_category.short_name,
                "color": default_category.color,
                "css_class": default_category.css_class,
                "is_closed": default_category.is_closed,
                "url": default_category.get_absolute_url(),
                "lft": default_category.lft,
                "rght": default_category.rght,
            },
        ],
    )

    with django_assert_num_queries(0):
        categories = get_categories(user_permissions, cache_versions)

    assert categories == {
        default_category.id: {
            "id": default_category.id,
            "parent_id": None,
            "name": default_category.name,
            "short_name": default_category.short_name,
            "color": default_category.color,
            "css_class": default_category.css_class,
            "is_closed": default_category.is_closed,
            "url": default_category.get_absolute_url(),
            "lft": default_category.lft,
            "rght": default_category.rght,
        },
    }

    cache_get.assert_called_once()


def test_get_categories_is_cached_when_database_is_used(
    mocker,
    django_assert_num_queries,
    cache_versions,
    user,
    default_category,
    other_category,
):
    cache_set = mocker.patch("django.core.cache.cache.set")

    grant_categories_permissions(
        user,
        [
            default_category,
            other_category,
        ],
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)
    user_permissions.permissions

    with django_assert_num_queries(1):
        categories = get_categories(user_permissions, cache_versions)

    assert categories == {
        default_category.id: {
            "id": default_category.id,
            "parent_id": None,
            "name": default_category.name,
            "short_name": default_category.short_name,
            "color": default_category.color,
            "css_class": default_category.css_class,
            "is_closed": default_category.is_closed,
            "url": default_category.get_absolute_url(),
            "lft": default_category.lft,
            "rght": default_category.rght,
        },
        other_category.id: {
            "id": other_category.id,
            "parent_id": None,
            "name": other_category.name,
            "short_name": other_category.short_name,
            "color": other_category.color,
            "css_class": other_category.css_class,
            "is_closed": other_category.is_closed,
            "url": other_category.get_absolute_url(),
            "lft": other_category.lft,
            "rght": other_category.rght,
        },
    }

    cache_set.assert_called_with(
        ANY,
        [
            {
                "id": default_category.id,
                "parent_id": None,
                "name": default_category.name,
                "short_name": default_category.short_name,
                "color": default_category.color,
                "css_class": default_category.css_class,
                "is_closed": default_category.is_closed,
                "url": default_category.get_absolute_url(),
                "lft": default_category.lft,
                "rght": default_category.rght,
            },
            {
                "id": other_category.id,
                "parent_id": None,
                "name": other_category.name,
                "short_name": other_category.short_name,
                "color": other_category.color,
                "css_class": other_category.css_class,
                "is_closed": other_category.is_closed,
                "url": other_category.get_absolute_url(),
                "lft": other_category.lft,
                "rght": other_category.rght,
            },
        ],
    )
