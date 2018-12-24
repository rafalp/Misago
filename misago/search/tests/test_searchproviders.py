from django.core.exceptions import PermissionDenied
from django.test import TestCase

from ...conf import settings
from ..searchprovider import SearchProvider
from ..searchproviders import SearchProviders


class MockProvider(SearchProvider):
    pass


class DisallowedProvider(SearchProvider):
    def allow_search(self):
        raise PermissionDenied()


class SearchProvidersTests(TestCase):
    def test_initialize_providers(self):
        """initialize_providers initializes providers"""
        searchproviders = SearchProviders(settings.MISAGO_SEARCH_EXTENSIONS)
        searchproviders.initialize_providers()

        self.assertTrue(searchproviders._initialized)

        self.assertEqual(
            len(searchproviders._providers), len(settings.MISAGO_SEARCH_EXTENSIONS)
        )

        for i, provider in enumerate(searchproviders._providers):
            classname = settings.MISAGO_SEARCH_EXTENSIONS[i].split(".")[-1]
            self.assertEqual(provider.__name__, classname)

    def test_get_providers(self):
        """get_providers returns initialized providers"""
        searchproviders = SearchProviders([])

        searchproviders._initialized = True
        searchproviders._providers = [MockProvider, MockProvider, MockProvider]

        self.assertEqual(
            [m.__class__ for m in searchproviders.get_providers(True)],
            searchproviders._providers,
        )

    def test_providers_are_init_with_request(self):
        """providers constructor is provided with request"""
        searchproviders = SearchProviders([])

        searchproviders._initialized = True
        searchproviders._providers = [MockProvider]

        self.assertEqual(searchproviders.get_providers("REQUEST")[0].request, "REQUEST")

    def test_get_allowed_providers(self):
        """
        allowed providers getter returns only providers that didn't raise an exception
        in allow_search
        """
        searchproviders = SearchProviders([])

        searchproviders._initialized = True
        searchproviders._providers = [MockProvider, DisallowedProvider, MockProvider]

        self.assertEqual(
            [m.__class__ for m in searchproviders.get_allowed_providers(True)],
            [MockProvider, MockProvider],
        )
