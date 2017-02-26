import markdown
from markdown.inlinepatterns import LinkPattern
from markdown.util import etree


IMAGES_RE = r'\!(\s?)\((<.*?>|([^\)]*))\)'


class ShortImagesExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.inlinePatterns.add('misago_short_images', ShortImagePattern(IMAGES_RE, md), '_end')


class ShortImagePattern(LinkPattern):
    def handleMatch(self, m):
        img_src = m.groups()[2].strip()
        if img_src:
            img = etree.Element("img")
            img.set('src', img_src)
            img.set('alt', img_src)
            return img
