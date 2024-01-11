from ..parser import Parser


class BlockPostProcessor:
    type_open: str
    type_close: str

    def __call__(self, parser: Parser, ast: list[dict]) -> list[dict]:
        return ast
