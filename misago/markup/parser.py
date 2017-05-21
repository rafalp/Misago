from __future__ import unicode_literals

import warnings

import bleach
import markdown
from bs4 import BeautifulSoup
from htmlmin.minify import html_minify
from markdown.extensions.fenced_code import FencedCodeExtension

from django.http import Http404
from django.urls import resolve
from django.utils import six

from .bbcode import blocks, inline
from .md.shortimgs import ShortImagesExtension
from .md.striketrough import StriketroughExtension
from .mentions import add_mentions
from .pipeline import pipeline


MISAGO_ATTACHMENT_VIEWS = ('misago:attachment', 'misago:attachment-thumbnail')


def parse(
        text,
        request,
        poster,
        allow_mentions=True,
        allow_links=True,
        allow_images=True,
        allow_blocks=True,
        force_shva=False,
        minify=True
):
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
        'internal_links': [],
        'outgoing_links': [],
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
    """creates and configures markdown object"""
    md = markdown.Markdown(extensions=[
        'markdown.extensions.nl2br',
    ])

    # Remove HTML allowances
    del md.preprocessors['html_block']
    del md.inlinePatterns['html']

    # Remove references
    del md.preprocessors['reference']
    del md.inlinePatterns['reference']
    del md.inlinePatterns['image_reference']
    del md.inlinePatterns['short_reference']

    # Add [b], [i], [u]
    md.inlinePatterns.add('bb_b', inline.bold, '<strong')
    md.inlinePatterns.add('bb_i', inline.italics, '<emphasis')
    md.inlinePatterns.add('bb_u', inline.underline, '<emphasis2')

    # Add ~~deleted~~
    striketrough_md = StriketroughExtension()
    striketrough_md.extendMarkdown(md)

    if allow_links:
        # Add [url]
        md.inlinePatterns.add('bb_url', inline.url(md), '<link')
    else:
        # Remove links
        del md.inlinePatterns['link']
        del md.inlinePatterns['autolink']
        del md.inlinePatterns['automail']

    if allow_images:
        # Add [img]
        md.inlinePatterns.add('bb_img', inline.image(md), '<image_link')
        short_images_md = ShortImagesExtension()
        short_images_md.extendMarkdown(md)
    else:
        # Remove images
        del md.inlinePatterns['image_link']

    if allow_blocks:
        # Add [hr] and [quote] blocks
        md.parser.blockprocessors.add('bb_hr', blocks.BBCodeHRProcessor(md.parser), '>hr')

        fenced_code = FencedCodeExtension()
        fenced_code.extendMarkdown(md, None)

        code_bbcode = blocks.CodeBlockExtension()
        code_bbcode.extendMarkdown(md)

        quote_bbcode = blocks.QuoteExtension()
        quote_bbcode.extendMarkdown(md)
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
    result['parsed_text'] = bleach.linkify(
        result['parsed_text'],
        skip_tags=['a', 'code', 'pre'],
        parse_email=True,
    )


def clean_links(request, result, force_shva=False):
    host = request.get_host()

    soup = BeautifulSoup(result['parsed_text'], 'html5lib')
    for link in soup.find_all('a'):
        if is_internal_link(link['href'], host):
            link['href'] = clean_internal_link(link['href'], host)
            result['internal_links'].append(link['href'])
            link['href'] = clean_attachment_link(link['href'], force_shva)
        else:
            result['outgoing_links'].append(clean_link_prefix(link['href']))
            link['href'] = assert_link_prefix(link['href'])
            link['rel'] = 'nofollow'

        if link.string:
            link.string = clean_link_prefix(link.string)

    for img in soup.find_all('img'):
        img['alt'] = clean_link_prefix(img['alt'])
        if is_internal_link(img['src'], host):
            img['src'] = clean_internal_link(img['src'], host)
            result['images'].append(img['src'])
            img['src'] = clean_attachment_link(img['src'], force_shva)
        else:
            result['images'].append(clean_link_prefix(img['src']))
            img['src'] = assert_link_prefix(img['src'])

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


def assert_link_prefix(link):
    if link.lower().startswith('https:'):
        return link
    if link.lower().startswith('http:'):
        return link
    if link.startswith('//'):
        return 'http:{}'.format(link)

    return 'http://{}'.format(link)


def clean_internal_link(link, host):
    link = clean_link_prefix(link)

    if link.lower().startswith('www.'):
        link = link[4:]
    if host.lower().startswith('www.'):
        host = host[4:]

    if link.lower().startswith(host):
        link = link[len(host):]

    return link or '/'


def clean_attachment_link(link, force_shva=False):
    try:
        resolution = resolve(link)
        url_name = ':'.join(resolution.namespaces + [resolution.url_name])
    except (Http404, ValueError):
        return link

    if url_name in MISAGO_ATTACHMENT_VIEWS:
        if force_shva:
            link = '{}?shva=1'.format(link)
        elif link.endswith('?shva=1'):
            link = link[:-7]
    return link


def minify_result(result):
    # [25:-14] trims <html><head></head><body> and </body></html>
    result['parsed_text'] = html_minify(result['parsed_text'].encode('utf-8'))
    result['parsed_text'] = result['parsed_text'][25:-14]
