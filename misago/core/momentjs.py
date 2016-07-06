import os

from path import Path


__all__ = ['list_available_locales', 'get_locale_path']


def list_available_locales():
    misago_dir = os.path.dirname(os.path.dirname(__file__))
    locales_dir = os.path.join(
        misago_dir, os.path.join(misago_dir, 'locale'), 'momentjs')

    locales = {}

    for locale in Path(locales_dir).files('*.js'):
        locales[locale.basename()[:-3]] = locale

    return locales


def get_locale_path(language):
    locales = list_available_locales()

    # first try: literal match
    if language in locales:
        return locales[language]

    # second try: fallback to macrolanguage
    language = language.split('-')[0]
    if language in locales:
        return locales[language]

    # nothing was found
    return None
