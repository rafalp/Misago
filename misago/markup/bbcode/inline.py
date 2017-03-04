"""
Supported inline BBCodes: b, u, i
"""
import re

from markdown.inlinepatterns import IMAGE_LINK_RE, ImagePattern, SimpleTagPattern, util


class SimpleBBCodePattern(SimpleTagPattern):
    """
    Case insensitive simple BBCode
    """

    def __init__(self, bbcode, tag=None):
        self.pattern = r'(\[%s\](.*?)\[/%s\])' % (bbcode, bbcode)
        self.compiled_re = re.compile(
            "^(.*?)%s(.*?)$" % self.pattern, re.DOTALL | re.UNICODE | re.IGNORECASE
        )

        # Api for Markdown to pass safe_mode into instance
        self.safe_mode = False

        # Store tag
        self.tag = tag or bbcode.lower()


bold = SimpleBBCodePattern('b')
italics = SimpleBBCodePattern('i')
underline = SimpleBBCodePattern('u')


class BBcodePattern(object):
    def __init__(self, pattern, markdown_instance=None):
        self.pattern = pattern
        self.compiled_re = re.compile(
            "^(.*?)%s(.*)$" % pattern, re.DOTALL | re.UNICODE  | re.IGNORECASE)

        self.safe_mode = False
        if markdown_instance:
            self.markdown = markdown_instance


class BBCodeImagePattern(BBcodePattern, ImagePattern):
    def handleMatch(self, m):
        el = util.etree.Element("img")
        src_parts = m.group(2).split()
        if src_parts:
            src = src_parts[0]
            if src[0] == "<" and src[-1] == ">":
                src = src[1:-1]
            el.set('src', self.sanitize_url(self.unescape(src)))
        else:
            el.set('src', "")
        if len(src_parts) > 1:
            el.set('title', dequote(self.unescape(" ".join(src_parts[1:]))))

        if self.markdown.enable_attributes:
            truealt = handleAttributes(m.group(2), el)
        else:
            truealt = m.group(2)

        el.set('alt', self.unescape(truealt))
        return el


IMAGE_PATTERN = r'\[img\](.*?)\[/img\]'


def image(md):
    return BBCodeImagePattern(IMAGE_PATTERN, md)


# todo: URL
# note: can't just replace url's bbcode with md cos:
# [url=http://onet.pl][1][/url] => [[1]](http://onet.pl)
