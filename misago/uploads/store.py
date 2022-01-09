import os
import shutil
from typing import IO

from ..conf import settings


def make_media_path(file_path: str) -> str:
    if ".." in file_path or "./" in file_path:
        raise ValueError(f"Insecure path {file_path}")

    return os.path.join(settings.media_root, file_path)


def media_file_exists(file_path: str) -> bool:
    media_path = make_media_path(file_path)
    return os.path.isfile(media_path)


def store_media_file(file: IO, file_path: str):
    media_path = make_media_path(file_path)
    make_media_directory(os.path.dirname(media_path))

    with open(media_path, "wb") as fp:
        while True:
            chunk = file.read(32)
            if not chunk:
                return
            fp.write(chunk)


def make_media_directory(dir_path: str):
    media_path = make_media_path(dir_path)
    os.makedirs(media_path, exist_ok=True)


def delete_media_file(file_path: str):
    media_path = make_media_path(file_path)
    if os.path.isfile(media_path):
        os.remove(media_path)


def delete_media_directory(dir_path: str):
    media_path = make_media_path(dir_path)
    if os.path.isdir(media_path):
        shutil.rmtree(media_path)
