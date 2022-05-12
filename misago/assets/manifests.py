import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

from ..conf import settings
from .runtime import read_runtime


class AssetManifestError(ValueError):
    pass


MANIFEST_PATH = os.path.join(settings.static_root, "misago", "asset-manifest.json")


@dataclass
class Assets:
    runtime: Optional[str] = None
    js: List[str] = field(default_factory=list)
    css: List[str] = field(default_factory=list)


def discover_asset_manifests():
    assets = {"misago": Assets()}

    if not os.path.exists(MANIFEST_PATH) or not os.path.isfile(MANIFEST_PATH):
        return assets

    assets["misago"] = parse_asset_manifest(MANIFEST_PATH)

    return assets


def parse_asset_manifest(manifest_path: str) -> Assets:
    assets = Assets()
    manifest = read_manifest_json(manifest_path)

    for path in manifest["entrypoints"]:
        if ".." in path:
            continue
        if path.startswith("static/"):
            path = path[7:]
        else:
            raise AssetManifestError("Path to entrypoint should start with 'static/'")

        if "/runtime-main." in path and path.endswith(".js"):
            assets.runtime = read_runtime(path)
        else:
            if path.endswith(".js"):
                assets.js.append(path)
            elif path.endswith(".css"):
                assets.css.append(path)

    return assets


def read_manifest_json(manifest_path: str) -> dict:
    with open(manifest_path, "r", encoding="utf-8") as json_file:
        manifest = json.load(json_file)
        validate_manifest_json(manifest_path, manifest)
        return manifest


def validate_manifest_json(path: str, manifest: dict):
    if not isinstance(manifest, dict):
        raise AssetManifestError(f"{path} file did not define JSON object")

    if "entrypoints" not in manifest:
        raise AssetManifestError(f"{path} file did not define 'entrypoints' list")

    if not isinstance(manifest["entrypoints"], list):
        raise AssetManifestError(
            f"{path} file contains 'entrypoints' value but it's not list"
        )


asset_manifests = discover_asset_manifests()
