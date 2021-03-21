from ..html import convert_rich_text_to_html


def test_code_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "code",
                "syntax": None,
                "text": "Hello <b>world</b>!",
            }
        ],
    )

    assert html == "<pre><code>Hello &lt;b&gt;world&lt;/b&gt;!</code></pre>"


def test_fragment_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "f",
                "text": "Hello <b>world</b>!",
            }
        ],
    )

    assert html == "Hello <b>world</b>!"


def test_heading_1_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "h1",
                "text": "Hello <b>world</b>!",
            }
        ],
    )

    assert html == '<div class="h1">Hello <b>world</b>!</div>'


def test_heading_2_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "h2",
                "text": "Hello <b>world</b>!",
            }
        ],
    )

    assert html == '<div class="h2">Hello <b>world</b>!</div>'


def test_heading_3_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "h3",
                "text": "Hello <b>world</b>!",
            }
        ],
    )

    assert html == '<div class="h3">Hello <b>world</b>!</div>'


def test_heading_4_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "h4",
                "text": "Hello <b>world</b>!",
            }
        ],
    )

    assert html == '<div class="h4">Hello <b>world</b>!</div>'


def test_heading_5_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "h5",
                "text": "Hello <b>world</b>!",
            }
        ],
    )

    assert html == '<div class="h5">Hello <b>world</b>!</div>'


def test_heading_6_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "h6",
                "text": "Hello <b>world</b>!",
            }
        ],
    )

    assert html == '<div class="h6">Hello <b>world</b>!</div>'


def test_horizontal_rule_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [{"id": "t3st", "type": "hr"}],
    )

    assert html == "<hr/>"


def test_paragraph_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "p",
                "text": "Hello <b>world</b>!",
            }
        ],
    )

    assert html == "<p>Hello <b>world</b>!</p>"


def test_ordered_list_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "list",
                "ordered": True,
                "children": [
                    {
                        "id": "t3st",
                        "type": "li",
                        "children": [
                            {
                                "id": "t3st",
                                "type": "f",
                                "text": "Hello <b>world</b>!",
                            }
                        ],
                    }
                ],
            }
        ],
    )

    assert html == "<ol><li>Hello <b>world</b>!</li></ol>"


def test_unordered_list_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "list",
                "ordered": False,
                "children": [
                    {
                        "id": "t3st",
                        "type": "li",
                        "children": [
                            {
                                "id": "t3st",
                                "type": "f",
                                "text": "Hello <b>world</b>!",
                            }
                        ],
                    }
                ],
            }
        ],
    )

    assert html == "<ul><li>Hello <b>world</b>!</li></ul>"


def test_quote_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "quote",
                "author": None,
                "post": None,
                "children": [
                    {
                        "id": "t3st",
                        "type": "p",
                        "text": "Hello <b>world</b>!",
                    }
                ],
            }
        ],
    )

    assert html == "<blockquote><p>Hello <b>world</b>!</p></blockquote>"


def test_spoiler_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "spoiler",
                "children": [
                    {
                        "id": "t3st",
                        "type": "p",
                        "text": "Hello <b>world</b>!",
                    }
                ],
            }
        ],
    )

    assert html == "<blockquote><p>Hello <b>world</b>!</p></blockquote>"


def test_multiple_blocks_are_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {
                "id": "t3st",
                "type": "p",
                "text": "Hello <b>world</b>!",
            },
            {
                "id": "z0rd",
                "type": "p",
                "text": "How's going?",
            },
        ],
    )
    assert html == ("<p>Hello <b>world</b>!</p>\n<p>How's going?</p>")
