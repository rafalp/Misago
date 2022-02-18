from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_h1_markdown_is_supported(context):
    result, _ = await parse_markup(context, "# Hello world!")
    assert result == [
        {
            "id": ANY,
            "type": "h1",
            "text": "Hello world!",
        }
    ]


@pytest.mark.asyncio
async def test_h1_alternate_markdown_is_supported(context):
    result, _ = await parse_markup(context, "Hello world!\n====")
    assert result == [
        {
            "id": ANY,
            "type": "h1",
            "text": "Hello world!",
        }
    ]


@pytest.mark.asyncio
async def test_h2_markdown_is_supported(context):
    result, _ = await parse_markup(context, "Hello world!\n----")
    assert result == [
        {
            "id": ANY,
            "type": "h2",
            "text": "Hello world!",
        }
    ]


@pytest.mark.asyncio
async def test_h2_alternate_markdown_is_supported(context):
    result, _ = await parse_markup(context, "## Hello world!")
    assert result == [
        {
            "id": ANY,
            "type": "h2",
            "text": "Hello world!",
        }
    ]


@pytest.mark.asyncio
async def test_h3_markdown_is_supported(context):
    result, _ = await parse_markup(context, "### Hello world!")
    assert result == [
        {
            "id": ANY,
            "type": "h3",
            "text": "Hello world!",
        }
    ]


@pytest.mark.asyncio
async def test_h4_markdown_is_supported(context):
    result, _ = await parse_markup(context, "#### Hello world!")
    assert result == [
        {
            "id": ANY,
            "type": "h4",
            "text": "Hello world!",
        }
    ]


@pytest.mark.asyncio
async def test_h5_markdown_is_supported(context):
    result, _ = await parse_markup(context, "##### Hello world!")
    assert result == [
        {
            "id": ANY,
            "type": "h5",
            "text": "Hello world!",
        }
    ]


@pytest.mark.asyncio
async def test_h6_markdown_is_supported(context):
    result, _ = await parse_markup(context, "###### Hello world!")
    assert result == [
        {
            "id": ANY,
            "type": "h6",
            "text": "Hello world!",
        }
    ]


@pytest.mark.asyncio
async def test_quote_markdown_is_supported(context):
    result, _ = await parse_markup(context, "> Hello world!")
    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "author": None,
            "post": None,
            "children": [
                {
                    "id": ANY,
                    "type": "p",
                    "text": "Hello world!",
                }
            ],
        }
    ]


@pytest.mark.asyncio
async def test_code_markdown_is_supported(context):
    result, _ = await parse_markup(context, "```\nconsole.log('test')\n```")
    assert result == [
        {
            "id": ANY,
            "type": "code",
            "syntax": None,
            "text": "console.log(&#x27;test&#x27;)",
        }
    ]


@pytest.mark.asyncio
async def test_code_markdown_with_syntax_is_supported(context):
    result, _ = await parse_markup(context, "```python\nlog('test')\n```")
    assert result == [
        {
            "id": ANY,
            "type": "code",
            "syntax": "python",
            "text": (
                '<span class="hl-n">log</span>'
                '<span class="hl-p">(</span>'
                '<span class="hl-s1">&#39;test&#39;</span>'
                '<span class="hl-p">)</span>'
            ),
        }
    ]


@pytest.mark.asyncio
async def test_code_markdown_escapes_text(context):
    result, _ = await parse_markup(context, "```\n<script>\n```")
    assert result == [
        {
            "id": ANY,
            "type": "code",
            "syntax": None,
            "text": "&lt;script&gt;",
        }
    ]


@pytest.mark.asyncio
async def test_horizontal_line_markdown_is_supported(context):
    result, _ = await parse_markup(context, "Hello\n- - -\nWorld")
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": "Hello",
        },
        {
            "id": ANY,
            "type": "hr",
        },
        {
            "id": ANY,
            "type": "p",
            "text": "World",
        },
    ]


@pytest.mark.asyncio
async def test_ordered_list_markdown_is_supported(context):
    result, _ = await parse_markup(context, "1. Lorem\n2. Ipsum")
    assert result == [
        {
            "id": ANY,
            "type": "list",
            "ordered": True,
            "children": [
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Lorem"}],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Ipsum"}],
                },
            ],
        },
    ]


@pytest.mark.asyncio
async def test_unordered_list_markdown_is_supported(context):
    result, _ = await parse_markup(context, "- Lorem\n- Ipsum")
    assert result == [
        {
            "id": ANY,
            "type": "list",
            "ordered": False,
            "children": [
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Lorem"}],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Ipsum"}],
                },
            ],
        },
    ]


@pytest.mark.asyncio
async def test_nesting_lists_markdown_is_supported(context):
    result, _ = await parse_markup(
        context,
        (
            "1. Apple\n"
            "2. Orange\n"
            "    1. Banana\n"
            "    2. Lemon\n"
            "3. Tomato\n"
            "4. Potato\n"
        ),
    )
    assert result == [
        {
            "id": ANY,
            "type": "list",
            "ordered": True,
            "children": [
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Apple"}],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [
                        {"id": ANY, "type": "f", "text": "Orange"},
                        {
                            "id": ANY,
                            "type": "list",
                            "ordered": True,
                            "children": [
                                {
                                    "id": ANY,
                                    "type": "li",
                                    "children": [
                                        {
                                            "id": ANY,
                                            "type": "f",
                                            "text": "Banana",
                                        }
                                    ],
                                },
                                {
                                    "id": ANY,
                                    "type": "li",
                                    "children": [
                                        {"id": ANY, "type": "f", "text": "Lemon"}
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Tomato"}],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Potato"}],
                },
            ],
        },
    ]
