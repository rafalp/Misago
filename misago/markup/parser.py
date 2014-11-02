import bleach
from bs4 import BeautifulSoup
from htmlmin.minify import html_minify
import markdown

from misago.markup.bbcode import inline, blocks
from misago.markup.pipeline import pipeline


__all__ = ['parse']


def parse(text, request, poster, allow_mentions=True, allow_links=True,
               allow_images=True, allow_blocks=True, minify=True):
    """
    Message parser

    Utility for flavours to call

    Breaks text into paragraphs, supports code, spoiler and quote blocks,
    headers, lists, images, spoilers, text styles

    Returns dict object
    """
    md = md_factory(allow_links=allow_links, allow_images=allow_images,
                    allow_blocks=allow_blocks)

    parsing_result = {
        'original_text': text,
        'parsed_text': '',
        'markdown': md,
        'mentions': [],
        'images': [],
        'outgoing_links': [],
        'inside_links': []
    }

    # Parse text
    parsed_text = md.convert(text)

    # Clean and store parsed text
    parsing_result['parsed_text'] = parsed_text.strip()

    if allow_links:
        linkify_paragraphs(parsing_result)

    if allow_links or allow_images:
        make_absolute_links_relative(parsing_result, request)

    parsing_result = pipeline.process_result(parsing_result)

    if minify:
        minify_result(parsing_result)
    return parsing_result


def linkify_paragraphs(result):
    result['parsed_text'] = bleach.linkify(
        result['parsed_text'], skip_pre=True, parse_email=True)


def make_absolute_links_relative(result, request):
    pass


def minify_result(result):
    # [25:-14] trims <html><head></head><body> and </body></html>
    result['parsed_text'] = html_minify(result['parsed_text'])[25:-14]


def md_factory(allow_links=True, allow_images=True, allow_blocks=True):
    """
    Create and configure markdown object
    """
    md = markdown.Markdown(safe_mode='escape',
                           extensions=['nl2br'])

    # Remove references
    del md.preprocessors['reference']
    del md.inlinePatterns['reference']
    del md.inlinePatterns['image_reference']
    del md.inlinePatterns['short_reference']

    # Add [b], [i], [u]
    md.inlinePatterns.add('bb_b', inline.bold, '<strong')
    md.inlinePatterns.add('bb_i', inline.italics, '<emphasis')
    md.inlinePatterns.add('bb_u', inline.underline, '<emphasis2')

    if allow_links:
        # Add [url]
        pass
    else:
        # Remove links
        del md.inlinePatterns['link']
        del md.inlinePatterns['autolink']
        del md.inlinePatterns['automail']

    if allow_images:
        # Add [img]
        pass
    else:
        # Remove images
        del md.inlinePatterns['image_link']

    if allow_blocks:
        # Add [hr] [quote], [spoiler], [list] and [code] blocks
        md.parser.blockprocessors.add('bb_hr',
                                      blocks.BBCodeHRProcessor(md.parser),
                                      '>hr')
    else:
        # Remove blocks
        del md.parser.blockprocessors['hashheader']
        del md.parser.blockprocessors['setextheader']
        del md.parser.blockprocessors['code']
        del md.parser.blockprocessors['quote']
        del md.parser.blockprocessors['hr']
        del md.parser.blockprocessors['olist']
        del md.parser.blockprocessors['ulist']

    return pipeline.extend_markdown(md)
