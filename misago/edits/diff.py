from dataclasses import dataclass
from difflib import ndiff


@dataclass
class TextDiff:
    lines: list[dict]
    added: int
    removed: int


def diff_text(before: str, after: str) -> TextDiff:
    raw_diff = ndiff(before.splitlines(), after.splitlines())
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
    diff_lines = cleanup_lines(diff_lines)
    diff_lines = add_lines_numbers(diff_lines)

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
    if not dst["diff"]:
        # Fast path for simple line diff
        return {
            "marker": "?",
            "diff": [
                {"marker": block["marker"], "text": block["text"]}
                for block in split_src_line_blocks(src)
            ],
        }

    src_blocks: list[dict] = split_src_line_blocks(src)
    dst_blocks: list[dict] = split_dst_line_blocks(dst)

    src_map: dict[int, dict] = {block["index"]: block for block in src_blocks}
    dst_map: dict[int, dict] = {block["index"]: block for block in dst_blocks}

    diff: list[dict] = []
    start = 0
    end = max(len(src["text"]), len(dst["text"]))

    while start < end:
        try:
            src_block = src_map[start]
        except KeyError:
            src_block = None
        try:
            dst_block = dst_map[start]
        except KeyError:
            dst_block = None

        if dst_block:
            if src_block and src_block["marker"] is not None:
                diff.append(
                    {
                        "marker": src_block["marker"],
                        "text": src_block["text"],
                    }
                )
            diff.append(
                {
                    "marker": dst_block["marker"],
                    "text": dst_block["text"],
                }
            )
        elif src_block and src_block["marker"] is not None:
            diff.append(
                {
                    "marker": src_block["marker"],
                    "text": src_block["text"],
                }
            )
        start += 1

    return {
        "marker": "?",
        "diff": diff,
    }


def split_src_line_blocks(src: dict) -> list[dict]:
    return split_line_blocks(src, "removed", "-")


def split_dst_line_blocks(dst: dict) -> list[dict]:
    return split_line_blocks(dst, "added", "+")


def split_line_blocks(line: dict, source: str, marker: str) -> list[dict]:
    blocks: list[dict] = []

    for i, c in enumerate(line["text"]):
        if i in line[source] or i in line["changed"]:
            block_marker = marker
        else:
            block_marker = None

        if not blocks or blocks[-1]["marker"] != block_marker:
            blocks.append(
                {
                    "index": i,
                    "marker": block_marker,
                    "text": c,
                    "length": 1,
                }
            )
        else:
            blocks[-1]["text"] += c
            blocks[-1]["length"] += 1

    return merge_close_diff_blocks(blocks)


def merge_close_diff_blocks(blocks: list[dict], distance: int = 2) -> list[dict]:
    last_block = len(blocks) - 1
    merged_blocks: list[dict] = []

    for i, block in enumerate(blocks):
        if (
            merged_blocks
            and block["marker"] is None
            and block["length"] <= distance
            and i < last_block
        ):
            merged_blocks[-1]["text"] += block["text"]
            merged_blocks[-1]["length"] += block["length"]
        elif merged_blocks and merged_blocks[-1]["marker"] == block["marker"]:
            merged_blocks[-1]["text"] += block["text"]
            merged_blocks[-1]["length"] += block["length"]
        else:
            merged_blocks.append(block)

    return merged_blocks


def cleanup_lines(lines: list[dict]) -> list[dict]:
    new_lines: list[dict] = []
    for line in lines:
        if line["marker"] == "?":
            new_lines.append(line)
        else:
            new_lines.append({"marker": line["marker"], "text": line["text"]})

    return new_lines


def add_lines_numbers(lines: list[dict]) -> list[dict]:
    for i, line in enumerate(lines, 1):
        line["number"] = i
    return lines
