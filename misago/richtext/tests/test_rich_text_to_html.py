from ..html import convert_rich_text_to_html


def test_paragraph_block_is_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context, [{"id": "t3st", "type": "p", "text": "Hello <b>world</b>!",}]
    )

    assert html == "<p>Hello <b>world</b>!</p>"


def test_multiple_paragraph_blocks_are_converted_to_html(graphql_context):
    html = convert_rich_text_to_html(
        graphql_context,
        [
            {"id": "t3st", "type": "p", "text": "Hello <b>world</b>!",},
            {"id": "z0rd", "type": "p", "text": "How's going?",},
        ],
    )
    assert html == ("<p>Hello <b>world</b>!</p>\n<p>How's going?</p>")
