from __future__ import unicode_literals

import re

from django.utils.crypto import get_random_string
import markdown
from markdown.blockprocessors import BlockProcessor, HRProcessor
from markdown.preprocessors import Preprocessor
from markdown.util import etree


QUOTE_START = get_random_string(32)
QUOTE_END = get_random_string(32)


class BBCodeHRProcessor(HRProcessor):
    RE = r'^\[hr\]*'

    # Detect hr on any line of a block.
    SEARCH_RE = re.compile(RE, re.MULTILINE | re.IGNORECASE)


class QuoteExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.preprocessors.add('misago_bbcode_quote', QuotePreprocessor(md), '_end')
        md.parser.blockprocessors.add('misago_bbcode_quote', QuoteBlockProcessor(md.parser), '>code')


class QuotePreprocessor(Preprocessor):
    QUOTE_BLOCK_RE = re.compile(r'''
\[quote\](?P<text>.*?)\[/quote\]
'''.strip(), re.IGNORECASE | re.MULTILINE | re.DOTALL);
    QUOTE_BLOCK_AUTHORED_RE = re.compile(r'''
\[quote=("?)(@?)(?P<author>[0-9a-zA-Z]+)("?)](?P<text>.*?)\[/quote\]
'''.strip(), re.IGNORECASE | re.MULTILINE | re.DOTALL);


    def run(self, lines):
        text = '\n'.join(lines)
        while self.QUOTE_BLOCK_RE.search(text):
            text = self.QUOTE_BLOCK_RE.sub(self.replace, text)
        while self.QUOTE_BLOCK_AUTHORED_RE.search(text):
            text = self.QUOTE_BLOCK_AUTHORED_RE.sub(self.replace_authored, text)
        return text.split('\n')

    def replace(self, matchobj):
        text = matchobj.group('text')
        return '\n\n{}\n\n{}\n\n{}\n\n'.format(QUOTE_START, text, QUOTE_END)

    def replace_authored(self, matchobj):
        author = matchobj.group('author').lstrip('@').strip()
        text = matchobj.group('text')

        if author:
            return '\n\n{}{}\n\n{}\n\n{}\n\n'.format(QUOTE_START, author, text, QUOTE_END)
        else:
            return '\n\n{}\n\n{}\n\n{}\n\n'.format(QUOTE_START, text, QUOTE_END)


class QuoteBlockProcessor(BlockProcessor):
    def __init__(self, *args, **kwargs):
        super(QuoteBlockProcessor, self).__init__(*args, **kwargs)
        self._author = None
        self._quote = 0
        self._children = []

    def test(self, parent, block):
        return block.strip().startswith(QUOTE_START) or self._quote

    def run(self, parent, blocks):
        block = blocks.pop(0)
        if block.strip().startswith(QUOTE_START):
            self._quote += 1
            if self._quote == 1:
                self._author = block[len(QUOTE_START):].strip() or None

        self._children.append(block)

        if block.strip() == QUOTE_END:
            self._quote -= 1

        if not self._quote:
            children, self._children = self._children[1:-1], []
            author, self._author = self._author, None

            blockquote = etree.SubElement(parent, 'blockquote')
            header = etree.SubElement(blockquote, 'header')
            if author:
                header.text = '@{}'.format(author)

            self.parser.parseBlocks(blockquote, children)
