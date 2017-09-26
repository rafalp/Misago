from types import ModuleType

from django.test import TestCase
from django.utils import six

from misago.acl.providers import PermissionProviders
from misago.conf import settings


class TestType(object):
    pass


class PermissionProvidersTests(TestCase):
    def test_initialization(self):
        """providers manager is lazily initialized"""
        providers = PermissionProviders()

        self.assertTrue(providers._initialized is False)
        self.assertTrue(not providers._providers)
        self.assertTrue(not providers._providers_dict)

        # public api errors on non-loaded object
        with self.assertRaises(AssertionError):
            providers.get_obj_type_annotators(TestType())

        with self.assertRaises(AssertionError):
            providers.get_obj_type_serializers(TestType())

        with self.assertRaises(AssertionError):
            providers.list()

        self.assertTrue(providers._initialized is False)
        self.assertTrue(not providers._providers)
        self.assertTrue(not providers._providers_dict)

        # load initializes providers
        providers = PermissionProviders()
        providers.load()

        self.assertTrue(providers._initialized)
        self.assertTrue(providers._providers)
        self.assertTrue(providers._providers_dict)

    def test_list(self):
        """providers manager list() returns iterable of tuples"""
        providers = PermissionProviders()

        # providers.list() throws before loading providers
        with self.assertRaises(AssertionError):
            providers.list()

        providers.load()

        providers_list = providers.list()

        providers_setting = settings.MISAGO_ACL_EXTENSIONS
        self.assertEqual(len(providers_list), len(providers_setting))

        for extension, module in providers_list:
            self.assertTrue(isinstance(extension, six.string_types))
            self.assertEqual(type(module), ModuleType)

    def test_dict(self):
        """providers manager dict() returns dict"""
        providers = PermissionProviders()

        # providers.dict() throws before loading providers
        with self.assertRaises(AssertionError):
            providers.dict()

        providers.load()

        providers_dict = providers.dict()

        providers_setting = settings.MISAGO_ACL_EXTENSIONS
        self.assertEqual(len(providers_dict), len(providers_setting))

        for extension, module in providers_dict.items():
            self.assertTrue(isinstance(extension, six.string_types))
            self.assertEqual(type(module), ModuleType)

    def test_annotators(self):
        """its possible to register and get annotators"""
        def mock_annotator(*args):
            pass

        providers = PermissionProviders()
        providers.acl_annotator(TestType, mock_annotator)
        providers.load()

        # providers.acl_annotator() throws after loading providers
        with self.assertRaises(AssertionError):
            providers.acl_annotator(TestType, mock_annotator)

        annotators_list = providers.get_obj_type_annotators(TestType())
        self.assertEqual(annotators_list[0], mock_annotator)

    def test_serializers(self):
        """its possible to register and get annotators"""
        def mock_serializer(*args):
            pass

        providers = PermissionProviders()
        providers.acl_serializer(TestType, mock_serializer)
        providers.load()

        # providers.acl_serializer() throws after loading providers
        with self.assertRaises(AssertionError):
            providers.acl_serializer(TestType, mock_serializer)

        serializers_list = providers.get_obj_type_serializers(TestType())
        self.assertEqual(serializers_list[0], mock_serializer)
