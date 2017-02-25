from django.test import TestCase

from misago.core.momentjs import clean_language_name, get_locale_url


class MomentJSTests(TestCase):
    def test_clean_language_name(self):
        """clean_language_name returns valid name"""
        TEST_CASES = [
            ('AF', 'af'),
            ('ar-SA', 'ar-sa'),
            ('de', 'de'),
            ('de-NO', 'de'),
            ('pl-pl', 'pl'),
            ('zz', None),
        ]

        for dirty, clean in TEST_CASES:
            self.assertEqual(clean_language_name(dirty), clean)

    def test_get_locale_path(self):
        """get_locale_path returns path to locale or null if it doesnt exist"""
        EXISTING_LOCALES = (
            'af', 'ar-sa', 'ar-sasa', 'de', 'et', 'pl', 'pl-pl', 'ru', 'pt-br', 'zh-tw'
        )

        for language in EXISTING_LOCALES:
            self.assertIsNotNone(get_locale_url(language))

        NONEXISTING_LOCALES = ('ga', 'en', 'en-us', 'martian', )

        for language in NONEXISTING_LOCALES:
            self.assertIsNone(get_locale_url(language))
