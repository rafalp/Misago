from unittest.mock import Mock

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


def test_block_post_processor_wraps_nested_block(parser, post_processor):
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
