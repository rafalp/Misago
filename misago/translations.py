import os
from typing import Dict

from babel.support import Translations

from .plugins import PluginsLoader, plugins_loader

LOCALE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locale")


class TranslationsLoader:
    _translations: Dict[str, Translations]
    _plugins_loader: PluginsLoader

    def __init__(self, plugins_loader: PluginsLoader):
        self._translations = {}
        self._plugins_loader = plugins_loader

    def load(self, locale: str):
        if locale not in self._translations:
            self._translations[locale] = self._load_translations(locale)

        return self._translations[locale]

    def _load_translations(self, locale: str):
        translations = Translations.load(LOCALE_DIR, locale)
        plugins_locales = self._plugins_loader.get_plugins_with_directory("locale")
        for _, locale_path in plugins_locales:
            plugin_translations = Translations.load(locale_path, locale)
            translations.merge(plugin_translations)
        return translations


translations = TranslationsLoader(plugins_loader)
