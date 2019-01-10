import json
import os
import shutil
from tempfile import TemporaryDirectory

from django.http import FileResponse

from ...core.utils import slugify


def export_theme(theme):
    with TemporaryDirectory() as tmp_dir:
        export_dir = create_export_directory(tmp_dir, theme)

        manifest = create_theme_manifest(theme)

        manifest["css"] = write_theme_css(export_dir, theme)
        manifest["media"] = write_theme_media(export_dir, theme)
        write_theme_manifest(export_dir, manifest)

        export_file = zip_theme_export(tmp_dir, export_dir)
        export_filename = os.path.split(export_file)[-1]

        response = FileResponse(open(export_file, "rb"), content_type="application/zip")
        response["Content-Length"] = os.path.getsize(export_file)
        response["Content-Disposition"] = "inline; filename=%s" % export_filename

        return response


def create_export_directory(tmp_dir, theme):
    export_name = get_export_name(theme)
    export_dir = os.path.join(tmp_dir, export_name)
    os.mkdir(export_dir)
    return export_dir


def get_export_name(theme):
    if theme.version:
        return "%s-%s" % (slugify(theme.name), theme.version.replace(".", "-"))
    return slugify(theme.name)


def create_theme_manifest(theme):
    return {
        "name": theme.name,
        "version": theme.version,
        "author": theme.author,
        "url": theme.url,
        "css": [],
        "media": [],
    }


def write_theme_css(export_dir, theme):
    files_dir = create_sub_directory(export_dir, "css")
    files = []

    for css in theme.css.all():
        if css.url:
            files.append({"name": css.name, "url": css.url})
        else:
            files.append(
                {"name": css.name, "path": copy_asset_file(files_dir, css.source_file)}
            )

    return files


def write_theme_media(export_dir, theme):
    files_dir = create_sub_directory(export_dir, "media")
    files = []

    for media in theme.media.all():
        files.append(
            {
                "name": media.name,
                "type": media.type,
                "path": copy_asset_file(files_dir, media.file),
            }
        )

    return files


def create_sub_directory(export_dir, dirname):
    new_dir = os.path.join(export_dir, dirname)
    os.mkdir(new_dir)
    return new_dir


def copy_asset_file(export_dir, asset_file):
    filename = os.path.split(asset_file.name)[-1]
    dst_path = os.path.join(export_dir, filename)
    with open(dst_path, "wb") as fp:
        for chunk in asset_file.chunks():
            fp.write(chunk)
    return filename


def write_theme_manifest(export_dir, manifest):
    manifest_path = os.path.join(export_dir, "manifest.json")
    with open(manifest_path, "w") as fp:
        json.dump(manifest, fp, ensure_ascii=False, indent=2)


def zip_theme_export(tmp_dir, export_dir):
    dir_name = os.path.split(export_dir)[-1]
    return shutil.make_archive(export_dir, "zip", tmp_dir, dir_name)
