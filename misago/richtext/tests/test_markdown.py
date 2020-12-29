from unittest.mock import ANY

import pytest

from ..parser import parse_markup
from ..markdown import html_markdown

MARKDOWN_VALUES = (
    (
        "Lorem ipsum\ndolor sit amet,",
        "<p>Lorem ipsum<br />\ndolor sit amet,</p>\n",
        [{'id': ANY, 'text': 'Lorem ipsum<br/>dolor sit amet,', 'type': 'p'}],
    ),
    (
        "[b]Lorem ipsum[/b]",
        "<p><strong>Lorem ipsum</strong></p>\n",
        [{'id': ANY, 'text': '<strong>Lorem ipsum</strong>', 'type': 'p'}],
    ),
    (
        "[i]Lorem ipsum[/i]",
        "<p><em>Lorem ipsum</em></p>\n",
        [{'id': ANY, 'text': '<em>Lorem ipsum</em>', 'type': 'p'}],
    ),
    (
        "[u]Lorem ipsum[/u]",
        '<p><span style="text-decoration: underline">Lorem ipsum</span></p>\n',
        [{'id': ANY, 'text': '<span style="text-decoration: underline">Lorem ipsum</span>', 'type': 'p'}],
    ),
    (
        "[s]Lorem ipsum[/s]",
        '<p><span style="text-decoration: line-through">Lorem ipsum</span></p>\n',
        [{'id': ANY, 'text': '<span style="text-decoration: line-through">Lorem ipsum</span>', 'type': 'p'}],
    ),
    (
        '[quote="@smith:123"]Lorem ipsum[/quote]',
        '<p><quote author="smith">Lorem ipsum</quote></p>\n',
        [
            {
                "type": "paragraph",
                "children": [
                    {
                        "type": "quote",
                        "children": {
                            "author": "smith",
                            "id_post": "123",
                            "children": [{"type": "text", "text": "Lorem ipsum"}],
                        },
                    }
                ],
            }
        ],
    ),
    (
        "[code]assert 1 == 1[/code]",
        "<p><pre><code>assert 1 == 1</code></pre>\n</p>\n",
        [
            {
                "type": "paragraph",
                "children": [
                    {
                        "type": "block_code",
                        "text": [{"type": "text", "text": "assert 1 == 1"}],
                        "info": None,
                    }
                ],
            }
        ],
    ),
    (
        "[list]\n[*]punkt jeden\n[*]punkt dwa\n[/list]",
        "<p><ul><br />\n<li>punkt jeden</li>\n<li>punkt dwa</li>\n</ul></p>\n",
        [
            {
                "type": "paragraph",
                "children": [
                    {"type": "list_start", "children": None},
                    {"type": "linebreak"},
                    {
                        "type": "list_item",
                        "children": [{"type": "text", "text": "punkt jeden"}],
                        "level": 0,
                    },
                    {
                        "type": "list_item",
                        "children": [{"type": "text", "text": "punkt dwa"}],
                        "level": 0,
                    },
                    {"type": "list_end", "children": None},
                ],
            }
        ],
    ),
    (
        "[url=https://pl.wikipedia.org]Wikipedia[/url]",
        '<p><a href="https://pl.wikipedia.org" title="Wikipedia">Wikipedia</a></p>\n',
        [
            {
                "type": "paragraph",
                "children": [
                    {
                        "type": "link",
                        "link": "https://pl.wikipedia.org",
                        "children": [{"text": "Wikipedia", "type": "text"}],
                        "title": "Wikipedia",
                    }
                ],
            }
        ],
    ),
    (
        "[img]https://misago.pl/logo.png[/img]",
        '<p><img src="https://misago.pl/logo.png" alt="" /></p>\n',
        [
            {
                "type": "paragraph",
                "children": [
                    {
                        "type": "image",
                        "src": "https://misago.pl/logo.png",
                        "alt": "",
                        "title": None,
                    }
                ],
            }
        ],
    ),
    (
        "[img=https://misago.pl/logo.png]",
        '<p><img src="https://misago.pl/logo.png" alt="" /></p>\n',
        [
            {
                "type": "paragraph",
                "children": [
                    {
                        "type": "image",
                        "src": "https://misago.pl/logo.png",
                        "alt": "",
                        "title": None,
                    }
                ],
            }
        ],
    ),
)


@pytest.mark.xfail
@pytest.mark.parametrize("text, html, ast", MARKDOWN_VALUES)
@pytest.mark.asyncio
async def test_ast_markdown_text(text, html, ast, graphql_context):
    result, _ = await parse_markup(graphql_context, text)
    assert result == ast


@pytest.mark.xfail
@pytest.mark.parametrize("text, html, ast", MARKDOWN_VALUES)
@pytest.mark.asyncio
async def test_html_markdown_text(text, html, ast):
    assert html == html_markdown(text)
