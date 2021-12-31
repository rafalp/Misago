import os
from unittest.mock import patch

import pytest

from ..manifests import parse_asset_manifest


@pytest.fixture
def manifest_path(static_path):
    return os.path.join(static_path, "misago", "asset-manifest.json")


def test_manifest_runtime_is_parsed(static_path, manifest_path):
    with patch("misago.conf.settings._static_root", static_path):
        manifest = parse_asset_manifest(manifest_path)
        assert manifest.runtime.splitlines()[-1] == (
            "//# sourceMappingURL=/static/misago/js/runtime-main.ef606b99.js.map"
        )


def test_manifest_js_files_are_parsed(static_path, manifest_path):
    with patch("misago.conf.settings._static_root", static_path):
        manifest = parse_asset_manifest(manifest_path)
        assert manifest.js == [
            "misago/js/10.f83e7772.chunk.js",
            "misago/js/main.3ff0e38f.chunk.js",
        ]


def test_manifest_css_files_are_parsed(static_path, manifest_path):
    with patch("misago.conf.settings._static_root", static_path):
        manifest = parse_asset_manifest(manifest_path)
        assert manifest.css == ["misago/css/main.af2a95f4.chunk.css"]
