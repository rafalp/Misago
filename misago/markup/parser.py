import markdown
from markdown.extensions.fenced_code import FencedCodeExtension

from .bbcode.code import CodeBlockExtension
from .bbcode.hr import BBCodeHRProcessor
from .bbcode.inline import bold, image, italics, underline, url
from .bbcode.quote import QuoteExtension
from .bbcode.spoiler import SpoilerExtension
from .htmlparser import parse_html_string, print_html_string
from .links import clean_links, linkify_texts
from .md.shortimgs import ShortImagesExtension
from .md.strikethrough import StrikethroughExtension
from .pipeline import pipeline


def parse(
    text,
    request,
    poster,
    allow_mentions=True,
    allow_links=True,
    allow_images=True,
    allow_blocks=True,
    force_shva=False,
):
    """
    Message parser

    Utility for flavours to call

    Breaks text into paragraphs, supports code, spoiler and quote blocks,
    headers, lists, images, spoilers, text styles

    Returns dict object
    """
    md = md_factory(
        allow_links=allow_links, allow_images=allow_images, allow_blocks=allow_blocks
    )

    parsing_result = {
        "original_text": text,
        "parsed_text": "",
        "markdown": md,
        "mentions": [],
        "images": [],
        "internal_links": [],
        "outgoing_links": [],
    }

    # Parse text
    parsed_text = md.convert(text)

    # Clean and store parsed text
    parsing_result["parsed_text"] = parsed_text.strip()

    # Run additional operations
    if allow_links or allow_images:
        root_node = parse_html_string(parsing_result["parsed_text"])

        if allow_links:
            linkify_texts(root_node)

        if allow_links or allow_images:
            clean_links(request, parsing_result, root_node, force_shva)

        parsing_result["parsed_text"] = print_html_string(root_node)

    # Let plugins do their magic
    parsing_result = pipeline.process_result(parsing_result)

    return parsing_result


def md_factory(allow_links=True, allow_images=True, allow_blocks=True):
    """creates and configures markdown object"""
    md = markdown.Markdown(extensions=["markdown.extensions.nl2br"])

    # Remove HTML allowances
    md.preprocessors.deregister("html_block")
    md.inlinePatterns.deregister("html")

    # Remove references
    md.parser.blockprocessors.deregister("reference")
    md.inlinePatterns.deregister("reference")
    md.inlinePatterns.deregister("image_reference")
    md.inlinePatterns.deregister("short_reference")

    # Add [b], [i], [u]
    md.inlinePatterns.register(bold, "bb_b", 55)
    md.inlinePatterns.register(italics, "bb_i", 55)
    md.inlinePatterns.register(underline, "bb_u", 55)

    # Add ~~deleted~~
    strikethrough_md = StrikethroughExtension()
    strikethrough_md.extendMarkdown(md)

    if allow_links:
        # Add [url]
        md.inlinePatterns.register(url(md), "bb_url", 155)
    else:
        # Remove links
        md.inlinePatterns.deregister("link")
        md.inlinePatterns.deregister("autolink")
        md.inlinePatterns.deregister("automail")

    if allow_images:
        # Add [img]
        md.inlinePatterns.register(image(md), "bb_img", 145)
        short_images_md = ShortImagesExtension()
        short_images_md.extendMarkdown(md)
    else:
        # Remove images
        md.inlinePatterns.deregister("image_link")

    if allow_blocks:
        # Add [hr] and [quote] blocks
        md.parser.blockprocessors.register(BBCodeHRProcessor(md.parser), "bb_hr", 45)

        fenced_code = FencedCodeExtension(lang_prefix="language-")
        fenced_code.extendMarkdown(md)

        code_bbcode = CodeBlockExtension()
        code_bbcode.extendMarkdown(md)

        quote_bbcode = QuoteExtension()
        quote_bbcode.extendMarkdown(md)

        spoiler_bbcode = SpoilerExtension()
        spoiler_bbcode.extendMarkdown(md)
    else:
        # Remove blocks
        md.parser.blockprocessors.deregister("hashheader")
        md.parser.blockprocessors.deregister("setextheader")
        md.parser.blockprocessors.deregister("code")
        md.parser.blockprocessors.deregister("quote")
        md.parser.blockprocessors.deregister("hr")
        md.parser.blockprocessors.deregister("olist")
        md.parser.blockprocessors.deregister("ulist")

    return pipeline.extend_markdown(md)
