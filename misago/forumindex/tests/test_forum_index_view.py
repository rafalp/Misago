from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains


@override_dynamic_settings(index_view="categories")
def test_forum_index_displays_categories(db, client):
    response = client.get(reverse("misago:index"))
    assert_contains(response, "page-categories")


@override_dynamic_settings(index_view="threads")
def test_forum_index_displays_threads(db, client):
    response = client.get(reverse("misago:index"))
    assert_contains(response, "page-threads")


@override_dynamic_settings(index_view="invalid")
def test_forum_index_displays_404_for_invalid_index_view(db, client):
    response = client.get(reverse("misago:index"))
    assert response.status_code == 404


@override_dynamic_settings(index_view="categories")
def test_categories_view_redirects_to_index_when_its_homepage(db, client):
    response = client.get(reverse("misago:categories"))
    assert response.status_code == 302
    assert response.headers["location"] == reverse("misago:index")


@override_dynamic_settings(index_view="threads")
def test_categories_view_returns_response_when_its_not_homepage(db, client):
    response = client.get(reverse("misago:categories"))
    assert_contains(response, "page-categories")


@override_dynamic_settings(index_view="threads")
def test_threads_view_redirects_to_index_when_its_homepage(db, client):
    response = client.get(reverse("misago:threads"))
    assert response.status_code == 302
    assert response.headers["location"] == reverse("misago:index")


@override_dynamic_settings(index_view="categories")
def test_threads_view_returns_response_when_its_not_homepage(db, client):
    response = client.get(reverse("misago:threads"))
    assert_contains(response, "page-threads")
