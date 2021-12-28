import os
from typing import Dict

from babel.support import Translations

from .plugins import PluginLoader, plugins

LOCALE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locale")


class TranslationsLoader:
    _translations: Dict[str, Translations]
    _plugin_laader: PluginLoader

    def __init__(self, plugin_loader: PluginLoader):
        self._translations = {}
        self._plugin_laader = plugin_loader

    def load(self, locale: str):
        if locale not in self._translations:
            self._translations[locale] = self._load_translations(locale)

        return self._translations[locale]

    def _load_translations(self, locale: str):
        translations = Translations.load(LOCALE_DIR, locale)
        for _, locale_path in plugins.get_plugins_with_directory("locale"):
            plugin_translations = Translations.load(locale_path, locale)
            translations.merge(plugin_translations)
        return translations


translations = TranslationsLoader(plugins)
