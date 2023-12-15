from enum import StrEnum
from typing import Any, Dict, List, Protocol

from django.template import Context
from django.utils.safestring import SafeString

from .hooks import ActionHook


class PluginOutletName(StrEnum):
    """Enum with standard plugin outlets defined by Misago"""

    TEST = "TEST"
    ADMIN_DASHBOARD_START = "ADMIN_DASHBOARD_START"
    ADMIN_DASHBOARD_AFTER_CHECKS = "ADMIN_DASHBOARD_AFTER_CHECKS"
    ADMIN_DASHBOARD_AFTER_ANALYTICS = "ADMIN_DASHBOARD_AFTER_ANALYTICS"
    ADMIN_DASHBOARD_END = "ADMIN_DASHBOARD_END"


class PluginOutletHookAction:
    def __call__(self, context: dict | Context) -> str | SafeString | None:
        pass


class PluginOutletHook(ActionHook[PluginOutletHookAction]):
    __slots__ = ActionHook.__slots__

    def __call__(self, context: dict | Context) -> List[str | SafeString | None]:
        return super().__call__(context)


template_outlets: Dict[str, PluginOutletHook] = {}
for plugin_outlet in PluginOutletName:
    template_outlets[plugin_outlet.value] = PluginOutletHook()


def append_template_plugin(
    outlet_name: str | PluginOutletName, plugin: PluginOutletHookAction
):
    get_outlet(outlet_name).append_action(plugin)


def prepend_template_plugin(
    outlet_name: str | PluginOutletName, plugin: PluginOutletHookAction
):
    get_outlet(outlet_name).append_action(plugin)


def get_outlet(outlet_name: str | PluginOutletName) -> PluginOutletHook:
    try:
        if isinstance(outlet_name, PluginOutletName):
            return template_outlets[outlet_name.value]
        return template_outlets[outlet_name]
    except KeyError as exc:
        raise KeyError(f"Unknown template outlet: {outlet_name}") from exc
