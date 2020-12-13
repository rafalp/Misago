import pytest

from ..markdown import ast_markdown, html_markdown

MARKDOWN_VALUES = (
    (
        "Lorem ipsum",
        "<p>Lorem ipsum</p>\n",
        [{"type": "p", "children": [{"type": "text", "text": "Lorem ipsum"}]}],
    ),
    (
        "**Lorem ipsum**",
        "<p><strong>Lorem ipsum</strong></p>\n",
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "strong",
                        "children": [{"type": "text", "text": "Lorem ipsum"}],
                    }
                ],
            }
        ],
    ),
    (
        "https://www.misago.pl",
        '<p><a href="https://www.misago.pl">https://www.misago.pl</a></p>\n',
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "link",
                        "link": "https://www.misago.pl",
                        "children": None,
                        "title": None,
                    }
                ],
            }
        ],
    ),
    (
        "Lorem <h1>ipsum</h1>",
        "<p>Lorem &lt;h1&gt;ipsum&lt;/h1&gt;</p>\n",
        [
            {
                "type": "p",
                "children": [
                    {"type": "text", "text": "Lorem "},
                    {"type": "inline_html", "text": "<h1>"},
                    {"type": "text", "text": "ipsum"},
                    {"type": "inline_html", "text": "</h1>"},
                ],
            }
        ],
    ),
    (
        "```python\ndef myfuction():\n    return None\n\nmyfunction()\n```",
        '<pre><code class="language-python">def myfuction():\n    return None\n\nmyfunction()\n</code></pre>\n',
        [
            {
                "type": "block_code",
                "text": "def myfuction():\n    return None\n\nmyfunction()\n",
                "info": "python",
            }
        ],
    ),
    (
        "> Lorem ipsum",
        "<blockquote>\n<p>Lorem ipsum</p>\n</blockquote>\n",
        [
            {
                "type": "block_quote",
                "children": [
                    {
                        "type": "p",
                        "children": [{"type": "text", "text": "Lorem ipsum"}],
                    }
                ],
            }
        ],
    ),
    (
        "Lorem ipsum\ndolor sit amet,",
        "<p>Lorem ipsum<br />\ndolor sit amet,</p>\n",
        [
            {
                "type": "p",
                "children": [
                    {"type": "text", "text": "Lorem ipsum"},
                    {"type": "linebreak"},
                    {"type": "text", "text": "dolor sit amet,"},
                ],
            }
        ],
    ),
    (
        "[b]Lorem ipsum[/b]",
        "<p><strong>Lorem ipsum</strong></p>\n",
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "strong",
                        "children": [{"type": "text", "text": "Lorem ipsum"}],
                    }
                ],
            }
        ],
    ),
    (
        "[i]Lorem ipsum[/i]",
        "<p><em>Lorem ipsum</em></p>\n",
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "emphasis",
                        "children": [{"type": "text", "text": "Lorem ipsum"}],
                    }
                ],
            }
        ],
    ),
    (
        "[u]Lorem ipsum[/u]",
        '<p><span style="text-decoration: underline">Lorem ipsum</span></p>\n',
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "underline",
                        "children": [{"type": "text", "text": "Lorem ipsum"}],
                    }
                ],
            }
        ],
    ),
    (
        "[s]Lorem ipsum[/s]",
        '<p><span style="text-decoration: line-through">Lorem ipsum</span></p>\n',
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "line_through",
                        "children": [{"type": "text", "text": "Lorem ipsum"}],
                    }
                ],
            }
        ],
    ),
    (
        "[center]Lorem ipsum[/center]",
        "<p><center>Lorem ipsum</center></p>\n",
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "center",
                        "children": [{"type": "text", "text": "Lorem ipsum"}],
                    }
                ],
            }
        ],
    ),
    (
        '[quote="Cyceron"]Lorem ipsum[/quote]',
        '<p><quote author="Cyceron">Lorem ipsum</quote></p>\n',
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "quote",
                        "author": "Cyceron",
                        "children": [{"type": "text", "text": "Lorem ipsum"}],
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
                "type": "p",
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
        "<p><ul><li>punkt jeden</li><li>punkt dwa</li><ul><p>\n",
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "list",
                        "children": [
                            {
                                "type": "list_element",
                                "children": [{"type": "text", "text": "punkt jeden"},],
                            },
                            {
                                "type": "list_element",
                                "children": [{"type": "text", "text": "punkt dwa"},],
                            },
                        ],
                    },
                    {"type": "linebreak"},
                ],
            }
        ],
    ),
    (
        "[url=https://pl.wikipedia.org]Polska Wikipedia[/url]",
        '<p><a href="https://pl.wikipedia.org" title="Polska Wikipedia">Polska Wikipedia</a></p>\n',
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "link",
                        "link": "https://pl.wikipedia.org",
                        "title": "Polska Wikipedia",
                    }
                ],
            }
        ],
    ),
    (
        "[img]https://misago.pl/logo.png[/img]",
        '<p><img src="https://misago.pl/logo.png" alt="" title=""></p>\n',
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "image",
                        "src": "https://misago.pl/logo.png",
                        "alt": "",
                        "title": "",
                    }
                ],
            }
        ],
    ),
    (
        "[img=https://misago.pl/logo.png]",
        '<p><img src="https://misago.pl/logo.png" alt="" title=""></p>\n',
        [
            {
                "type": "p",
                "children": [
                    {
                        "type": "image",
                        "src": "https://misago.pl/logo.png",
                        "alt": "",
                        "title": "",
                    }
                ],
            }
        ],
    ),
    (
        "[table][tr][td]dane tabeli[/td][/tr][/table]",
        "<table><tr><td>dane tabeli</td></tr></table>\n",
        [
            {
                "type": "table",
                "children": [
                    {
                        "type": "row",
                        "children": [{"type": "cell", "text": "dane tabeli"},],
                    }
                ],
            }
        ],
    ),
)


@pytest.mark.xfail(reason="WIP")
@pytest.mark.parametrize("text, html, ast", MARKDOWN_VALUES)
@pytest.mark.asyncio
async def test_ast_markdown_text(text, html, ast):
    result = ast_markdown(text)
    first_row = result[0]
    if "id" in first_row:
        del first_row["id"]
    assert ast == result


@pytest.mark.xfail(reason="WIP")
@pytest.mark.parametrize("text, html, ast", MARKDOWN_VALUES)
@pytest.mark.asyncio
async def test_html_markdown_text(text, html, ast):
    assert html == html_markdown(text)
