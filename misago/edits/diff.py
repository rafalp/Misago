from dataclasses import dataclass
from difflib import ndiff


@dataclass
class TextDiff:
    lines: list[dict]
    added: int
    removed: int


def diff_text(before: str, after: str) -> TextDiff:
    raw_diff = ndiff(before.splitlines(keepends=True), after.splitlines(keepends=True))
    diff_lines = list(map(parse_diff_line, raw_diff))

    added = 0
    removed = 0
    for line in diff_lines:
        if line["marker"] == "+":
            added += 1
        elif line["marker"] == "-":
            removed += 1

    return TextDiff(
        lines=diff_lines,
        added=added,
        removed=removed,
    )


def parse_diff_line(line: str) -> dict:
    marker = line[0]
    text = line[2:]

    if marker == "+":
        return {"marker": "+", "text": text}
    elif marker == "-":
        return {"marker": "-", "text": text}
    elif marker == "?":
        changed = []
        added = []
        removed = []
        for i, c in enumerate(text.rstrip()):
            if c == "^":
                changed.append(i)
            elif c == "+":
                added.append(i)
            elif c == "-":
                removed.append(i)
        return {"marker": "?", "changed": changed, "added": added, "removed": removed}
    else:
        return {"marker": None, "text": text}
