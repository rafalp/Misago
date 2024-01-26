import pytest

from ..html import render_ast_to_html
from ..metadata import create_ast_metadata


@pytest.mark.parametrize(
    "markup",
    (
        "# Hello world!",
        "## Hello world!",
        "### Hello world!",
        "#### Hello world!",
        "##### Hello world!",
        "###### Hello world!",
    ),
)
def test_render_ast_to_html_heading(markup, parser_context, parse_markup, snapshot):
    ast = parse_markup(markup)
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


@pytest.mark.parametrize(
    "markup",
    (
        "Hello world!\n=====",
        "Hello world!\n-----",
    ),
)
def test_render_ast_to_html_setex_heading(
    markup, parser_context, parse_markup, snapshot
):
    ast = parse_markup(markup)
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_paragraph(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello world!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_two_paragraphs(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello world!\n\nHow's going?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_thematic_break(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello world!\n- - -\nHow's going?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_thematic_break_bbcode(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello world!\n[hr]\nHow's going?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_code(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        ```
            if random.randint(0, 10) > 4:
                print("Gotcha!")
                return True
            return False
        ```
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_code_with_syntax(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        ```python
            if random.randint(0, 10) > 4:
                print("Gotcha!")
                return True
            return False
        ```
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_code_bbcode(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        [code]
            if random.randint(0, 10) > 4:
                print("Gotcha!")
                return True
            return False
        [/code]
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_code_bbcode_with_syntax(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        """
        [code=python]
            if random.randint(0, 10) > 4:
                print("Gotcha!")
                return True
            return False
        [/code]
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_code_indented(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        Hello:

            if random.randint(0, 10) > 4:
                print("Gotcha!")
                return True
            return False
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_inline_code(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello `world`!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_emphasis_text(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello *world*!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_emphasis_underscore_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello _world_!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_strong_text(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello **world**!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_strikethrough_text(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello ~~world~~!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_bold_bbcode_text(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello [b]world[/b]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_italics_bbcode_text(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello [i]world[/i]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_underline_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [u]world[/u]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_strikethrough_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [s]world[/s]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_superscript_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [sup]world[/sup]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_subscript_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [sub]world[/sub]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_escaped_characters(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello\[hr\]World!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_soft_linebreak(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello world!\nHow's going?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_for_unsupported_ast_raises_error(parser_context):
    with pytest.raises(ValueError):
        metadata = create_ast_metadata(parser_context, [])
        render_ast_to_html(parser_context, [{"type": "unsupported"}], metadata)
