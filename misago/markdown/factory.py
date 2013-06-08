import re
import markdown
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from misago.utils.strings import random_string
from misago.markdown.extensions.cleanlinks import CleanLinksExtension
from misago.markdown.extensions.emoji import EmojiExtension
from misago.markdown.parsers import RemoveHTMLParser

def clear_markdown(text):
    parser = RemoveHTMLParser()
    parser.feed(text)
    return parser.clean_text


def remove_unsupported(md):
    # References are evil, we dont support them
    del md.preprocessors['reference']
    del md.inlinePatterns['reference']
    del md.inlinePatterns['image_reference']
    del md.inlinePatterns['short_reference']


def signature_markdown(acl, text):
    md = markdown.Markdown(
                           safe_mode='escape',
                           output_format=settings.OUTPUT_FORMAT,
                           extensions=['nl2br'])

    remove_unsupported(md)
    cleanlinks = CleanLinksExtension()
    cleanlinks.extendMarkdown(md)

    if not acl.usercp.allow_signature_links():
        del md.inlinePatterns['link']
        del md.inlinePatterns['autolink']
    if not acl.usercp.allow_signature_images():
        del md.inlinePatterns['image_link']
    else:
        emojis = EmojiExtension()
        emojis.extendMarkdown(md)

    del md.parser.blockprocessors['hashheader']
    del md.parser.blockprocessors['setextheader']
    del md.parser.blockprocessors['code']
    del md.parser.blockprocessors['quote']
    del md.parser.blockprocessors['hr']
    del md.parser.blockprocessors['olist']
    del md.parser.blockprocessors['ulist']
    
    return md.convert(text)


def post_markdown(text):
    md = markdown.Markdown(
                           safe_mode='escape',
                           output_format=settings.OUTPUT_FORMAT,
                           extensions=['nl2br', 'fenced_code'])

    remove_unsupported(md)
    md.mi_token = random_string(16)
    for extension in settings.MARKDOWN_EXTENSIONS:
        module = '.'.join(extension.split('.')[:-1])
        extension = extension.split('.')[-1]
        module = import_module(module)
        attr = getattr(module, extension)
        ext = attr()
        ext.extendMarkdown(md)
    text = md.convert(text)
    md, text = tidy_markdown(md, text)
    return md, text


def tidy_markdown(md, text):
    text = text.replace('<p><h3><quotetitle>', '<article><header><quotetitle>')
    text = text.replace('</quotetitle></h3></p>', '</quotetitle></header></article>')
    text = text.replace('</quotetitle></h3><br>\r\n', '</quotetitle></header></article>\r\n<p>')
    text = text.replace('\r\n<p></p>', '')
    return md, text


def finalize_markdown(text):
    def trans_quotetitle(match):
        return _("Posted by %(user)s") % {'user': match.group('content')}
    text = re.sub(r'<quotetitle>(?P<content>.+)</quotetitle>', trans_quotetitle, text)
    text = re.sub(r'<quotesingletitle>', _("Quote"), text)
    text = re.sub(r'<imgalt>', _("Posted image"), text)
    return text


def emojis():
    if 'misago.markdown.extensions.emoji.EmojiExtension' in settings.MARKDOWN_EXTENSIONS:
        from misago.markdown.extensions.emoji import EMOJIS
        return EMOJIS
    return []