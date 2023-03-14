import re
from xml.etree.ElementTree import SubElement

import markdown
from django.utils.crypto import get_random_string
from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor

SPOILER_START = get_random_string(32)
SPOILER_END = get_random_string(32)


class SpoilerExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.preprocessors.register(SpoilerPreprocessor(md), "misago_bbcode_spoiler", 200)
        md.parser.blockprocessors.register(
            SpoilerBlockProcessor(md.parser), "misago_bbcode_spoiler", 85
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

            aside = SubElement(parent, "aside")
            aside.set("class", "spoiler-block")

            blockquote = SubElement(aside, "blockquote")
            blockquote.set("class", "spoiler-body")
            blockquote.set("data-block", "spoiler")

            overlay = SubElement(aside, "div")
            overlay.set("class", "spoiler-overlay")
            overlay.set("data-noquote", "1")

            reveal_btn = SubElement(overlay, "button")
            reveal_btn.set("class", "spoiler-reveal")
            reveal_btn.set("type", "button")

            self.parser.parseBlocks(blockquote, children)
