import re
from xml.etree.ElementTree import SubElement

import markdown
from django.utils.crypto import get_random_string
from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor

QUOTE_START = get_random_string(32)
QUOTE_END = get_random_string(32)


class QuoteExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.preprocessors.register(QuotePreprocessor(md), "misago_bbcode_quote", 200)
        md.parser.blockprocessors.register(
            QuoteBlockProcessor(md.parser), "misago_bbcode_quote", 90
        )


class QuotePreprocessor(Preprocessor):
    QUOTE_BLOCK_RE = re.compile(
        r"""
\[quote\](?P<text>.*?)\[/quote\]
""".strip(),
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    QUOTE_BLOCK_TITLE_RE = re.compile(
        r"""
\[quote=("?)(?P<title>.*?)("?)](?P<text>.*?)\[/quote\]
""".strip(),
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    def run(self, lines):
        text = "\n".join(lines)
        while self.QUOTE_BLOCK_RE.search(text):
            text = self.QUOTE_BLOCK_RE.sub(self.replace, text)
        while self.QUOTE_BLOCK_TITLE_RE.search(text):
            text = self.QUOTE_BLOCK_TITLE_RE.sub(self.replace_titled, text)
        return text.split("\n")

    def replace(self, matchobj):
        text = matchobj.group("text")
        return "\n\n%s\n\n%s\n\n%s\n\n" % (QUOTE_START, text, QUOTE_END)

    def replace_titled(self, matchobj):
        title = matchobj.group("title").strip()
        text = matchobj.group("text")

        if title:
            return "\n\n%s%s\n\n%s\n\n%s\n\n" % (QUOTE_START, title, text, QUOTE_END)
        return "\n\n%s\n\n%s\n\n%s\n\n" % (QUOTE_START, text, QUOTE_END)


class QuoteBlockProcessor(BlockProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._title = None
        self._quote = 0
        self._children = []

    def test(self, parent, block):
        return block.strip().startswith(QUOTE_START) or self._quote

    def run(self, parent, blocks):
        block = blocks.pop(0)
        if block.strip().startswith(QUOTE_START):
            self._quote += 1
            if self._quote == 1:
                self._title = block[len(QUOTE_START) :].strip() or None

        self._children.append(block)

        if block.strip() == QUOTE_END:
            self._quote -= 1

        if not self._quote:
            children, self._children = self._children[1:-1], []
            title, self._title = self._title, None

            aside = SubElement(parent, "aside")
            aside.set("class", "quote-block")

            heading = SubElement(aside, "div")
            heading.set("class", "quote-heading")
            heading.set("data-noquote", "1")

            blockquote = SubElement(aside, "blockquote")
            blockquote.set("class", "quote-body")
            blockquote.set("data-block", "quote")

            if title:
                blockquote.set("data-author", title)

            if title:
                heading.text = title

            self.parser.parseBlocks(blockquote, children)
