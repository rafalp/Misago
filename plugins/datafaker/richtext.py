import random

from misago.richtext import get_block_id
from misago.types import RichText, RichTextBlock

from .sentences import Sentences


sentences = Sentences(max_length=200)


def create_fake_rich_text(depth: int = 0) -> RichText:
    rich_text: RichText = []

    for _ in range(random.randint(1, 30)):
        dice_roll = random.randint(0, 100)
        if dice_roll > 95:
            if depth < 5:
                rich_text.append(create_fake_rich_text_quote(depth + 1))
            else:
                rich_text.append(create_fake_rich_text_paragraph())
        elif dice_roll > 80:
            rich_text.append(create_fake_rich_text_header())
        elif dice_roll > 70:
            rich_text.append(create_fake_rich_text_list())
        else:
            rich_text.append(create_fake_rich_text_paragraph())

    return rich_text


def create_fake_rich_text_header() -> RichTextBlock:
    text = " ".join(sentences.get_random_sentences(random.randint(1, 2)))
    return {
        "id": get_block_id(),
        "type": "h%s" % random.randint(1, 6),
        "text": text,
    }


def create_fake_rich_text_paragraph() -> RichTextBlock:
    text = " ".join(sentences.get_random_sentences(random.randint(1, 8)))
    return {
        "id": get_block_id(),
        "type": "p",
        "text": text,
    }


def create_fake_rich_text_quote(depth: int = 0) -> RichTextBlock:
    return {
        "id": get_block_id(),
        "type": "quote",
        "author": None,
        "post": None,
        "children": create_fake_rich_text(depth),
    }


def create_fake_rich_text_list(depth: int = 0) -> RichTextBlock:
    children = []
    for _ in range(random.randint(2, 10)):
        if depth == 0 and random.randint(1, 10) == 10:
            children.append(
                {
                    "id": get_block_id(),
                    "type": "li",
                    "children": [create_fake_rich_text_list(depth + 1)],
                }
            )
        else:
            children.append(
                {
                    "id": get_block_id(),
                    "type": "li",
                    "children": [
                        {
                            "id": get_block_id(),
                            "type": "f",
                            "text": sentences.get_random_sentence(),
                        }
                    ],
                }
            )

    return {
        "id": get_block_id(),
        "type": "list",
        "ordered": random.choice((True, False)),
        "children": children,
    }
