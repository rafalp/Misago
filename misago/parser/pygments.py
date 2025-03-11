from typing import Iterable

from django.conf import settings
from pygments.lexers import get_all_lexers


def get_pygments_options(
    enabled_languages: Iterable[str] | bool,
) -> tuple[set[str], tuple[tuple[str, str], ...], dict[str, str]]:
    languages: list[str] = []
    choices: list[tuple[str, str]] = []
    names: dict[str, str] = {}

    for lexer in get_all_lexers():
        name, aliases = lexer[:2]
        if not aliases:
            continue

        if enabled_languages is True or (
            isinstance(enabled_languages, (list, tuple))
            and aliases[0] in enabled_languages
        ):
            languages.extend(aliases)
            choices.append((aliases[0], name))

            for alias in aliases:
                names[alias] = name

    return set(languages), tuple(choices), names


PYGMENTS_LANGUAGES: set[str] = set()
PYGMENTS_CHOICES: tuple[tuple[str, str], ...] = ()
PYGMENTS_NAMES: dict[str, str] = {}

if settings.MISAGO_PYGMENTS_LANGUAGES is True or isinstance(
    settings.MISAGO_PYGMENTS_LANGUAGES, (list, tuple)
):
    PYGMENTS_LANGUAGES, PYGMENTS_CHOICES, PYGMENTS_NAMES = get_pygments_options(
        settings.MISAGO_PYGMENTS_LANGUAGES
    )
