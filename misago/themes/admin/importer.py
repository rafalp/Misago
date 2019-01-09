from tempfile import TemporaryDirectory

from django.utils.translation import gettext as _


class ThemeImportError(BaseException):
    pass


def import_theme(name, zipfile):
    with TemporaryDirectory() as tmp_dir:
        pass
    
