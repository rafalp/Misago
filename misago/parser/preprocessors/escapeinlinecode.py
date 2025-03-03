from ..parser import Parser


def escape_inline_code(parser: Parser, markup: str) -> str:
    if not "`" in markup:
        return markup

    def replace_pattern(match):
        match_str = match.group(0)
        if match_str.startswith("``") or match_str.endswith("``"):
            return match_str

        placeholder = parser.get_unique_placeholder(markup)
        parser.string_placeholders[placeholder] = match_str[1:-1]
        return f"`{placeholder}`"

    return parser.inline_code.sub(replace_pattern, markup)
