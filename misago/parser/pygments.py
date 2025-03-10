from typing import Iterable

from django.conf import settings
from pygments.lexers import get_all_lexers


def get_pygments_options(
    enable_languages: Iterable[str] | bool,
) -> tuple[dict[str, str], set[str]]:
    languages: list[str] = []
    choices: list[tuple[str, str]] = []

    for lexer in get_all_lexers():
        name, aliases = lexer[:2]
        if not aliases:
            continue

        if enable_languages is True or (
            isinstance(enable_languages, (list, tuple))
            and aliases[0] in enable_languages
        ):
            languages.extend(aliases)
            choices.append((name, aliases[0]))

    return set(languages), tuple(choices)


PYGMENTS_LANGUAGES: set[str] = set()
PYGMENTS_CHOICES: tuple[tuple[str, str], ...] = ()

if settings.MISAGO_PARSER_PYGMENTS_LANGUAGES is True or isinstance(
    settings.MISAGO_PARSER_PYGMENTS_LANGUAGES, (list, tuple)
):
    PYGMENTS_LANGUAGES, PYGMENTS_CHOICES = get_pygments_options(
        settings.MISAGO_PARSER_PYGMENTS_LANGUAGES
    )
