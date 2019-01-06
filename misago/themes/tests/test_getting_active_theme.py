from django.core.files.base import ContentFile

from ..activetheme import get_active_theme
from ..models import Theme


def test_active_theme_data_can_be_obtained(db):
    assert get_active_theme()


def test_if_active_theme_is_default_theme_include_defaults_flag_is_set(db):
    assert get_active_theme()["include_defaults"]


def test_if_active_theme_is_default_themes_child_include_defaults_flag_is_set(
    default_theme, active_theme
):
    active_theme.parent = default_theme
    active_theme.save()
    assert get_active_theme()["include_defaults"]


def test_if_active_theme_is_not_default_themes_child_include_defaults_flag_is_not_set(
    active_theme
):
    assert not get_active_theme()["include_defaults"]


def test_active_theme_styles_are_included(active_theme):
    active_theme.css.create(name="test", url="https://example.com")
    assert get_active_theme()["styles"]


def test_active_theme_parents_styles_are_included(active_theme):
    parent_theme = Theme.objects.create(name="Parent theme")
    parent_theme.css.create(name="test", url="https://example.com")

    active_theme.move_to(parent_theme)
    active_theme.save()

    assert get_active_theme()["styles"]


def test_active_theme_child_themes_styles_are_not_included(active_theme):
    child_theme = Theme.objects.create(parent=active_theme, name="Child theme")
    child_theme.css.create(name="test", url="https://example.com")
    assert not get_active_theme()["styles"]


def test_active_theme_styles_are_ordered(active_theme):
    last_css = active_theme.css.create(
        name="test", url="https://last-example.com", order=1
    )
    first_css = active_theme.css.create(
        name="test", url="https://first-example.com", order=0
    )

    assert get_active_theme()["styles"] == [first_css.url, last_css.url]


def test_active_theme_styles_list_includes_url_to_remote_css(active_theme):
    css = active_theme.css.create(name="test", url="https://last-example.com")
    assert get_active_theme()["styles"] == [css.url]


def test_active_theme_styles_list_contains_url_to_local_css(active_theme):
    css = active_theme.css.create(
        name="test",
        source_file=ContentFile("body {}", name="test.css"),
        source_hash="abcdefgh",
    )
    assert get_active_theme()["styles"] == [css.source_file.url]


def test_active_theme_styles_list_contains_url_to_local_built_css(active_theme):
    css = active_theme.css.create(
        name="test",
        source_needs_building=True,
        build_file=ContentFile("body {}", name="test.css"),
        build_hash="abcdefgh",
    )
    assert get_active_theme()["styles"] == [css.build_file.url]


def test_active_theme_styles_list_exclude_url_to_css_that_has_not_been_built(
    active_theme
):
    active_theme.css.create(
        name="test",
        source_file=ContentFile("body {}", name="test.css"),
        source_hash="abcdefgh",
        source_needs_building=True,
    )
    assert not get_active_theme()["styles"]
