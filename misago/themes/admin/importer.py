import json
import os
from tempfile import TemporaryDirectory
from zipfile import BadZipFile, ZipFile

from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext as _, gettext_lazy

from ..models import Theme
from .css import create_css
from .forms import (
    ThemeCssUrlManifest,
    ThemeManifest,
    create_css_file_manifest,
    create_media_file_manifest,
)
from .media import create_media
from .tasks import build_theme_css, update_remote_css_size

INVALID_MANIFEST_ERROR = gettext_lazy(
    '"manifest.json" contained by ZIP file is not a valid theme manifest file.'
)


class ThemeImportError(BaseException):
    pass


class InvalidThemeManifest(ThemeImportError):
    def __init__(self):
        super().__init__(INVALID_MANIFEST_ERROR)


def import_theme(name, parent, zipfile):
    with TemporaryDirectory() as tmp_dir:
        extract_zipfile_to_tmp_dir(zipfile, tmp_dir)
        validate_zipfile_contains_single_directory(tmp_dir)
        theme_dir = os.path.join(tmp_dir, os.listdir(tmp_dir)[0])
        cleaned_manifest = clean_theme_contents(theme_dir)

        theme = create_theme_from_manifest(name, parent, cleaned_manifest)

        try:
            create_css_from_manifest(theme_dir, theme, cleaned_manifest["css"])
            create_media_from_manifest(theme_dir, theme, cleaned_manifest["media"])
        except Exception:
            theme.delete()
            raise InvalidThemeManifest()
        else:
            for css in theme.css.filter(url__isnull=False):
                update_remote_css_size.delay(css.pk)
            build_theme_css.delay(theme.pk)

        return theme


def extract_zipfile_to_tmp_dir(zipfile, tmp_dir):
    try:
        ZipFile(zipfile).extractall(tmp_dir)
    except BadZipFile:
        raise ThemeImportError(_("Uploaded ZIP file could not be extracted."))


def validate_zipfile_contains_single_directory(tmp_dir):
    dir_contents = os.listdir(tmp_dir)
    if not dir_contents:
        raise ThemeImportError(_("Uploaded ZIP file is empty."))
    if len(dir_contents) > 1:
        raise ThemeImportError(_("Uploaded ZIP file should contain single directory."))
    if not os.path.isdir(os.path.join(tmp_dir, dir_contents[0])):
        raise ThemeImportError(_("Uploaded ZIP file didn't contain a directory."))


def clean_theme_contents(theme_dir):
    manifest = read_manifest(theme_dir)
    return clean_manifest(theme_dir, manifest)


def read_manifest(theme_dir):
    try:
        with open(os.path.join(theme_dir, "manifest.json")) as fp:
            return json.load(fp)
    except FileNotFoundError:
        raise ThemeImportError(
            _('Uploaded ZIP file didn\'t contain a "manifest.json".')
        )
    except json.decoder.JSONDecodeError:
        raise ThemeImportError(
            _('"manifest.json" contained by ZIP file is not a valid JSON file.')
        )


def clean_manifest(theme_dir, manifest):
    if not isinstance(manifest, dict):
        raise InvalidThemeManifest()

    form = ThemeManifest(manifest)
    if not form.is_valid():
        raise InvalidThemeManifest()

    cleaned_manifest = form.cleaned_data.copy()
    cleaned_manifest["css"] = clean_css_list(theme_dir, manifest.get("css"))
    cleaned_manifest["media"] = clean_media_list(theme_dir, manifest.get("media"))

    return cleaned_manifest


def clean_css_list(theme_dir, manifest):
    if not isinstance(manifest, list):
        raise InvalidThemeManifest()

    theme_css_dir = os.path.join(theme_dir, "css")
    if not os.path.isdir(theme_css_dir):
        raise InvalidThemeManifest()

    cleaned_data = []
    for item in manifest:
        cleaned_data.append(clean_css_list_item(theme_css_dir, item))
    return cleaned_data


def clean_css_list_item(theme_css_dir, item):
    if not isinstance(item, dict):
        raise InvalidThemeManifest()

    if item.get("url"):
        return clean_css_url(item)
    if item.get("path"):
        return clean_css_file(theme_css_dir, item)

    raise InvalidThemeManifest()


def clean_css_url(data):
    form = ThemeCssUrlManifest(data)
    if not form.is_valid():
        raise InvalidThemeManifest()
    return form.cleaned_data


def clean_css_file(theme_css_dir, data):
    file_manifest = create_css_file_manifest(theme_css_dir)

    if data.get("path"):
        data["path"] = os.path.join(theme_css_dir, str(data["path"]))

    form = file_manifest(data)
    if not form.is_valid():
        raise InvalidThemeManifest()
    return form.cleaned_data


def clean_media_list(theme_dir, manifest):
    if not isinstance(manifest, list):
        raise InvalidThemeManifest()

    theme_media_dir = os.path.join(theme_dir, "media")
    if not os.path.isdir(theme_media_dir):
        raise InvalidThemeManifest()

    cleaned_data = []
    for item in manifest:
        cleaned_data.append(clean_media_list_item(theme_media_dir, item))
    return cleaned_data


def clean_media_list_item(theme_media_dir, data):
    if not isinstance(data, dict):
        raise InvalidThemeManifest()

    file_manifest = create_media_file_manifest(theme_media_dir)

    if data.get("path"):
        data["path"] = os.path.join(theme_media_dir, str(data["path"]))

    form = file_manifest(data)
    if not form.is_valid():
        raise InvalidThemeManifest()

    return form.cleaned_data


def create_theme_from_manifest(name, parent, cleaned_data):
    return Theme.objects.create(
        name=name or cleaned_data["name"],
        parent=parent,
        version=cleaned_data.get("version") or None,
        author=cleaned_data.get("author") or None,
        url=cleaned_data.get("url") or None,
    )


def create_css_from_manifest(tmp_dir, theme, manifest):
    for item in manifest:
        if "url" in item:
            theme.css.create(**item, order=theme.css.count())
        else:
            with open(item["path"], "rb") as fp:
                file_obj = UploadedFile(
                    fp,
                    name=item["name"],
                    content_type="text/css",
                    size=os.path.getsize(item["path"]),
                )
                create_css(theme, file_obj)


def create_media_from_manifest(tmp_dir, theme, manifest):
    for item in manifest:
        with open(item["path"], "rb") as fp:
            file_obj = UploadedFile(
                fp,
                name=item["name"],
                content_type=item["type"],
                size=os.path.getsize(item["path"]),
            )
            create_media(theme, file_obj)
