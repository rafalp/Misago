#-*- coding: utf-8 -*-
import re
import markdown
from markdown.inlinepatterns import LinkPattern
from misago.utils.strings import html_escape
from misago.utils.urls import is_inner, clean_inner
from markdown.util import etree

IMAGES_RE =  r'\!(\s?)\((<.*?>|([^\)]*))\)'

class ShorthandImagesExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.add('mi_shorthand_imgs',
                              ShorthandImagePattern(IMAGES_RE, md),
                              '_end')


class ShorthandImagePattern(LinkPattern):
    def handleMatch(self, m):
        img_src = m.groups()[2].strip()
        if is_inner(img_src):
            img_src = clean_inner(img_src)
        if img_src:
            el = etree.Element("img")
            el.set('alt', img_src)
            el.set('src', img_src)
            return el