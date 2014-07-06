from importlib import import_module

from bs4 import BeautifulSoup
from django.conf import settings
import markdown

from misago.markup.bbcode import inline, blocks


__all__ = ['parse_text']


def parse_text(text, author=None, allow_mentions=True, allow_links=True,
               allow_images=True, allow_blocks=True):
    """
    Message parser

    Utility for flavours to call

    Breaks text into paragraphs, supports code, spoiler and quote blocks,
    headers, lists, images, spoilers, text styles

    Returns dict object
    """
    md = md_factory(author=author, allow_mentions=allow_mentions,
                    allow_links=allow_links, allow_images=allow_images,
                    allow_blocks=allow_blocks)

    parsing_result = {
        'original_text': text,
        'parsed_text': '',
        'markdown': md,
    }

    # Parse text
    parsed_text = md.convert(text)

    # Clean and store parsed text
    parsing_result['parsed_text'] = parsed_text.strip()
    parsing_result = pipeline.process_result(parsing_result)
    return parsing_result


def md_factory(author=None, allow_mentions=True, allow_links=True,
               allow_images=True, allow_blocks=True):
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

    if allow_mentions:
        # Register mentions
        pass

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


class MarkupPipeline(object):
    """
    Small framework for extending parser
    """
    def extend_markdown(self, md):
        for extension in settings.MISAGO_MARKUP_EXTENSIONS:
            module = import_module(extension)
            if hasattr(module, 'extend_markdown'):
                hook = getattr(module, 'extend_markdown')
                hook.extend_markdown(md)
        return md

    def process_result(self, result):
        soup = BeautifulSoup(result['parsed_text'])
        for extension in settings.MISAGO_MARKUP_EXTENSIONS:
            module = import_module(extension)
            if hasattr(module, 'clean_parsed'):
                hook = getattr(module, 'clean_parsed')
                hook.process_result(result, soup)

        souped_text = unicode(soup.body).strip()[6:-7]
        result['parsed_text'] = souped_text
        return result

pipeline = MarkupPipeline()
