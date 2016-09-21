import markdown

import bleach
from bs4 import BeautifulSoup
from django.utils import six
from htmlmin.minify import html_minify

from .bbcode import blocks, inline
from .md.shortimgs import ShortImagesExtension
from .mentions import add_mentions
from .pipeline import pipeline


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
    md = md_factory(
        allow_links=allow_links,
        allow_images=allow_images,
        allow_blocks=allow_blocks,
    )

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

    parsing_result = pipeline.process_result(parsing_result)

    if allow_mentions:
        add_mentions(request, parsing_result)

    if allow_links or allow_images:
        clean_links(request, parsing_result)

    if minify:
        minify_result(parsing_result)
    return parsing_result


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
        short_images_md = ShortImagesExtension()
        short_images_md.extendMarkdown(md)
    else:
        # Remove images
        del md.inlinePatterns['image_link']

    if allow_blocks:
        # Add [hr] [quote], [spoiler], [list] and [code] blocks
        md.parser.blockprocessors.add('bb_hr', blocks.BBCodeHRProcessor(md.parser), '>hr')
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


def linkify_paragraphs(result):
    result['parsed_text'] = bleach.linkify(result['parsed_text'], skip_pre=True, parse_email=True)


def clean_links(request, result):
    site_address = '%s://%s' % (request.scheme, request.get_host())

    soup = BeautifulSoup(result['parsed_text'], 'html5lib')
    for link in soup.find_all('a'):
        if link['href'].lower().startswith(site_address):
            result['inside_links'].append(link['href'])
            if link['href'].lower() == site_address:
                link['href'] = '/'
            else:
                link['href'] = link['href'].lower()[len(site_address):]
        else:
            result['outgoing_links'].append(link['href'])

        if link.string.startswith('http://'):
            link.string.replace_with(link.string[7:].strip())
        if link.string.startswith('https://'):
            print link.string
            link.string.replace_with(link.string[8:].strip())

    for img in soup.find_all('img'):
        result['images'].append(img['src'])
        if img['src'].lower().startswith(site_address):
            if img['src'].lower() == site_address:
                img['src'] = '/'
            else:
                img['src'] = img['src'].lower()[len(site_address):]

        if img['alt'].startswith('http://'):
            img['alt'] = img['alt'][7:].strip()
        if img['alt'].startswith('https://'):
            img['alt'] = img['alt'][8:].strip()

    # [6:-7] trims <body></body> wrap
    result['parsed_text'] = six.text_type(soup.body)[6:-7]


def minify_result(result):
    # [25:-14] trims <html><head></head><body> and </body></html>
    result['parsed_text'] = html_minify(result['parsed_text'].encode('utf-8'))
    result['parsed_text'] = result['parsed_text'][25:-14]
