from unittest.mock import Mock

from django.urls import reverse

from ...categories.proxy import CategoriesProxy
from ..breadcrumbs import get_category_breadcrumbs, get_thread_breadcrumbs


def test_get_category_breadcrumbs_returns_category_breadcrumbs(
    cache_versions, user_permissions, default_category
):
    categories = CategoriesProxy(user_permissions, cache_versions)
    request = Mock(categories=categories)

    data = get_category_breadcrumbs(request, default_category)

    assert data == {
        "id": "breadcrumbs",
        "template_name": "misago/category_breadcrumbs.html",
        "items": [
            {
                "type": "index",
                "label": "Home",
                "url": "/",
            },
        ],
    }


def test_get_category_breadcrumbs_returns_category_breadcrumbs_including_itself(
    cache_versions, user_permissions, default_category
):
    categories = CategoriesProxy(user_permissions, cache_versions)
    request = Mock(categories=categories)

    data = get_category_breadcrumbs(request, default_category, include_category=True)

    assert data == {
        "id": "breadcrumbs",
        "template_name": "misago/category_breadcrumbs.html",
        "items": [
            {
                "type": "index",
                "label": "Home",
                "url": "/",
            },
            {
                "type": "category",
                "label": default_category.name,
                "short_label": default_category.short_name,
                "color": default_category.color,
                "css_class": default_category.css_class,
                "url": reverse(
                    "misago:category-thread-list",
                    kwargs={
                        "category_id": default_category.id,
                        "slug": default_category.slug,
                    },
                ),
            },
        ],
    }


def test_get_thread_breadcrumbs_returns_thread_breadcrumbs(
    cache_versions, user_permissions, default_category, thread
):
    categories = CategoriesProxy(user_permissions, cache_versions)
    request = Mock(categories=categories)

    data = get_thread_breadcrumbs(request, thread)

    assert data == {
        "id": "breadcrumbs",
        "template_name": "misago/thread_breadcrumbs.html",
        "items": [
            {
                "type": "index",
                "label": "Home",
                "url": "/",
            },
            {
                "type": "category",
                "label": default_category.name,
                "short_label": default_category.short_name,
                "color": default_category.color,
                "css_class": default_category.css_class,
                "url": reverse(
                    "misago:category-thread-list",
                    kwargs={
                        "category_id": default_category.id,
                        "slug": default_category.slug,
                    },
                ),
            },
            {
                "type": "thread",
                "label": thread.title,
                "url": reverse(
                    "misago:thread",
                    kwargs={"thread_id": thread.id, "slug": thread.slug},
                ),
            },
        ],
    }
