import pytest
from django.conf import settings

from ..metadata import PluginsMetadataLoader


@pytest.fixture
def plugins_metadata():
    return PluginsMetadataLoader(settings.INSTALLED_PLUGINS)


def test_plugins_metadata_loader_returns_metadata_dict(plugins_metadata):
    metadata = plugins_metadata.get_metadata()
    assert metadata


def test_plugins_metadata_loader_caches_metadata(plugins_metadata):
    metadata = plugins_metadata.get_metadata()
    other_metadata = plugins_metadata.get_metadata()
    assert id(metadata) == id(other_metadata)


def test_plugins_metadata_loader_handles_plugins_without_manifests(plugins_metadata):
    metadata = plugins_metadata.get_metadata()
    assert "minimal_plugin" in metadata

    plugin_metadata = metadata["minimal_plugin"]
    assert plugin_metadata.package == "minimal_plugin"
    assert plugin_metadata.dirname == "minimal-plugin"
    assert plugin_metadata.has_manifest == False
    assert plugin_metadata.manifest_error is None
    assert plugin_metadata.name is None


def test_plugins_metadata_loader_handles_plugins_with_empty_manifests(plugins_metadata):
    metadata = plugins_metadata.get_metadata()
    assert "empty_manifest_plugin" in metadata

    plugin_metadata = metadata["empty_manifest_plugin"]
    assert plugin_metadata.package == "empty_manifest_plugin"
    assert plugin_metadata.dirname == "empty-manifest-plugin"
    assert plugin_metadata.has_manifest == True
    assert plugin_metadata.manifest_error is None
    assert plugin_metadata.name is None


def test_plugins_metadata_loader_handles_plugins_with_full_manifests(plugins_metadata):
    metadata = plugins_metadata.get_metadata()
    assert "full_manifest_plugin" in metadata

    plugin_metadata = metadata["full_manifest_plugin"]
    assert plugin_metadata.package == "full_manifest_plugin"
    assert plugin_metadata.dirname == "full-manifest-plugin"
    assert plugin_metadata.has_manifest == True
    assert plugin_metadata.manifest_error is None
    assert plugin_metadata.name == "Example plugin with complete manifest"


def test_plugins_metadata_loader_handles_plugins_with_invalid_manifests(
    plugins_metadata,
):
    metadata = plugins_metadata.get_metadata()
    assert "invalid_manifest_plugin" in metadata

    plugin_metadata = metadata["invalid_manifest_plugin"]
    assert plugin_metadata.package == "invalid_manifest_plugin"
    assert plugin_metadata.dirname == "invalid-manifest-plugin"
    assert plugin_metadata.has_manifest == False
    assert plugin_metadata.manifest_error is not None
    assert plugin_metadata.name is None


def test_plugins_metadata_loader_handles_empty_plugins_list():
    plugins_metadata = PluginsMetadataLoader([])
    metadata = plugins_metadata.get_metadata()
    assert metadata == {}
    assert id(metadata) == id(metadata)
