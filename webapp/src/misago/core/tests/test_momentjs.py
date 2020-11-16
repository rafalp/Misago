from django.test import override_settings

from ..momentjs import clean_language_name, get_locale_url


def test_django_language_code_is_cleaned_for_moment_js():
    assert clean_language_name("en", ["en"]) == "en"


def test_two_part_django_language_code_is_cleaned_for_moment_js():
    assert clean_language_name("en_us", ["en-us"]) == "en-us"


def test_two_part_django_language_code_is_fallbacked_to_single_part_code():
    assert clean_language_name("en_us", ["en", "en-uk"]) == "en"


def test_django_language_code_cleanup_is_case_insensitive():
    assert clean_language_name("en_US", ["en-us"]) == "en-us"


def test_django_language_code_is_cleaned_to_none_if_translation_is_not_available():
    assert clean_language_name("pl", ["en"]) is None


def test_locale_url_getter_uses_passed_locales_list():
    with override_settings(MISAGO_MOMENT_JS_LOCALES=["en-us"]):
        assert get_locale_url("en_us", locales=["en"]).endswith("en.js")


def test_locale_url_getter_fallbacks_to_locales_setting_if_locales_kwarg_is_not_set():
    with override_settings(MISAGO_MOMENT_JS_LOCALES=["en-us"]):
        assert get_locale_url("en_us").endswith("en-us.js")


def test_locale_url_getter_uses_passed_static_path_template():
    locale_url = get_locale_url(
        "en_us", static_path_template="test/%s", locales=["en-us"]
    )
    assert locale_url == "test/en-us"


def test_locale_url_getter_returns_none_for_unsupported_locale():
    assert get_locale_url("pl", locales=["en"]) is None
