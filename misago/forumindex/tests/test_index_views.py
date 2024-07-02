import pytest

from ..views import IndexViews

index_views = IndexViews()
index_views.add_index_view("threads", "Threads", lambda: "threads")
index_views.add_index_view("categories", "Categories", lambda: "categories")


def test_index_views_get_choices_returns_django_form_choices_tuple():
    choices = index_views.get_choices()
    assert choices == (
        ("threads", "Threads"),
        ("categories", "Categories"),
    )


def test_index_views_get_view_returns_view_callable():
    view = index_views.get_view("threads")
    assert view() == "threads"


def test_index_views_get_view_raises_key_error_for_invalid_view():
    with pytest.raises(KeyError):
        index_views.get_view("invalid")
