# pylint: disable=protected-access
from types import ModuleType

from django.conf import settings
from django.test import TestCase

from misago.acl.providers import PermissionProviders


class TestType(object):
    pass


class PermissionProvidersTests(TestCase):
    def test_initialization(self):
        """providers manager is lazily initialized"""
        providers = PermissionProviders()

        self.assertTrue(providers._initialized is False)
        self.assertTrue(not providers._providers)
        self.assertTrue(not providers._providers_dict)

        # list call initializes providers
        providers_list = providers.list()

        self.assertTrue(providers_list)
        self.assertTrue(providers._initialized)
        self.assertTrue(providers._providers)
        self.assertTrue(providers._providers_dict)

        # dict call initializes providers
        providers = PermissionProviders()
        providers_dict = providers.dict()

        self.assertTrue(providers_dict)
        self.assertTrue(providers._initialized)
        self.assertTrue(providers._providers)
        self.assertTrue(providers._providers_dict)

    def test_list(self):
        """providers manager list() returns iterable of tuples"""
        providers = PermissionProviders()
        providers_list = providers.list()

        providers_setting = settings.MISAGO_ACL_EXTENSIONS
        self.assertEqual(len(providers_list), len(providers_setting))

        for extension, module in providers_list:
            self.assertTrue(isinstance(extension, basestring))
            self.assertEqual(type(module), ModuleType)

    def test_dict(self):
        """providers manager dict() returns dict"""
        providers = PermissionProviders()
        providers_dict = providers.dict()

        providers_setting = settings.MISAGO_ACL_EXTENSIONS
        self.assertEqual(len(providers_dict), len(providers_setting))

        for extension, module in providers_dict.items():
            self.assertTrue(isinstance(extension, basestring))
            self.assertEqual(type(module), ModuleType)

    def test_annotators(self):
        """its possible to register and get annotators"""
        providers = PermissionProviders()

        def test_annotator(*args):
            pass

        providers.acl_annotator(TestType, test_annotator)
        annotators_list = providers.get_type_annotators(TestType())
        self.assertEqual(annotators_list[0], test_annotator)

    def test_serializers(self):
        """its possible to register and get annotators"""
        providers = PermissionProviders()

        def test_serializer(*args):
            pass

        providers.acl_serializer(TestType, test_serializer)
        serializers_list = providers.get_type_serializers(TestType())
        self.assertEqual(serializers_list[0], test_serializer)
