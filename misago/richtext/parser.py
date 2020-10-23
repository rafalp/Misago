import json
from ..markdown import markdown
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


def render_richtext_as_html(richtext: RichText) -> str:
    html_list = []
    for row in richtext:
        if row["type"] == "p":
            html_list.append(markdown(row['text']))

    return ''.join(html_list)


def make_json(markup: str) -> str:
    return json.dumps(markup)
