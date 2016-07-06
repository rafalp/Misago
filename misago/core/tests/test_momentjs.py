from django.conf import settings
from django.test import TestCase

from misago.core.momentjs import get_locale_path, list_available_locales


class MomentJSTests(TestCase):
    def test_list_available_locales(self):
        """list_available_locales returns list of locales"""
        TEST_CASES = (
            'af',
            'ar-sa',
            'de',
            'et',
            'pl',
            'ru',
            'pt-br',
            'zh-tw'
        )

        locales = list_available_locales().keys()

        for language in TEST_CASES:
            self.assertIn(language, locales)

    def test_get_locale_path(self):
        """get_locale_path returns path to locale or null if it doesnt exist"""
        EXISTING_LOCALES = (
            'af',
            'ar-sa',
            'ar-sasa',
            'de',
            'et',
            'pl',
            'pl-pl',
            'ru',
            'pt-br',
            'zh-tw'
        )

        for language in EXISTING_LOCALES:
            self.assertIsNotNone(get_locale_path(language))

        NONEXISTING_LOCALES = (
            'ga',
            'en',
            'en-us',
            'martian',
        )

        for language in NONEXISTING_LOCALES:
            self.assertIsNone(get_locale_path(language))
