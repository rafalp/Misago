from importlib.util import find_spec

from django.urls import URLResolver, include, path


def discover_plugins_urlpatterns(plugins: list[str]) -> list[URLResolver]:
    urlpatterns: list[URLResolver] = []
    for plugin in plugins:
        if plugin_has_urls(plugin):
            urlpatterns.append(path("", include(f"{plugin}.urls")))

    return urlpatterns


def plugin_has_urls(plugin: str) -> bool:
    return bool(find_spec(f"{plugin}.urls"))
