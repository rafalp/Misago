import os
from glob import glob
from pathlib import Path

MISAGO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOMENT_LOCALES_DIR = os.path.join(MISAGO_DIR, "static", "misago", "admin", "momentjs")


def get_admin_locales():
    locales = []
    for locale_path in glob(os.path.join(MOMENT_LOCALES_DIR, "*.js")):
        locales.append(Path(locale_path).stem)
    return locales


MISAGO_ADMIN_MOMENT_LOCALES = get_admin_locales()
