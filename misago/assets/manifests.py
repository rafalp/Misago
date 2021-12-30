import json
import os
from typing_extensions import runtime

from ..conf import settings


class AssetManifestError(ValueError):
    pass


MISAGO_PATH = os.path.join(settings.static_root, "misago", "asset-manifest.json")


def discover_asset_manifests():
    assets = {
        "misago": {
            "runtime": None,
            "css": [],
            "chunks": [],
        }
    }

    if not os.path.exists(MISAGO_PATH) or not os.path.isfile(MISAGO_PATH):
        return assets

    assets["misago"] = parse_asset_manifest(MISAGO_PATH)

    return assets


def parse_asset_manifest(manifest_path: str) -> dict:
    assets = {
        "runtime": None,
        "css": [],
        "chunks": [],
    }

    with open(manifest_path) as json_file:
        manifest = json.load(json_file)

    validate_manifest_json(manifest)

    for path in manifest["entrypoints"]:
        if ".." in path:
            continue

        if path.startswith("static/"):
            path = path[7:]
        else:
            raise AssetManifestError("Path to entrypoint should start with 'static/'")

        if "/runtime-main." in path and path.endswith(".js"):
            with open(os.path.join(settings.static_root, path)) as fp:
                assets["runtime"] = fp.read()
        else:
            if path.endswith(".js"):
                assets["chunks"].append(path)
            elif path.endswith(".css"):
                assets["css"].append(path)

    return assets


def validate_manifest_json(manifest: dict):
    if not isinstance(manifest, dict):
        raise AssetManifestError(f"{path} file did not define JSON object")

    if "entrypoints" not in manifest:
        raise AssetManifestError(f"{path} file did not define 'entrypoints' list")

    if not isinstance(manifest["entrypoints"], list):
        raise AssetManifestError(
            f"{path} file contains 'entrypoints' value but it's not list"
        )


asset_manifests = discover_asset_manifests()
