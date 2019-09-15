from unittest.mock import Mock

from ..context_processors import footer, navbar


def test_footer_menu_links_context_processor(links_footer, cache_versions):
    result = footer(Mock(cache_versions=cache_versions))
    assert isinstance(result, dict)
    assert len(links_footer) == len(result["footer_menu_links"])


def test_top_menu_links_context_processor(links_top, cache_versions):
    result = navbar(Mock(cache_versions=cache_versions))
    assert isinstance(result, dict)
    assert len(links_top) == len(result["top_menu_links"])
