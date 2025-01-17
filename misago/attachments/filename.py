from ..core.utils import slugify
from .filetypes import AttachmentFileType

CLEAN_FILENAME_MAX_LENGTH = 50

illegal_characters = frozenset("#%&{}\\<>*?/$'\":@+`|=")


def clean_filename(
    filename: str, filetype: AttachmentFileType, max_length=CLEAN_FILENAME_MAX_LENGTH
) -> str:
    name, extension = filetype.split_name(filename)

    clean_name = ""
    for c in name:
        if c not in illegal_characters:
            clean_name += c
        else:
            clean_name += " "

    while "  " in clean_name:
        clean_name = clean_name.replace("  ", " ")

    clean_name = clean_name.strip() or "file"
    clean_name += "." + extension

    return trim_filename(clean_name, filetype, max_length)


def trim_filename(
    filename: str, filetype: AttachmentFileType, max_length=CLEAN_FILENAME_MAX_LENGTH
) -> str:
    name, extension = filetype.split_name(filename)
    max_length -= len(extension) + 1
    return (name[:max_length].strip() or "file") + "." + extension
