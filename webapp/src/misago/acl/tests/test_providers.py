import pytest

from ...conf import settings
from ..providers import PermissionProviders


def test_providers_are_not_loaded_on_container_init():
    providers = PermissionProviders()

    assert not providers._initialized
    assert not providers._providers
    assert not providers._annotators
    assert not providers._user_acl_serializers


def test_container_loads_providers():
    providers = PermissionProviders()
    providers.load()

    assert providers._providers
    assert providers._annotators
    assert providers._user_acl_serializers


def test_loading_providers_second_time_raises_runtime_error():
    providers = PermissionProviders()
    providers.load()

    with pytest.raises(RuntimeError):
        providers.load()


def test_container_returns_list_of_providers():
    providers = PermissionProviders()
    providers.load()

    providers_setting = settings.MISAGO_ACL_EXTENSIONS
    assert len(providers.list()) == len(providers_setting)


def test_container_returns_dict_of_providers():
    providers = PermissionProviders()
    providers.load()

    providers_setting = settings.MISAGO_ACL_EXTENSIONS
    assert len(providers.dict()) == len(providers_setting)


def test_accessing_providers_list_before_load_raises_assertion_error():
    providers = PermissionProviders()
    with pytest.raises(AssertionError):
        providers.list()


def test_accessing_providers_dict_before_load_raises_assertion_error():
    providers = PermissionProviders()
    with pytest.raises(AssertionError):
        providers.dict()


def test_getter_returns_registered_type_annotator():
    class TestType:
        pass

    def test_annotator():
        pass

    providers = PermissionProviders()
    providers.acl_annotator(TestType, test_annotator)
    providers.load()

    assert test_annotator in providers.get_obj_type_annotators(TestType())


def test_container_returns_list_of_user_acl_serializers():
    providers = PermissionProviders()
    providers.load()

    assert providers.get_user_acl_serializers()


def test_getter_returns_registered_user_acl_serializer():
    def test_user_acl_serializer():
        pass

    providers = PermissionProviders()
    providers.user_acl_serializer(test_user_acl_serializer)
    providers.load()

    assert test_user_acl_serializer in providers.get_user_acl_serializers()
