from __future__ import unicode_literals

import markdown

import bleach
from bs4 import BeautifulSoup
from django.core.urlresolvers import resolve
from django.http import Http404
from django.utils import six
from htmlmin.minify import html_minify

from .bbcode import blocks, inline
from .md.shortimgs import ShortImagesExtension
from .mentions import add_mentions
from .pipeline import pipeline


__all__ = ['parse']


def parse(text, request, poster, allow_mentions=True, allow_links=True,
          allow_images=True, allow_blocks=True, force_shva=False, minify=True):
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
        clean_links(request, parsing_result, force_shva)

    if minify:
        minify_result(parsing_result)
    return parsing_result


def md_factory(allow_links=True, allow_images=True, allow_blocks=True):
    """
    Create and configure markdown object
    """
    md = markdown.Markdown(safe_mode='escape', extensions=['nl2br'])

    # Remove references
    del md.preprocessors['reference']
    del md.inlinePatterns['reference']
    del md.inlinePatterns['image_reference']
    del md.inlinePatterns['short_reference']

    # Add [b], [i], [u]
    md.inlinePatterns.add('bb_b', inline.bold, '<strong')
    md.inlinePatterns.add('bb_i', inline.italics, '<emphasis')
    md.inlinePatterns.add('bb_u', inline.underline, '<emphasis2')

    if not allow_links:
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
        # Add [hr], [quote] and [code] blocks
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


def clean_links(request, result, force_shva=False):
    host = request.get_host()
    site_address = '%s://%s' % (request.scheme, request.get_host())

    soup = BeautifulSoup(result['parsed_text'], 'html5lib')
    for link in soup.find_all('a'):
        if is_internal_link(link['href'], host):
            link['href'] = clean_internal_link(link['href'], host)
            if force_shva:
                try:
                    resolution = resolve(link['href'])
                    print resolution
                except (Http404, ValueError):
                    pass
            result['inside_links'].append(link['href'])
        else:
            result['outgoing_links'].append(link['href'])

        if link.string:
            link.string = clean_link_prefix(link.string)

    for img in soup.find_all('img'):
        img['alt'] = clean_link_prefix(img['alt'])
        if is_internal_link(img['src'], host):
            img['src'] = clean_internal_link(img['src'], host)
            result['images'].append(img['src'])
        else:
            result['images'].append(img['src'])

    # [6:-7] trims <body></body> wrap
    result['parsed_text'] = six.text_type(soup.body)[6:-7]


def is_internal_link(link, host):
    if link.startswith('/') and not link.startswith('//'):
        return True

    link = clean_link_prefix(link).lstrip('www.').lower()
    return link.lower().startswith(host.lstrip('www.'))


def clean_link_prefix(link):
    if link.lower().startswith('https:'):
        link = link[6:]
    if link.lower().startswith('http:'):
        link = link[5:]
    if link.startswith('//'):
        link = link[2:]
    return link


def clean_internal_link(link, host):
    link = clean_link_prefix(link)

    if link.lower().startswith('www.'):
        link = link[4:]
    if host.lower().startswith('www.'):
        host = host[4:]

    if link.lower().startswith(host):
        link = link[len(host):]

    return link or '/'


def minify_result(result):
    # [25:-14] trims <html><head></head><body> and </body></html>
    result['parsed_text'] = html_minify(result['parsed_text'].encode('utf-8'))
    result['parsed_text'] = result['parsed_text'][25:-14]
