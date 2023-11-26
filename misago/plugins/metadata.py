from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Dict, List, Optional

from django.conf import settings
from django.utils.translation import pgettext_lazy

from .manifest import MisagoPlugin


@dataclass(frozen=True)
class PluginMetadata:
    package: str
    dirname: str
    has_manifest: bool
    manifest_error: Optional[str]

    name: Optional[str]


class PluginsMetadataLoader:
    initialized: bool
    plugins: List[str]
    metadata: Dict[str, PluginMetadata]

    def __init__(self, plugins: List[str]):
        self.initialized = False
        self.plugins = plugins
        self.metadata = {}

    def get_metadata(self) -> Dict[str, PluginMetadata]:
        if not self.initialized:
            self.metadata = self.build_metadata(self.plugins)
            self.initialized = True

        return self.metadata

    def build_metadata(self, plugins: List[str]) -> Dict[str, PluginMetadata]:
        metadata: Dict[str, PluginMetadata] = {}
        for plugin_package in plugins:
            metadata[plugin_package] = self.build_plugin_metadata(plugin_package)
        return metadata

    def build_plugin_metadata(self, plugin_package: str) -> PluginMetadata:
        package_obj = import_module(plugin_package)

        manifest: Optional[MisagoPlugin] = None
        manifest_error: Optional[str] = None

        try:
            manifest_module = import_module(f"{plugin_package}.misago_plugin")
            manifest_attr = getattr(manifest_module, "manifest", None)
            if manifest_attr is not None and not isinstance(
                manifest_attr, MisagoPlugin
            ):
                raise TypeError(
                    pgettext_lazy(
                        "plugins metadata",
                        "Plugin's manifest was of an unexpected type '%(manifest_type)s'.",
                    )
                    % {type(manifest_attr).__name__}
                )
            manifest = manifest_attr
        except Exception as exc:
            manifest_error = f"{type(exc).__name__}: {exc}"

        return create_plugin_metadata(
            plugin_package,
            package_obj,
            manifest,
            manifest_error,
        )


def create_plugin_metadata(
    plugin_package: str,
    package_obj: ModuleType,
    manifest: Optional[MisagoPlugin],
    manifest_error: Optional[str],
) -> PluginMetadata:
    has_manifest = False
    name: Optional[str] = None

    if manifest:
        has_manifest = True
        name = str(manifest.name or "") or None

    return PluginMetadata(
        package=plugin_package,
        dirname=Path(package_obj.__file__).parent.parent.name,
        has_manifest=has_manifest,
        manifest_error=manifest_error,
        name=name,
    )


plugins_metadata = PluginsMetadataLoader(settings.INSTALLED_PLUGINS)
