import json
import os
from tempfile import TemporaryDirectory
from zipfile import BadZipFile, ZipFile

from django.utils.translation import gettext as _

from ..models import Theme


class ThemeImportError(BaseException):
    pass


def import_theme(name, parent, zipfile):
    with TemporaryDirectory() as tmp_dir:
        extract_zipfile_to_tmp_dir(zipfile, tmp_dir)
        validate_zipfile_contains_single_directory(tmp_dir)
        theme_dir = os.path.join(tmp_dir, os.listdir(tmp_dir)[0])
        clean_data = clean_theme_contents(theme_dir)

        # TODO: finish import
        return Theme.objects.create(
            name=name or clean_data["name"],
            parent=parent,
            version=clean_data["version"],
            author=clean_data["author"],
            url=clean_data["url"],
        )
    

def extract_zipfile_to_tmp_dir(zipfile, tmp_dir):
    try:
        ZipFile(zipfile).extractall(tmp_dir)
    except BadZipFile:
        raise ThemeImportError(_("Uploaded ZIP file could not be extracted."))


def validate_zipfile_contains_single_directory(tmp_dir):
    dir_contents = os.listdir(tmp_dir)
    if not len(dir_contents):
        raise ThemeImportError(_("Uploaded ZIP file is empty."))
    if len(dir_contents) > 1:
        raise ThemeImportError(_("Uploaded ZIP file should contain single directory."))
    if not os.path.isdir(os.path.join(tmp_dir, dir_contents[0])):
        raise ThemeImportError(_("Uploaded ZIP file didn't contain a directory."))


def clean_theme_contents(theme_dir):
    return read_manifest(theme_dir)


def read_manifest(theme_dir):
    try:
        with open(os.path.join(theme_dir, "manifest.json")) as fp:
            manifest = json.load(fp)
        if not isinstance(manifest, dict):
            message = _(
                '"manifest.json" contained by ZIP file is not a valid '
                'theme manifest file.'
            )
            raise ThemeImportError(message)
    except FileNotFoundError:
        raise ThemeImportError(
            _('Uploaded ZIP file didn\'t contain a "manifest.json".')
        )
    except json.decoder.JSONDecodeError:
        raise ThemeImportError(
            _('"manifest.json" contained by ZIP file is not a valid JSON file.')
        )
    else:
        return manifest
