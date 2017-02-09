from misago.conf import settings


MOMENT_STATIC_PATH = 'misago/momentjs/{}.js'


def get_locale_url(language):
    clean_language = clean_language_name(language)
    if clean_language:
        return MOMENT_STATIC_PATH.format(clean_language)

    return None


def clean_language_name(language):
    # lowercase language
    language = language.lower()

    # first try: literal match
    if language in settings.MISAGO_MOMENT_JS_LOCALES:
        return language

    # second try: fallback to macrolanguage
    language = language.split('-')[0]
    if language in settings.MISAGO_MOMENT_JS_LOCALES:
        return language

    # nothing was found
    return None
