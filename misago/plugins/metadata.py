import re
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Dict, List, Optional
from urllib.parse import urlparse

from django.conf import settings
from django.utils.translation import pgettext_lazy

from .manifest import MisagoPlugin


@dataclass(frozen=True)
class PluginMetadataUrl:
    url: str
    netloc: str


@dataclass(frozen=True)
class PluginMetadata:
    package: str
    dirname: str
    has_manifest: bool
    manifest_error: Optional[str]

    name: Optional[str]
    description: Optional[str]
    license: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    version: Optional[str]
    author: Optional[str]
    homepage: Optional[PluginMetadataUrl]
    sponsor: Optional[PluginMetadataUrl]
    help: Optional[PluginMetadataUrl]
    bugs: Optional[PluginMetadataUrl]
    repo: Optional[PluginMetadataUrl]

    @property
    def has_urls(self) -> bool:
        return bool(
            self.homepage or self.sponsor or self.help or self.bugs or self.repo
        )


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
                        "Plugin manifest is of an unexpected type '%(manifest_type)s' (expected MisagoPlugin instance)",
                    )
                    % {"manifest_type": type(manifest_attr).__name__}
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
    description: Optional[str] = None
    license: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    homepage: Optional[PluginMetadataUrl] = None
    sponsor: Optional[PluginMetadataUrl] = None
    help: Optional[PluginMetadataUrl] = None
    bugs: Optional[PluginMetadataUrl] = None
    repo: Optional[PluginMetadataUrl] = None

    if manifest:
        has_manifest = True
        name = clean_plugin_str(manifest.name, 100)
        description = clean_plugin_str(manifest.description, 250)
        license = clean_plugin_str(manifest.license, 50)
        icon = clean_plugin_icon(manifest.icon)
        color = clean_plugin_color(manifest.color)
        version = clean_plugin_str(manifest.version, 50)
        author = clean_plugin_str(manifest.author, 150)
        homepage = clean_plugin_url(manifest.homepage)
        sponsor = clean_plugin_url(manifest.sponsor)
        help = clean_plugin_url(manifest.help)
        bugs = clean_plugin_url(manifest.bugs)
        repo = clean_plugin_url(manifest.repo)

    return PluginMetadata(
        package=plugin_package,
        dirname=Path(package_obj.__file__).parent.parent.name,
        has_manifest=has_manifest,
        manifest_error=manifest_error,
        name=name,
        description=description,
        license=license,
        icon=icon,
        color=color,
        version=version,
        author=author,
        homepage=homepage,
        sponsor=sponsor,
        help=help,
        bugs=bugs,
        repo=repo,
    )


def clean_plugin_str(value: Optional[str], max_length: int) -> Optional[str]:
    if isinstance(value, str):
        return (value.strip()[:max_length].strip()) or None
    return None


URL_RE = re.compile(r"^https?://[A-Za-z0-9-_/?=&#.]+$")


def clean_plugin_url(value: Optional[str]) -> Optional[PluginMetadataUrl]:
    if isinstance(value, str) and URL_RE.match(value):
        try:
            url = urlparse(value)
            if not url:
                return None

            return PluginMetadataUrl(
                url=value,
                netloc=url.netloc,
            )
        except ValueError:
            return None
    return None


ICON_RE = re.compile(r"^fa(r|s)? fa-[a-z-]+$")


def clean_plugin_icon(value: Optional[str]) -> Optional[str]:
    if isinstance(value, str) and ICON_RE.match(value):
        return value
    return None


COLOR_RE = re.compile(r"^#[0-9a-f]{6}$", re.IGNORECASE)


def clean_plugin_color(value: Optional[str]) -> Optional[str]:
    if isinstance(value, str) and COLOR_RE.match(value):
        return value.upper()
    return None


plugins_metadata = PluginsMetadataLoader(settings.INSTALLED_PLUGINS)
