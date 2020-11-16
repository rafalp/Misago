from ..conf import settings

MOMENT_STATIC_PATH = "misago/momentjs/%s.js"


def get_locale_url(language, *, static_path_template=None, locales=None):
    locales = locales or settings.MISAGO_MOMENT_JS_LOCALES
    clean_language = clean_language_name(language, locales)
    if clean_language:
        static_path_template = static_path_template or MOMENT_STATIC_PATH
        return static_path_template % clean_language


def clean_language_name(language, locales):
    # lowercase language
    language = language.lower().replace("_", "-")

    # first try: literal match
    if language in locales:
        return language

    # second try: fallback to macrolanguage
    language = language.split("-")[0]
    if language in locales:
        return language

    # nothing was found
    return None
