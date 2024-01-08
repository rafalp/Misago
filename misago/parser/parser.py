import re
from functools import cached_property


class Pattern:
    pattern: str

    def parse(self, parser: "Parser", match: str) -> dict:
        raise NotImplementedError()


class Paragraph(Pattern):
    pattern = r".+(\n.+)*"

    def parse(self, parser: "Parser", match: str) -> dict:
        return {"type": "paragraph", "children": parser.parse_inline(match)}


class LineBreak(Pattern):
    pattern = r"\n"

    def parse(self, parser: "Parser", match: str) -> dict:
        return {"type": "line_break"}


class Parser:
    block_patterns: list[Pattern]
    inline_patterns: list[Pattern]

    def __init__(
        self,
        block_patterns: list[Pattern] | None = None,
        inline_patterns: list[Pattern] | None = None,
    ):
        self.block_patterns = block_patterns or []
        self.inline_patterns = inline_patterns or []

    def __call__(self, markup: str) -> list[dict]:
        blocks = self.parse_blocks(markup)
        return blocks

    def parse_blocks(self, markup: str) -> list[dict]:
        result: list[dict] = []
        for m in self._block_re.finditer(markup):
            for key, pattern in self._final_block_patterns.items():
                block_match = m.group(key)
                if block_match is not None:
                    result.append(pattern.parse(self, block_match))
                    break

        return result

    def parse_inline(self, markup: str) -> list[dict]:
        result: list[dict] = []
        cursor = 0
        for m in self._inline_re.finditer(markup):
            for key, pattern in self._final_inline_patterns.items():
                block_match = m.group(key)
                if block_match is not None:
                    start = m.start()
                    if start > cursor:
                        result.append({"type": "text", "text": markup[cursor:start]})
                    result.append(pattern.parse(self, block_match))
                    cursor = m.end()
                    break

        if cursor < len(markup):
            result.append({"type": "text", "text": markup[cursor:]})

        return result

    def _parse(
        self, markup: str, patterns: dict[str, Pattern], pattern: re.Pattern
    ) -> list[dict]:
        result: list[dict] = []
        for m in pattern.finditer(markup):
            for key, pattern in patterns.items():
                block_match = m.group(key)
                if block_match is not None:
                    result.append(pattern.parse(self, block_match))
                    break

        return result

    @cached_property
    def _final_block_patterns(self) -> dict[str, Pattern]:
        patterns: list[Pattern] = self.block_patterns.copy()
        patterns.append(Paragraph())
        return {f"b_{i}": pattern for i, pattern in enumerate(patterns)}

    @cached_property
    def _block_re(self) -> re.Pattern:
        return self._build_re_pattern(self._final_block_patterns)

    @cached_property
    def _final_inline_patterns(self) -> dict[str, Pattern]:
        patterns: list[Pattern] = self.inline_patterns.copy()
        patterns += [LineBreak()]
        return {f"i_{i}": pattern for i, pattern in enumerate(patterns)}

    @cached_property
    def _inline_re(self) -> re.Pattern:
        return self._build_re_pattern(self._final_inline_patterns)

    def _build_re_pattern(self, patterns: dict[str, Pattern]) -> re.Pattern:
        return re.compile(
            "|".join(
                f"(?P<{key}>{pattern.pattern})" for key, pattern in patterns.items()
            ),
            re.IGNORECASE,
        )
