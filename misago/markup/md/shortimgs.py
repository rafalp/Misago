from xml import etree

import markdown
from markdown.inlinepatterns import LinkInlineProcessor

IMAGES_RE = r"\!\((<.*?>|([^\)]*))\)"


class ShortImagesExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.register(
            ShortImagePattern(IMAGES_RE, md), "misago_short_images", 200
        )


class ShortImagePattern(LinkInlineProcessor):
    def handleMatch(self, m):
        img_src = m.groups()[2].strip()
        if img_src:
            img = etree.Element("img")
            img.set("src", img_src)
            img.set("alt", img_src)
            return img
