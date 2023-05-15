from unittest.mock import Mock

from ..categories_map import get_categories_map


def test_categories_map_returns_top_categories_visible_by_user(
    cache_versions,
    user,
    default_category,
    sibling_category,
    child_category,
    other_category,
):
    request = Mock(
        cache_versions=cache_versions,
        user=user,
        user_acl={
            "visible_categories": [
                default_category.id,
                sibling_category.id,
                child_category.id,
                other_category.id,
            ],
        },
    )

    categories_map = get_categories_map(request)
    assert categories_map == [
        {
            "id": default_category.id,
            "name": default_category.name,
            "shortName": default_category.short_name,
            "color": default_category.color,
            "url": default_category.get_absolute_url(),
        },
        {
            "id": sibling_category.id,
            "name": sibling_category.name,
            "shortName": sibling_category.short_name,
            "color": sibling_category.color,
            "url": sibling_category.get_absolute_url(),
        },
        {
            "id": other_category.id,
            "name": other_category.name,
            "shortName": other_category.short_name,
            "color": other_category.color,
            "url": other_category.get_absolute_url(),
        },
    ]


def test_categories_map_excludes_categories_invisible_to_user(
    cache_versions,
    user,
    default_category,
    sibling_category,
    child_category,
    other_category,
):
    request = Mock(
        cache_versions=cache_versions,
        user=user,
        user_acl={
            "visible_categories": [
                default_category.id,
                other_category.id,
            ],
        },
    )

    categories_map = get_categories_map(request)
    assert categories_map == [
        {
            "id": default_category.id,
            "name": default_category.name,
            "shortName": default_category.short_name,
            "color": default_category.color,
            "url": default_category.get_absolute_url(),
        },
        {
            "id": other_category.id,
            "name": other_category.name,
            "shortName": other_category.short_name,
            "color": other_category.color,
            "url": other_category.get_absolute_url(),
        },
    ]


def test_categories_map_excludes_special_categories(
    cache_versions,
    user,
    private_threads_category,
    default_category,
    sibling_category,
    child_category,
    other_category,
):
    request = Mock(
        cache_versions=cache_versions,
        user=user,
        user_acl={
            "visible_categories": [
                private_threads_category.id,
                default_category.id,
                other_category.id,
            ],
        },
    )

    categories_map = get_categories_map(request)
    assert categories_map == [
        {
            "id": default_category.id,
            "name": default_category.name,
            "shortName": default_category.short_name,
            "color": default_category.color,
            "url": default_category.get_absolute_url(),
        },
        {
            "id": other_category.id,
            "name": other_category.name,
            "shortName": other_category.short_name,
            "color": other_category.color,
            "url": other_category.get_absolute_url(),
        },
    ]


def test_categories_map_skips_database_read_if_there_is_cache(
    mocker,
    django_assert_num_queries,
    cache_versions,
    user,
    default_category,
    sibling_category,
    child_category,
    other_category,
):
    cache_get = mocker.patch(
        "django.core.cache.cache.get",
        return_value=[
            {
                "id": default_category.id,
                "name": default_category.name,
                "shortName": default_category.short_name,
                "color": default_category.color,
                "url": default_category.get_absolute_url(),
            },
        ],
    )

    request = Mock(
        cache_versions=cache_versions,
        user=user,
        user_acl={
            "visible_categories": [
                default_category.id,
                other_category.id,
            ],
        },
    )

    with django_assert_num_queries(0):
        categories_map = get_categories_map(request)

    assert categories_map == [
        {
            "id": default_category.id,
            "name": default_category.name,
            "shortName": default_category.short_name,
            "color": default_category.color,
            "url": default_category.get_absolute_url(),
        },
    ]

    cache_get.assert_called_once()


def test_categories_map_is_cached_when_database_is_used(
    mocker,
    django_assert_num_queries,
    cache_versions,
    user,
    default_category,
    sibling_category,
    child_category,
    other_category,
):
    cache_set = mocker.patch("django.core.cache.cache.set")

    request = Mock(
        cache_versions=cache_versions,
        user=user,
        user_acl={
            "visible_categories": [
                default_category.id,
                other_category.id,
            ],
        },
    )

    with django_assert_num_queries(1):
        categories_map = get_categories_map(request)

    assert categories_map == [
        {
            "id": default_category.id,
            "name": default_category.name,
            "shortName": default_category.short_name,
            "color": default_category.color,
            "url": default_category.get_absolute_url(),
        },
        {
            "id": other_category.id,
            "name": other_category.name,
            "shortName": other_category.short_name,
            "color": other_category.color,
            "url": other_category.get_absolute_url(),
        },
    ]

    cache_set.assert_called_once()
