from unittest.mock import ANY

from ...permissions.enums import CategoryPermission
from ...permissions.proxy import UserPermissionsProxy
from ...testutils import grant_category_group_permissions
from ..categories import get_categories, get_category_data


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
        default_category.id: get_category_data(default_category.__dict__),
        sibling_category.id: get_category_data(sibling_category.__dict__),
        child_category.id: get_category_data(child_category.__dict__),
        other_category.id: get_category_data(other_category.__dict__),
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
        default_category.id: get_category_data(default_category.__dict__),
        sibling_category.id: get_category_data(sibling_category.__dict__),
        child_category.id: get_category_data(child_category.__dict__),
        other_category.id: get_category_data(other_category.__dict__),
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
        default_category.id: get_category_data(default_category.__dict__),
        other_category.id: get_category_data(other_category.__dict__),
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
        default_category.id: get_category_data(default_category.__dict__),
        other_category.id: get_category_data(other_category.__dict__),
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
            get_category_data(default_category.__dict__),
        ],
    )

    with django_assert_num_queries(0):
        categories = get_categories(user_permissions, cache_versions)

    assert categories == {
        default_category.id: get_category_data(default_category.__dict__),
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
        default_category.id: get_category_data(default_category.__dict__),
        other_category.id: get_category_data(other_category.__dict__),
    }

    cache_set.assert_called_with(
        ANY,
        [
            get_category_data(default_category.__dict__),
            get_category_data(other_category.__dict__),
        ],
    )


def test_get_category_data_returns_dict_with_category_data(default_category):
    assert get_category_data(default_category.__dict__) == {
        "id": default_category.id,
        "parent_id": None,
        "level": default_category.level - 1,
        "name": default_category.name,
        "short_name": default_category.short_name,
        "color": default_category.color,
        "css_class": default_category.css_class,
        "delay_browse_check": default_category.delay_browse_check,
        "show_started_only": default_category.show_started_only,
        "is_closed": default_category.is_closed,
        "is_vanilla": default_category.is_vanilla,
        "url": default_category.get_absolute_url(),
        "lft": default_category.lft,
        "rght": default_category.rght,
    }
