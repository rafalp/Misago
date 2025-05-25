import re
from functools import partial
from typing import Type

from django.db.models import Model

from ..markup import render_tokens_to_markup
from ..parse import parse


def update_attachments_markup_to_0_40(attachment_type: Type[Model], markup: str) -> str:
    tokens = parse(markup).tokens
    return render_tokens_to_markup(tokens)
