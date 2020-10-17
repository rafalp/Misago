import json
import mistune
from ..types import RichText
from ..utils.strings import get_random_string


def parse_markup(markup: str) -> RichText:
    richtext: RichText = []
    for block in markup.splitlines():
        clean_text = block.strip()
        if clean_text:
            richtext.append(
                {"id": get_random_string(6), "type": "p", "text": block.strip()}
            )

    return richtext


def make_html(markup: str) -> str:
    return mistune.html(markup)


def make_json(markup: str) -> str:
    return json.dumps(markup)
