from ..core.utils import slugify
from .filetypes import AttachmentFileType

FILENAME_MAX_LENGTH = 50


def clean_filename(filename: str, filetype: AttachmentFileType) -> str:
    extension = _get_filename_extension(filename, filetype)
    filename_clean = filename[: len(extension) * -1] or "attachment"
    filename_clean = slugify(filename_clean)[:FILENAME_MAX_LENGTH]
    return filename_clean + extension


def _get_filename_extension(filename: str, filetype: AttachmentFileType) -> str:
    for extension in filetype.extensions:
        extension = "." + extension
        if filename.lower().endswith(extension):
            return extension

    raise ValueError(
        f"Filename doesn't match filetype: '{filename}' != '{filetype.name}'"
    )
