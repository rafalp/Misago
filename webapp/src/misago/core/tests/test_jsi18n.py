import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

MISAGO_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
LOCALES_DIR = os.path.join(MISAGO_DIR, "locale")


class JsI18nUrlTests(TestCase):
    def test_url_cache_buster(self):
        """js i18n catalog link has cachebuster with lang code"""
        url = "%s?%s" % (reverse("django-i18n"), settings.LANGUAGE_CODE)

        response = self.client.get(reverse("misago:index"))
        self.assertContains(response, url)

    def test_js_catalogs_are_correct(self):
        """no JS catalogs have showstoppers"""
        failed_languages = []
        for language in os.listdir(LOCALES_DIR):
            if "." in language:
                continue
            try:
                with translation.override(language):
                    response = self.client.get(reverse("django-i18n"))
                    if response.status_code != 200:
                        failed_languages.append(language)
            except Exception:  # pylint: disable=broad-except
                failed_languages.append(language)

        if failed_languages:
            self.fail(
                "JS catalog failed for languages: %s" % (", ".join(failed_languages))
            )
