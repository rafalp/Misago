from unittest.mock import Mock

from ..context_processors import preload_categories_json


def test_categories_json_is_included_in_frontend_json(
    cache_versions,
    user,
    default_category,
    sibling_category,
    child_category,
    other_category,
):
    request = Mock(
        include_frontend_context=True,
        frontend_context={},
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

    preload_categories_json(request)

    assert request.frontend_context["categoriesMap"] == [
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
