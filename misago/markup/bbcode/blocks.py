import re

import markdown
from django.utils.crypto import get_random_string
from markdown.blockprocessors import BlockProcessor, HRProcessor
from markdown.extensions.fenced_code import FencedBlockPreprocessor
from markdown.preprocessors import Preprocessor
from markdown.util import etree

QUOTE_START = get_random_string(32)
QUOTE_END = get_random_string(32)


class BBCodeHRProcessor(HRProcessor):
    RE = r"^\[hr\]*"

    # Detect hr on any line of a block.
    SEARCH_RE = re.compile(RE, re.MULTILINE | re.IGNORECASE)


class QuoteExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.preprocessors.add("misago_bbcode_quote", QuotePreprocessor(md), "_end")
        md.parser.blockprocessors.add(
            "misago_bbcode_quote", QuoteBlockProcessor(md.parser), ">code"
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

            aside = etree.SubElement(parent, "aside")
            aside.set("class", "quote-block")

            heading = etree.SubElement(aside, "div")
            heading.set("class", "quote-heading")

            blockquote = etree.SubElement(aside, "blockquote")
            blockquote.set("class", "quote-body")

            if title:
                heading.text = title

            self.parser.parseBlocks(blockquote, children)


class CodeBlockExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.preprocessors.add(
            "misago_code_bbcode", CodeBlockPreprocessor(md), ">normalize_whitespace"
        )


class CodeBlockPreprocessor(FencedBlockPreprocessor):
    FENCED_BLOCK_RE = re.compile(
        r"""
\[code(=("?)(?P<lang>.*?)("?))?](([ ]*\n)+)?(?P<code>.*?)((\s|\n)+)?\[/code\]
""",
        re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE,
    )
