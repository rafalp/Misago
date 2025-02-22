import pytest

from ..metadata import create_ast_metadata
from ..plaintext import PlainTextFormat, render_ast_to_plaintext


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
def test_render_ast_to_plaintext_heading(
    markup, parser_context, parse_markup, snapshot
):
    ast = parse_markup(markup)
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


@pytest.mark.parametrize(
    "markup",
    (
        "Hello world!\n=====",
        "Hello world!\n-----",
    ),
)
def test_render_ast_to_plaintext_setex_heading(
    markup, parser_context, parse_markup, snapshot
):
    ast = parse_markup(markup)
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_quote(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        > Hello world!
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_quote_bbcode(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        [quote]Hello world![/quote]
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_quote_bbcode_with_author(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        """
        [quote=Author]Hello world![/quote]
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_unordered_list(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        - Lorem
        - _Ipsum_
        - Dolor
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_ordered_list(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        1. Lorem
        2. _Ipsum_
        3. Dolor
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_unordered_list_with_nested_list(
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
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_minimal_table(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        | Col1 |
        | ---- |
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_table(parser_context, parse_markup, snapshot):
    ast = parse_markup(
        """
        | Col1 | Col2 |*Col3*| Col4 |
        | ---- | :--- | :--: | ---: |
        | Cel1 | Cel2 |      | Cel4 |
        | Cel5 |*Cel6*| Cel7 | Cel8 |
        """
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_spoiler(parser_context, parse_markup, snapshot):
    ast = parse_markup("[spoiler]Hello world![/spoiler]")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_spoiler_with_summary(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("[spoiler=Secret message]Hello world![/spoiler]")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_paragraph(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello world!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_two_paragraphs(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello world!\n\nHow's going?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_thematic_break(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello world!\n- - -\nHow's going?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_thematic_break_bbcode(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello world!\n[hr]\nHow's going?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_code(parser_context, parse_markup, snapshot):
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
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_code_with_syntax(
    parser_context, parse_markup, snapshot
):
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
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_code_bbcode(parser_context, parse_markup, snapshot):
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
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_code_bbcode_with_syntax(
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
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_code_indented(parser_context, parse_markup, snapshot):
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
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_inline_code(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello `world`!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_emphasis_text(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello *world*!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_emphasis_underscore_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello _world_!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_strong_text(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello **world**!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_strikethrough_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello ~~world~~!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_bold_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [b]world[/b]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_italics_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [i]world[/i]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_underline_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [u]world[/u]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_strikethrough_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [s]world[/s]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_superscript_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [sup]world[/sup]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_subscript_bbcode_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("Hello [sub]world[/sub]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_escaped_characters(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(r"Hello\[hr\]World!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_soft_linebreak(parser_context, parse_markup, snapshot):
    ast = parse_markup("Hello world!\nHow's going?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_image_auto_link(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See the logo: <!https://misago-project.org/img.png>")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_image(parser_context, parse_markup, snapshot):
    ast = parse_markup("See the logo: !(https://misago-project.org/img.png)")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_image_with_alt_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See the logo: ![Alt text](https://misago-project.org/img.png)")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_image_with_title(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        'See the logo: !(https://misago-project.org/img.png "Amazing, right?")'
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_image_with_title_and_alt_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        'See the logo: ![Alt text](https://misago-project.org/img.png "Amazing, right?")'
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_image_bbcode(parser_context, parse_markup, snapshot):
    ast = parse_markup("See the logo: [img]https://misago-project.org/img.png[/img]")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_image_bbcode_with_alt_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        "See the logo: [img=https://misago-project.org/img.png]Alt text[/img]"
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_image_auto_link_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See the logo: <!https://misago-project.org/img.png>")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_image_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See the logo: !(https://misago-project.org/img.png)")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_image_with_alt_text_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See the logo: ![Alt text](https://misago-project.org/img.png)")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_image_with_title_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        'See the logo: !(https://misago-project.org/img.png "Amazing, right?")'
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_image_with_title_and_alt_text_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        'See the logo: ![Alt text](https://misago-project.org/img.png "Amazing, right?")'
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_image_bbcode_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See the logo: [img]https://misago-project.org/img.png[/img]")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_image_bbcode_with_alt_text_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        "See the logo: [img=https://misago-project.org/img.png]Alt text[/img]"
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_url(parser_context, parse_markup, snapshot):
    ast = parse_markup("See [*the site*](https://misago-project.org)!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_url_with_title(parser_context, parse_markup, snapshot):
    ast = parse_markup('See [*the site*](https://misago-project.org "misago forums")!')
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_url_bbcode(parser_context, parse_markup, snapshot):
    ast = parse_markup("See [url]https://misago-project.org[/url]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_url_bbcode_with_text(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See [url=https://misago-project.org]*the site*[/url]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_attachment_group(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup(
        "See the logo: <attachment=file.png:123><attachment=document.pdf:41>"
    )
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_attachment(parser_context, parse_markup, snapshot):
    ast = parse_markup("See the logo: <attachment=file.png:123>")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_auto_link(parser_context, parse_markup, snapshot):
    ast = parse_markup("See the site: <https://misago-project.org>")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_auto_url(parser_context, parse_markup, snapshot):
    ast = parse_markup("See the site: https://misago-project.org")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_url_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See [*the site*](https://misago-project.org)!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_url_with_title_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup('See [*the site*](https://misago-project.org "misago forums")!')
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_url_bbcode_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See [url]https://misago-project.org[/url]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_url_bbcode_with_text_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See [url=https://misago-project.org]*the site*[/url]!")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_auto_link_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See the site: <https://misago-project.org>")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_auto_url_meta_description(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("See the site: https://misago-project.org")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(
        parser_context,
        ast,
        metadata,
        PlainTextFormat.META_DESCRIPTION,
    )


def test_render_ast_to_plaintext_mention(parser_context, parse_markup, snapshot, user):
    user.id = 1000
    user.set_username("MentionedUser")
    user.set_email("mentioned@example.com")
    user.save()

    ast = parse_markup(f"How's going, @{user.username}?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_mention_non_existing_user(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("How's going, @JohnDoe?")
    metadata = create_ast_metadata(parser_context, ast)
    assert snapshot == render_ast_to_plaintext(parser_context, ast, metadata)


def test_render_ast_to_plaintext_for_unsupported_ast_raises_error(parser_context):
    with pytest.raises(ValueError):
        metadata = create_ast_metadata(parser_context, [])
        render_ast_to_plaintext(parser_context, [{"type": "unsupported"}], metadata)


def test_render_ast_to_plaintext_meta_description_removes_new_lines(
    parser_context, parse_markup
):
    ast = parse_markup("Lorem ipsum\nDolor met")
    metadata = create_ast_metadata(parser_context, ast)
    assert (
        render_ast_to_plaintext(
            parser_context,
            ast,
            metadata,
            PlainTextFormat.META_DESCRIPTION,
        )
        == "Lorem ipsum Dolor met"
    )


def test_render_ast_to_plaintext_search_document_removes_new_lines(
    parser_context, parse_markup
):
    ast = parse_markup("Lorem ipsum\nDolor met")
    metadata = create_ast_metadata(parser_context, ast)
    assert (
        render_ast_to_plaintext(
            parser_context,
            ast,
            metadata,
            PlainTextFormat.SEARCH_DOCUMENT,
        )
        == "Lorem ipsum Dolor met"
    )
