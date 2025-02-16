import pytest

from ..parser import Parser
from ..postprocessors import BlockPostProcessor


class PostProcessor(BlockPostProcessor):
    opening_type = "mock-open"
    closing_type = "mock-close"

    def wrap_block(
        self,
        parser: Parser,
        opening_block: dict,
        closing_block: dict,
        children: list[dict],
    ) -> dict | None:
        if not children:
            return None

        return {"type": "mock", "children": self(parser, children)}


@pytest.fixture
def post_processor():
    return PostProcessor()


def test_block_post_processor_wraps_block(parser, post_processor):
    result = post_processor(
        parser,
        [
            {"type": "mock-open"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Hello world!"}],
            },
            {"type": "mock-close"},
        ],
    )
    assert result == [
        {
            "type": "mock",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        }
    ]


def test_block_post_processor_wraps_block_in_other_block(parser, post_processor):
    result = post_processor(
        parser,
        [
            {
                "type": "other-block",
                "children": [
                    {"type": "mock-open"},
                    {
                        "type": "paragraph",
                        "children": [{"type": "text", "text": "Hello world!"}],
                    },
                    {"type": "mock-close"},
                ],
            },
        ],
    )
    assert result == [
        {
            "type": "other-block",
            "children": [
                {
                    "type": "mock",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [{"type": "text", "text": "Hello world!"}],
                        },
                    ],
                }
            ],
        },
    ]


def test_block_post_processor_removes_empty_block_in_other_block(
    parser, post_processor
):
    result = post_processor(
        parser,
        [
            {
                "type": "other-block",
                "children": [
                    {"type": "mock-open"},
                    {"type": "mock-close"},
                ],
            },
        ],
    )
    assert result == [
        {
            "type": "other-block",
            "children": [],
        },
    ]


def test_block_post_processor_wraps_block_in_block(parser, post_processor):
    result = post_processor(
        parser,
        [
            {"type": "mock-open"},
            {"type": "mock-open"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Hello world!"}],
            },
            {"type": "mock-close"},
            {"type": "mock-close"},
        ],
    )
    assert result == [
        {
            "type": "mock",
            "children": [
                {
                    "type": "mock",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [{"type": "text", "text": "Hello world!"}],
                        },
                    ],
                }
            ],
        },
    ]


def test_block_post_processor_handles_siblings_blocks(parser, post_processor):
    result = post_processor(
        parser,
        [
            {"type": "mock-open"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Hello world!"}],
            },
            {"type": "mock-close"},
            {"type": "mock-open"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Lorem Ipsum!"}],
            },
            {"type": "mock-close"},
        ],
    )
    assert result == [
        {
            "type": "mock",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
        {
            "type": "mock",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Lorem Ipsum!"}],
                },
            ],
        },
    ]


def test_block_post_processor_handles_blocks_separated_with_paragraph(
    parser, post_processor
):
    result = post_processor(
        parser,
        [
            {"type": "mock-open"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Hello world!"}],
            },
            {"type": "mock-close"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Separator!"}],
            },
            {"type": "mock-open"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Lorem Ipsum!"}],
            },
            {"type": "mock-close"},
        ],
    )
    assert result == [
        {
            "type": "mock",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Separator!"}],
        },
        {
            "type": "mock",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Lorem Ipsum!"}],
                },
            ],
        },
    ]


def test_block_post_processor_handles_unclosed_block(parser, post_processor):
    result = post_processor(
        parser,
        [
            {"type": "mock-open"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Hello world!"}],
            },
        ],
    )
    assert result == [
        {"type": "mock-open"},
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Hello world!"}],
        },
    ]


def test_block_post_processor_handles_unopened_block(parser, post_processor):
    result = post_processor(
        parser,
        [
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Hello world!"}],
            },
            {"type": "mock-close"},
        ],
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Hello world!"}],
        },
        {"type": "mock-close"},
    ]


def test_block_post_processor_handles_extra_closing_block(parser, post_processor):
    result = post_processor(
        parser,
        [
            {"type": "mock-open"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Hello world!"}],
            },
            {"type": "mock-close"},
            {"type": "mock-close"},
        ],
    )
    assert result == [
        {
            "type": "mock",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
        {"type": "mock-close"},
    ]


def test_block_post_processor_handles_extra_opening_block(parser, post_processor):
    result = post_processor(
        parser,
        [
            {"type": "mock-open"},
            {"type": "mock-open"},
            {
                "type": "paragraph",
                "children": [{"type": "text", "text": "Hello world!"}],
            },
            {"type": "mock-close"},
        ],
    )
    assert result == [
        {"type": "mock-open"},
        {
            "type": "mock",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]
