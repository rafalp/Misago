from ..core.utils import slugify
from .filetypes import AttachmentFileType

FILENAME_MAX_LENGTH = 50


def clean_filename(filename: str, filetype: AttachmentFileType) -> str:
    filename_clean = filename[: len(extension) * -1] or "attachment"
    filename_clean = slugify(filename_clean)[:FILENAME_MAX_LENGTH]
    return filename_clean + extension


def cut_filename(
    filename: str, filetype: AttachmentFileType, max_length=FILENAME_MAX_LENGTH
) -> str:
    name, extension = filetype.split_name(filename)
    max_length -= len(extension) + 1
    return name[:max_length].strip() + "." + extension
