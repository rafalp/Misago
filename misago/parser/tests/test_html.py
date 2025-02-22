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


def test_render_ast_to_html_quote(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        > Hello world!
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_quote_bbcode(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        [quote]Hello world![/quote]
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_quote_bbcode_with_author(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        """
        [quote=Author]Hello world![/quote]
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_unordered_list(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        - Lorem
        - _Ipsum_
        - Dolor
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_ordered_list(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        1. Lorem
        2. _Ipsum_
        3. Dolor
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_unordered_list_with_nested_list(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        """
        - Lorem
        - _Ipsum_
          - Met
          - Elit
        - Dolor
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_minimal_table(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        | Col1 |
        | ---- |
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_table(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        | Col1 | Col2 |*Col3*| Col4 |
        | ---- | :--- | :--: | ---: |
        | Cel1 | Cel2 |      | Cel4 |
        | Cel5 |*Cel6*| Cel7 | Cel8 |
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_spoiler(parser_context, parse_markup, snapshot):
    ast = parse_markup("[spoiler]Hello world![/spoiler]")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_spoiler_with_summary(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("[spoiler=Secret message]Hello world![/spoiler]")
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
    ast = parse_markup(r"Hello\[hr\]World!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_soft_linebreak(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello world!\nHow's going?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_image_auto_link(parser_context, parse_markup, snapshot):
    ast = parse_markup(f"See the logo: <!https://misago-project.org/img.png>")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_image(parser_context, parse_markup, snapshot):
    ast = parse_markup(f"See the logo: !(https://misago-project.org/img.png)")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_image_with_alt_text(parser_context, parse_markup, snapshot):
    ast = parse_markup(f"See the logo: ![Alt text](https://misago-project.org/img.png)")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_image_with_title(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        f'See the logo: !(https://misago-project.org/img.png "Amazing, right?")'
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_image_with_title_and_alt_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        'See the logo: ![Alt text](https://misago-project.org/img.png "Amazing, right?")'
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_image_bbcode(parser_context, parse_markup, snapshot):
    ast = parse_markup(f"See the logo: [img]https://misago-project.org/img.png[/img]")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_image_bbcode_with_alt_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        f"See the logo: [img=https://misago-project.org/img.png]Alt text[/img]"
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_url(parser_context, parse_markup, snapshot):
    ast = parse_markup(f"See [*the site*](https://misago-project.org)!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_plaintext_url_with_title(parser_context, parse_markup, snapshot):
    ast = parse_markup('See [*the site*](https://misago-project.org "misago forums")!')
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_url_bbcode(parser_context, parse_markup, snapshot):
    ast = parse_markup(f"See [url]https://misago-project.org[/url]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_url_bbcode_with_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(f"See [url=https://misago-project.org]*the site*[/url]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_attachment(parser_context, parse_markup, snapshot):
    ast = parse_markup(f"See the site: <attachment=image.png:123>")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_auto_link(parser_context, parse_markup, snapshot):
    ast = parse_markup(f"See the file: <https://misago-project.org>")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_auto_url(parser_context, parse_markup, snapshot):
    ast = parse_markup(f"See the site: https://misago-project.org")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_mention(parser_context, parse_markup, snapshot, user):
    user.id = 1000
    user.set_username("MentionedUser")
    user.set_email("mentioned@example.com")
    user.save()

    ast = parse_markup(f"How's going, @{user.username}?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_mention_non_existing_user(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(f"How's going, @JohnDoe?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_html(parser_context, ast, metadata)


def test_render_ast_to_html_for_unsupported_ast_raises_error(parser_context):
    with pytest.raises(ValueError):
        metadata = create_ast_metadata(parser_context, [])
        render_ast_to_html(parser_context, [{"type": "unsupported"}], metadata)
