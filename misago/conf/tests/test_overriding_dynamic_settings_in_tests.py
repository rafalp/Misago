import pytest

from ..testing import override_dynamic_settings


def test_dynamic_setting_can_be_overridden_using_context_manager(dynamic_settings):
    assert dynamic_settings["forum_name"] == "Misago"
    with override_dynamic_settings(forum_name="Overrided"):
        assert dynamic_settings["forum_name"] == "Overrided"
    assert dynamic_settings["forum_name"] == "Misago"


def test_dynamic_setting_can_be_overridden_using_decorator(dynamic_settings):
    @override_dynamic_settings(forum_name="Overrided")
    def decorated_function(settings):
        return settings["forum_name"]

    assert dynamic_settings["forum_name"] == "Misago"
    assert decorated_function(dynamic_settings) == "Overrided"
    assert dynamic_settings["forum_name"] == "Misago"


@pytest.mark.asyncio
async def test_dynamic_setting_can_be_overridden_in_async_function_using_decorator(
    dynamic_settings,
):
    @override_dynamic_settings(forum_name="Overrided")
    async def decorated_function(settings):
        return settings["forum_name"]

    assert dynamic_settings["forum_name"] == "Misago"
    assert await decorated_function(dynamic_settings) == "Overrided"
    assert dynamic_settings["forum_name"] == "Misago"
