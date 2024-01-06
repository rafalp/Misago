import pytest

from ..factory import create_markdown


@pytest.fixture
def markdown():
    return create_markdown()


def test_parser_html_blocks_support_is_disabled(markdown):
    result = markdown("<h1>Lorem ipsum</h1>\n<div>Dolor **met**.</div>")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {
                    "type": "text",
                    "raw": "<h1>Lorem ipsum</h1>",
                },
                {"type": "softbreak"},
                {
                    "type": "text",
                    "raw": "<div>Dolor ",
                },
                {
                    "type": "strong",
                    "children": [
                        {
                            "type": "text",
                            "raw": "met",
                        },
                    ],
                },
                {
                    "type": "text",
                    "raw": ".</div>",
                },
            ],
        }
    ]


def test_parser_inline_html_support_is_disabled(markdown):
    result = markdown('<img src="http://misago-project.org" alt="**Image**"/>')
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {
                    "type": "text",
                    "raw": '<img src="',
                },
                {
                    "type": "link",
                    "attrs": {
                        "url": "http://misago-project.org",
                    },
                    "children": [
                        {
                            "type": "text",
                            "raw": "http://misago-project.org",
                        },
                    ],
                },
                {
                    "type": "text",
                    "raw": '" alt="',
                },
                {
                    "type": "strong",
                    "children": [
                        {
                            "type": "text",
                            "raw": "Image",
                        },
                    ],
                },
                {
                    "type": "text",
                    "raw": '"/>',
                },
            ],
        }
    ]
