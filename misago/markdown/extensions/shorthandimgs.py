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
            img_src = self.sanitize_url(clean_inner(img_src))
        if img_src:
            a = etree.Element("a")
            a.set('href', img_src)
            a.set('rel', 'nofollow')
            a.set('target', '_blank')
            img = etree.SubElement(a, "img")
            img.set('src', img_src)
            img.set('alt', img_src)
            return a