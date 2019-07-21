import re

import markdown
from django.utils.crypto import get_random_string
from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor
from markdown.util import etree

SPOILER_START = get_random_string(32)
SPOILER_END = get_random_string(32)


class SpoilerExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.preprocessors.add("misago_bbcode_spoiler", SpoilerPreprocessor(md), "_end")
        md.parser.blockprocessors.add(
            "misago_bbcode_spoiler", SpoilerBlockProcessor(md.parser), ">code"
        )


class SpoilerPreprocessor(Preprocessor):
    SPOILER_BLOCK_RE = re.compile(
        r"""
\[spoiler\](?P<text>.*?)\[/spoiler\]
""".strip(),
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    def run(self, lines):
        text = "\n".join(lines)
        while self.SPOILER_BLOCK_RE.search(text):
            text = self.SPOILER_BLOCK_RE.sub(self.replace, text)
        return text.split("\n")

    def replace(self, matchobj):
        text = matchobj.group("text")
        return "\n\n%s\n\n%s\n\n%s\n\n" % (SPOILER_START, text, SPOILER_END)


class SpoilerBlockProcessor(BlockProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._spoiler = 0
        self._children = []

    def test(self, parent, block):
        return block.strip().startswith(SPOILER_START) or self._spoiler

    def run(self, parent, blocks):
        block = blocks.pop(0)
        if block.strip().startswith(SPOILER_START):
            self._spoiler += 1

        self._children.append(block)

        if block.strip() == SPOILER_END:
            self._spoiler -= 1

        if not self._spoiler:
            children, self._children = self._children[1:-1], []

            aside = etree.SubElement(parent, "aside")
            aside.set("class", "spoiler-block")

            blockquote = etree.SubElement(aside, "blockquote")
            blockquote.set("class", "spoiler-body")

            overlay = etree.SubElement(aside, "div")
            overlay.set("class", "spoiler-overlay")

            reveal_btn = etree.SubElement(overlay, "button")
            reveal_btn.set("class", "spoiler-reveal")
            reveal_btn.set("type", "button")

            self.parser.parseBlocks(blockquote, children)
