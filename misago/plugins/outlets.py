from functools import wraps
from typing import Dict, List, Protocol

from django.http import HttpRequest
from django.template import Context
from django.utils.safestring import SafeString, mark_safe

from .enums import PluginOutlet
from .hooks import ActionHook


class PluginOutletHookAction(Protocol):
    def __call__(
        self, request: HttpRequest, context: dict | Context
    ) -> str | SafeString | None:
        pass


class PluginOutletHook(ActionHook[PluginOutletHookAction]):
    __slots__ = ActionHook.__slots__

    def __call__(
        self, request: HttpRequest, context: dict | Context
    ) -> List[str | SafeString | None]:
        return super().__call__(request, context)


template_outlets: Dict[str, PluginOutletHook] = {}


def create_new_outlet(outlet_name: str):
    if outlet_name in template_outlets:
        raise ValueError(f"Template outlet '{outlet_name}' already exists.")

    template_outlets[plugin_outlet.name] = PluginOutletHook()


for plugin_outlet in PluginOutlet:
    create_new_outlet(plugin_outlet.name)


def append_outlet_action(
    outlet_name: str | PluginOutlet, action: PluginOutletHookAction
):
    get_outlet(outlet_name).append_action(action)


def prepend_outlet_action(
    outlet_name: str | PluginOutlet, action: PluginOutletHookAction
):
    get_outlet(outlet_name).prepend_action(action)


def get_outlet(outlet_name: str | PluginOutlet) -> PluginOutletHook:
    try:
        if isinstance(outlet_name, PluginOutlet):
            return template_outlets[outlet_name.name]
        return template_outlets[outlet_name]
    except KeyError as exc:
        raise KeyError(f"Unknown template outlet: {outlet_name}") from exc


def template_outlet_action(f):
    """Decorator for an outlet action that renders a template with returned context."""

    @wraps(f)
    @mark_safe
    def wrapped_outlet_action(request: HttpRequest, context: Context):
        template_data = f(request, context)
        if template_data is None:
            return ""

        if isinstance(template_data, str):
            return _include_template(template_data, context)

        if isinstance(template_data, tuple):
            template_name, new_context = template_data
            return _include_template(template_name, context, new_context)

        return ""

    return wrapped_outlet_action


def _include_template(
    template_name: str, context: Context, new_context: dict | None = None
):
    """Subset of Django include template tag.

    Works only with Django template engine.
    """
    cache = context.render_context.dicts[0].setdefault("_template_outlet_action", {})
    template = cache.get(template_name)
    if template is None:
        template = context.template.engine.get_template(template_name)
        cache[template_name] = template

    if new_context:
        with context.push(**new_context):
            return template.render(context)

    return template.render(context)
