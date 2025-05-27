# Source: https://github.com/executablebooks/markdown-it-py/blob/36a9d146af52265420de634cc2e25d1d40cfcdb7/markdown_it/rules_inline/escape.py#L60C1
ESCAPED_CHARACTERS = {
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "{",
    "|",
    "}",
    "~",
}


def escape(value: str, characters: str | None = None) -> str:
    escaped_characters = "\\" + characters if characters else ESCAPED_CHARACTERS

    result = ""
    for c in value:
        if c in escaped_characters:
            result += "\\"
        result += c
    return result


def unescape(value: str) -> str:
    result = ""

    pos = 0
    maximum = len(value)
    while pos < maximum:
        if (
            value[pos] == "\\"
            and pos + 1 < maximum
            and value[pos + 1] in ESCAPED_CHARACTERS
        ):
            result += value[pos + 1]
            pos += 2
        else:
            result += value[pos]
            pos += 1

    return result
