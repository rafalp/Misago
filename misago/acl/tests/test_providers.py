from django.test import TestCase

from misago.acl.providers import PermissionProviders
from misago.conf import settings


class PermissionProvidersTests(TestCase):
    def test_providers_are_not_loaded_on_container_init(self):
        providers = PermissionProviders()

        assert not providers._initialized
        assert not providers._providers
        assert not providers._annotators
        assert not providers._user_acl_serializers

    def test_container_loads_providers(self):
        providers = PermissionProviders()
        providers.load()

        assert providers._providers
        assert providers._annotators
        assert providers._user_acl_serializers

    def test_loading_providers_second_time_raises_runtime_error(self):
        providers = PermissionProviders()
        providers.load()

        with self.assertRaises(RuntimeError):
            providers.load()

    def test_container_returns_list_of_providers(self):
        providers = PermissionProviders()
        providers.load()
        
        providers_setting = settings.MISAGO_ACL_EXTENSIONS
        self.assertEqual(len(providers.list()), len(providers_setting))

    def test_container_returns_dict_of_providers(self):
        providers = PermissionProviders()
        providers.load()
        
        providers_setting = settings.MISAGO_ACL_EXTENSIONS
        self.assertEqual(len(providers.dict()), len(providers_setting))

    def test_accessing_providers_list_before_load_raises_assertion_error(self):
        providers = PermissionProviders()
        with self.assertRaises(AssertionError):
            providers.list()
    
    def test_accessing_providers_dict_before_load_raises_assertion_error(self):
        providers = PermissionProviders()
        with self.assertRaises(AssertionError):
            providers.dict()

    def test_getter_returns_registered_type_annotator(self):
        class TestType(object):
            pass


        def test_annotator():
            pass
        

        providers = PermissionProviders()
        providers.acl_annotator(TestType, test_annotator)
        providers.load()

        assert test_annotator in providers.get_obj_type_annotators(TestType())

    def test_container_returns_list_of_user_acl_serializers(self):
        providers = PermissionProviders()
        providers.load()

        assert providers.get_user_acl_serializers()

    def test_getter_returns_registered_user_acl_serializer(self):
        def test_user_acl_serializer():
            pass


        providers = PermissionProviders()
        providers.user_acl_serializer(test_user_acl_serializer)
        providers.load()

        assert test_user_acl_serializer in providers.get_user_acl_serializers()
