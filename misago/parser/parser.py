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
    escaped_characters = "\\!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~"

    character_placeholders: dict[str, str]
    string_placeholders: dict[str, str]
    placeholder_length = 16

    block_patterns: list[Pattern]
    inline_patterns: list[Pattern]
    pre_processors: list[Callable[["Parser", str], str]]
    post_processors: list[Callable[["Parser", list[dict]], list[dict]]]

    inline_code = re.compile(r"(?<!`)`.+?(\n.+?)*?`(?!`)")
    paragraph = re.compile(r".+(\n.+)*")

    def __init__(
        self,
        block_patterns: list[Pattern] | None = None,
        inline_patterns: list[Pattern] | None = None,
        pre_processors: list[Callable[["Parser", str], str]] | None = None,
        post_processors: (
            list[Callable[["Parser", list[dict]], list[dict]]] | None
        ) = None,
    ):
        self.character_placeholders = {}
        self.string_placeholders = {}

        self.block_patterns = block_patterns or []
        self.inline_patterns = inline_patterns or []
        self.pre_processors = pre_processors or []
        self.post_processors = post_processors or []

        self._reserved_patterns = {}

    def __call__(self, markup: str) -> list[dict]:
        markup = self.normalize_newlines(markup)
        markup = self.escape(markup)

        for pre_processor in self.pre_processors:
            markup = pre_processor(self, markup)

        ast = self.parse_blocks(markup, [])

        for post_processor in self.post_processors:
            ast = post_processor(self, ast)

        return ast

    def normalize_newlines(self, markup: str) -> str:
        return markup.replace("\r\n", "\n").replace("\r", "\n")

    def escape(self, text: str) -> str:
        if not text:
            return ""

        return self.escape_special_characters(text)

    def unescape(self, text: str) -> str:
        if not text:
            return ""

        text = self.replace_string_placeholders(text)
        text = self.replace_character_placeholders(text)

        return text

    def escape_special_characters(self, markup: str) -> str:
        for character in self.escaped_characters:
            escaped_character = f"\\{character}"
            if escaped_character in markup:
                placeholder = self.get_unique_placeholder(markup)
                self.character_placeholders[character] = placeholder
                markup = markup.replace(escaped_character, placeholder)

        return markup

    def replace_character_placeholders(self, text: str) -> str:
        for value, placeholder in reversed(self.character_placeholders.items()):
            if placeholder in text:
                text = text.replace(placeholder, value)
        return text

    def replace_string_placeholders(self, text: str) -> str:
        for placeholder, string in self.string_placeholders.items():
            if placeholder in text:
                text = text.replace(placeholder, string)
        return text

    def get_unique_placeholder(self, text: str) -> str:
        placeholder = ""
        while placeholder in text:
            placeholder = get_random_string(self.placeholder_length)
        return placeholder

    def text_ast(self, text: str, unescape: bool = True) -> dict:
        if unescape:
            text = self.unescape(text)

        return {"type": "text", "text": text}

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
        for m in self.paragraph.finditer(markup):
            result.append(
                {
                    "type": "paragraph",
                    "children": self.parse_inline(m.group(0).strip(), parents),
                }
            )
        return result

    def parse_inline(
        self,
        markup: str,
        parents: list[str],
    ) -> list[dict]:
        cursor = 0

        result: list[dict] = []
        for m in self._inline_re.finditer(markup):
            for key, pattern in self._final_inline_patterns.items():
                block_match = m.group(key)
                if block_match is not None:
                    start = m.start()
                    if start > cursor:
                        if result and result[-1]["type"] == "text":
                            result[-1]["text"] += self.unescape(markup[cursor:start])
                        else:
                            result.append(self.text_ast(markup[cursor:start]))

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
                result[-1]["text"] += self.unescape(markup[cursor:])
            else:
                result.append(self.text_ast(markup[cursor:]))

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
