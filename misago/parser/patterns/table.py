from enum import StrEnum

from ..parser import Parser, Pattern

TABLE_PATTERN = (
    r"(\n|^)"  # Table is preceded by a new line or the start of the text
    r" *\|.+\n"  # Header row
    r" *(\| *:?-+:? *)+\|?"  # Header's underline
    r"(\n *\|.*)*"  # Remaining rows
)


class ColAlignment(StrEnum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


Cell = tuple[ColAlignment, str]


class TableMarkdown(Pattern):
    pattern_type: str = "table"
    pattern: str = TABLE_PATTERN

    def parse(self, parser: Parser, match: str, parents: list[str]) -> list[dict]:
        data = match.strip().splitlines()

        header = [c for c in self.split_row(data[0]) if c]
        cols = self.parse_cols_row(data[1])
        rows = [self.split_row(r) for r in data[2:]]

        if len(header) != len(cols):
            # TODO: return paragraph with text lines containing table markup
            return []

        ast = {"type": self.pattern_type}

        # TODO: return table AST

        return [ast]

    def parse_cols_row(self, row: str) -> list[ColAlignment]:
        cols: list[ColAlignment] = []
        for col in self.split_row(row):
            if col.startswith(":") and col.endswith(":"):
                cols.append(ColAlignment.CENTER)
            elif col.endswith(":"):
                cols.append(ColAlignment.RIGHT)
            else:
                cols.append(ColAlignment.LEFT)
        return cols

    def split_row(self, row: str) -> list[str]:
        row = row.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return [s.strip() for s in row.split("|")]
