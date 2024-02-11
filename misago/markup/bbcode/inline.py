"""
Supported inline BBCodes: b, u, i
"""

import re
from xml.etree.ElementTree import Element

from markdown.inlinepatterns import (
    ImageInlineProcessor,
    LinkInlineProcessor,
    Pattern,
    SimpleTagPattern,
    dequote,
)


class SimpleBBCodePattern(SimpleTagPattern):
    """
    Case insensitive simple BBCode
    """

    def __init__(self, bbcode, tag=None):  # pylint: disable=super-init-not-called
        self.pattern = r"(\[%s\](.*?)\[/%s\])" % (bbcode, bbcode)
        self.compiled_re = re.compile(
            "^(.*?)%s(.*?)$" % self.pattern, re.DOTALL | re.UNICODE | re.IGNORECASE
        )

        # Api for Markdown to pass safe_mode into instance
        self.safe_mode = False

        # Store tag
        self.tag = tag or bbcode.lower()


bold = SimpleBBCodePattern("b")
italics = SimpleBBCodePattern("i")
underline = SimpleBBCodePattern("u")


class BBcodeProcessor(Pattern):
    def __init__(self, pattern, md=None):
        self.pattern = pattern
        self.compiled_re = re.compile(
            "^(.*?)%s(.*)$" % pattern, re.DOTALL | re.UNICODE | re.IGNORECASE
        )

        self.safe_mode = False
        if md:
            self.md = md


class BBCodeImageProcessor(BBcodeProcessor, ImageInlineProcessor):
    def handleMatch(self, m, _):
        el = Element("img")

        src = m.group("content").strip()
        el.set("src", self.unescape(src))

        alt_text = src.replace('"', "&quot;")
        if alt_text.lower()[:6] == "https:":
            alt_text = alt_text[6:]
        elif alt_text.lower()[:5] == "http:":
            alt_text = alt_text[5:]

        alt_text = alt_text.lstrip("/")

        el.set("alt", alt_text)

        return el, m.start("open"), m.end("close")


IMAGE_PATTERN = r"(?P<open>\[img\])(?P<content>.*?)(?P<close>\[/img\])"


def image(md):
    return BBCodeImageProcessor(IMAGE_PATTERN, md)


class BBCodeUrlPattern(BBcodeProcessor, LinkInlineProcessor):
    def handleMatch(self, m, _):
        el = Element("a")

        if m.group("arg"):
            el.text = m.group("content")
            href = m.group("arg")
        else:
            el.text = m.group("content").strip()
            href = m.group("content")

        if href:
            el.set("href", self.unescape(href.strip()))
        else:
            el.set("href", "")

        return el, m.start("open"), m.end("close")


URL_PATTERN = r'(?P<open>(\[url=("?)(?P<arg>.*?)("?)\])|(\[url\]))(?P<content>.*?)(?P<close>\[/url\])'


def url(md):
    return BBCodeUrlPattern(URL_PATTERN, md)
