from xml.etree.ElementTree import Element

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
    def handleMatch(self, m, _):
        img_src = m.groups()[1].strip()
        if not img_src:
            return None, None, None

        img = Element("img")
        img.set("src", img_src)
        img.set("alt", img_src)
        return img, m.start(0), m.end(0)
