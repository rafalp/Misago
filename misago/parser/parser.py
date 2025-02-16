import re
from functools import cached_property
from typing import Callable

from django.utils.crypto import get_random_string


class Pattern:
    pattern_type: str
    pattern: str

    def parse(
        self, parser: "Parser", match: str, parents: list[str]
    ) -> dict | list[dict]:
        raise NotImplementedError()


class LineBreak(Pattern):
    pattern_type = "line-break"
    pattern = r" *\n *"

    def parse(self, parser: "Parser", match: str, parents: list[str]) -> dict:
        return {"type": self.pattern_type}


class Parser:
    block_patterns: list[Pattern]
    inline_patterns: list[Pattern]
    post_processors: list[Callable[["Parser", list[dict]], list[dict]]]

    reserve_inline_code = re.compile(r"`*`(.|\n)+?``*")
    _reserved_patterns: dict[str, str]

    _paragraph_re = re.compile(r".+(\n.+)*")

    def __init__(
        self,
        block_patterns: list[Pattern] | None = None,
        inline_patterns: list[Pattern] | None = None,
        post_processors: (
            list[Callable[["Parser", list[dict]], list[dict]]] | None
        ) = None,
    ):
        self.block_patterns = block_patterns or []
        self.inline_patterns = inline_patterns or []
        self.post_processors = post_processors or []

        self._reserved_patterns = {}

    def __call__(self, markup: str) -> list[dict]:
        markup = self.normalize_newlines(markup)
        markup = self.reserve_patterns(markup)
        ast = self.parse_blocks(markup, [])
        for post_processor in self.post_processors:
            ast = post_processor(self, ast)
        return ast

    def normalize_newlines(self, markup: str) -> str:
        return markup.replace("\r\n", "\n").replace("\r", "\n")

    def reserve_patterns(self, markup: str) -> str:
        if not "`" in markup:
            return markup

        def replace_pattern(match):
            match_str = match.group(0)
            if match_str.startswith("``") or match_str.endswith("``"):
                return match_str

            pattern_id = f"%%{get_random_string(12)}%%"
            while pattern_id in markup or pattern_id in self._reserved_patterns:
                pattern_id = f"%%{get_random_string(12)}%%"

            self._reserved_patterns[pattern_id] = match_str
            return pattern_id

        return self.reserve_inline_code.sub(replace_pattern, markup)

    def reverse_reservations(self, value: str) -> str:
        if not self._reserved_patterns or "%%" not in value:
            return value

        for pattern, org in self._reserved_patterns.items():
            value = value.replace(pattern, org)
        return value

    def parse_blocks(self, markup: str, parents: list[str]) -> list[dict]:
        cursor = 0

        result: list[dict] = []
        for m in self._block_re.finditer(markup):
            for key, pattern in self._final_block_patterns.items():
                block_match = m.group(key)
                if block_match is not None:
                    start = m.start()
                    if start > cursor:
                        result += self.parse_paragraphs(markup[cursor:start], parents)

                    block_ast = pattern.parse(self, block_match, parents)
                    if isinstance(block_ast, list):
                        result += block_ast
                    elif isinstance(block_ast, dict):
                        result.append(block_ast)

                    cursor = m.end()
                    break

        if cursor < len(markup):
            result += self.parse_paragraphs(markup[cursor:], parents)

        return result

    def parse_paragraphs(self, markup: str, parents: list[str]) -> list[dict]:
        markup = markup.strip()

        if not markup:
            return []

        parents = parents + ["paragraph"]

        result: list[dict] = []
        for m in self._paragraph_re.finditer(markup):
            result.append(
                {
                    "type": "paragraph",
                    "children": self.parse_inline(
                        m.group(0).strip(), parents, reverse_reservations=True
                    ),
                }
            )
        return result

    def parse_inline(
        self,
        markup: str,
        parents: list[str],
        reverse_reservations: bool = False,
    ) -> list[dict]:
        if reverse_reservations:
            markup = self.reverse_reservations(markup)

        cursor = 0

        result: list[dict] = []
        for m in self._inline_re.finditer(markup):
            for key, pattern in self._final_inline_patterns.items():
                block_match = m.group(key)
                if block_match is not None:
                    start = m.start()
                    if start > cursor:
                        if result and result[-1]["type"] == "text":
                            result[-1]["text"] += markup[cursor:start]
                        else:
                            result.append(
                                {"type": "text", "text": markup[cursor:start]}
                            )

                    inline_ast = pattern.parse(self, block_match, parents)
                    if isinstance(inline_ast, list):
                        for child in inline_ast:
                            if (
                                result
                                and child["type"] == "text"
                                and result[-1]["type"] == "text"
                            ):
                                result[-1]["text"] += child["text"]
                            else:
                                result.append(child)

                    elif isinstance(inline_ast, dict):
                        if (
                            result
                            and inline_ast["type"] == "text"
                            and result[-1]["type"] == "text"
                        ):
                            result[-1]["text"] += inline_ast["text"]
                        else:
                            result.append(inline_ast)

                    cursor = m.end()
                    break

        if cursor < len(markup):
            if result and result[-1]["type"] == "text":
                result[-1]["text"] += markup[cursor:]
            else:
                result.append({"type": "text", "text": markup[cursor:]})

        return result

    @cached_property
    def _final_block_patterns(self) -> dict[str, Pattern]:
        patterns: list[Pattern] = self.block_patterns.copy()
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
