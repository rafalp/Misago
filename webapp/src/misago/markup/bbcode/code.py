import re

import markdown
from markdown.extensions.fenced_code import FencedBlockPreprocessor


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
