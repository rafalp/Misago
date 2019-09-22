from unittest.mock import Mock

from ..context_processors import menus


def test_context_processor_adds_navbar_menu_to_context(
    navbar_menu_items, cache_versions
):
    result = menus(Mock(cache_versions=cache_versions))
    assert isinstance(result, dict)
    assert len(navbar_menu_items) == len(result["navbar_menu"])


def test_context_processor_adds_footer_menu_to_context(
    footer_menu_items, cache_versions
):
    result = menus(Mock(cache_versions=cache_versions))
    assert isinstance(result, dict)
    assert len(footer_menu_items) == len(result["footer_menu"])
