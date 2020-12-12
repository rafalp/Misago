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
)


@pytest.mark.xfail(reason="WIP")
@pytest.mark.parametrize("text, html, ast", MARKDOWN_VALUES)
@pytest.mark.asyncio
async def test_asr_markdown_text(text, html, ast):
    assert ast == ast_markdown(text)


@pytest.mark.xfail(reason="WIP")
@pytest.mark.parametrize("text, html, ast", MARKDOWN_VALUES)
@pytest.mark.asyncio
async def test_html_markdown_text(text, html, ast):
    assert html == html_markdown(text)
