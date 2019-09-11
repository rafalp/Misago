from unittest.mock import Mock

from ..context_processors import footer, navbar


def test_footer_menu_links_context_processor(links_footer):
    result = footer(Mock())
    assert isinstance(result, dict)
    assert len(links_footer) == len(result["footer_menu_links"])


def test_top_menu_links_context_processor(links_top):
    result = navbar(Mock())
    assert isinstance(result, dict)
    assert len(links_top) == len(result["top_menu_links"])
