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
    diff_lines = merge_lines_diff_data(diff_lines)

    added = 0
    removed = 0
    for line in diff_lines:
        if line["marker"] == "+":
            added += 1
        elif line["marker"] == "-":
            removed += 1

    diff_lines = merge_changed_lines(diff_lines)

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


def merge_lines_diff_data(lines: list[dict]) -> list[dict]:
    new_lines: list[dict] = []
    for line in lines:
        if line["marker"] == "?":
            new_lines[-1].update(
                {
                    "diff": bool(line["changed"] or line["added"] or line["removed"]),
                    "changed": line["changed"],
                    "added": line["added"],
                    "removed": line["removed"],
                }
            )
        else:
            line["diff"] = False
            line["changed"] = []
            line["added"] = []
            line["removed"] = []
            new_lines.append(line)

    return new_lines


def merge_changed_lines(lines: list[dict]) -> list[dict]:
    new_lines: list[dict] = []
    for line in lines:
        if (
            line["marker"] == "+"
            and new_lines
            and new_lines[-1]["marker"] == "-"
            and (line["diff"] or new_lines[-1]["diff"])
        ):
            new_lines[-1] = combine_two_lines(new_lines[-1], line)
        else:
            new_lines.append(line)

    return new_lines


def combine_two_lines(src: dict, dst: dict) -> dict:
    if src["diff"] and dst["diff"]:
        pass  # Update src with changes from diff
    if src["diff"]:
        pass  # 
    if dst["diff"]:
        pass
