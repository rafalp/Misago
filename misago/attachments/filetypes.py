from dataclasses import dataclass
from typing import Iterable

from django.utils.translation import pgettext_lazy

from .enums import AllowedAttachments, AttachmentType


@dataclass(frozen=True)
class AttachmentFileType:
    id: str
    name: str
    extensions: Iterable[str]
    content_types: Iterable[str]
    as_attachment: bool = True
    is_image: bool = False
    is_video: bool = False
    is_archive: bool = False
    is_document: bool = False

    @property
    def is_media(self) -> bool:
        return bool(self.is_image or self.is_video)

    def split_name(self, name: str) -> tuple[str, str]:
        for extension in self.extensions:
            if name.lower().endswith("." + extension):
                return tuple(name.rsplit(".", 1))

        raise ValueError(f"'{name}' is not a valid file name for this file type.")


class AttachmentFileTypes:
    _filetypes: dict[str, AttachmentFileType]

    def __init__(self):
        self._filetypes = {}

    def add_filetype(
        self,
        id: str,
        name: str,
        extensions: str | Iterable[str],
        content_types: str | Iterable[str],
        as_attachment: bool = True,
        is_image: bool = False,
        is_video: bool = False,
        is_archive: bool = False,
        is_document: bool = False,
    ) -> AttachmentFileType:
        filetype = AttachmentFileType(
            id=id,
            name=name,
            extensions=(extensions,) if isinstance(extensions, str) else extensions,
            content_types=(
                (content_types,) if isinstance(content_types, str) else content_types
            ),
            as_attachment=as_attachment,
            is_image=is_image,
            is_video=is_video,
            is_archive=is_archive,
            is_document=is_document,
        )

        self._filetypes[id] = filetype
        return filetype

    def get_all_filetypes(self) -> list[AttachmentFileType]:
        return sorted(self._filetypes.values(), key=lambda i: i.id)

    def get_filetype(self, id: str) -> AttachmentFileType:
        try:
            return self._filetypes[id]
        except KeyError:
            raise ValueError(f"'{id}' file type is not supported")

    def match_filetype(
        self, filename: str, content_type: str | None = None
    ) -> AttachmentFileType | None:
        filename_clean = filename.lower()
        content_type_clean = content_type.lower() if content_type else None

        for filetype in self._filetypes.values():
            if match := self._match_filetype_to_file(
                filetype, filename_clean, content_type_clean
            ):
                return match

        return None

    def _match_filetype_to_file(
        self, filetype: AttachmentFileType, filename: str, content_type: str | None
    ) -> AttachmentFileType | None:
        extension_match = False
        for extension in filetype.extensions:
            if filename.endswith(f".{extension}"):
                extension_match = True

        if not extension_match:
            return None

        if content_type and content_type not in filetype.content_types:
            return None

        return filetype

    def as_django_choices(self) -> tuple[tuple[str, str]]:
        return tuple(
            (t.id, f"{t.name} ({', '.join(t.extensions)})")
            for t in sorted(self._filetypes.values(), key=lambda x: x.name)
        )

    def get_accept_attr_str(
        self,
        allowed_attachments: AllowedAttachments | str,
        *,
        require_extensions: list[str] | None = None,
        disallow_extensions: list[str] | None = None,
        type_filter: AttachmentType | str | None = None,
    ) -> str:
        if allowed_attachments == AllowedAttachments.NONE:
            return ""

        items: list[str] = []
        for filetype in self._filetypes.values():
            # Filter attachment types
            if type_filter == AttachmentType.IMAGE and not filetype.is_image:
                continue

            if type_filter == AttachmentType.VIDEO and not filetype.is_video:
                continue

            if type_filter == AttachmentType.OTHER and filetype.is_media:
                continue

            # Exclude regular files if only media is allowed
            if allowed_attachments != AllowedAttachments.ALL and not filetype.is_media:
                continue

            # Exclude non-images if only images are allowed
            if (
                allowed_attachments == AllowedAttachments.IMAGES
                and not filetype.is_image
            ):
                continue

            items.extend(filetype.extensions)

        if require_extensions and disallow_extensions:
            raise ValueError(
                "'require_extensions' and 'disallow_extensions' can't be used together"
            )

        if require_extensions:
            items = set(require_extensions).intersection(items)
        elif disallow_extensions:
            items = set(items).difference(disallow_extensions)

        return ", ".join("." + item for item in items)


filetypes = AttachmentFileTypes()

# Images
filetypes.add_filetype(
    id="gif",
    name=pgettext_lazy("file type", "GIF image"),
    extensions="gif",
    content_types="image/gif",
    as_attachment=False,
    is_image=True,
)
filetypes.add_filetype(
    id="jpeg",
    name=pgettext_lazy("file type", "JPEG image"),
    extensions=("jpg", "jpeg"),
    content_types="image/jpeg",
    as_attachment=False,
    is_image=True,
)
filetypes.add_filetype(
    id="png",
    name=pgettext_lazy("file type", "PNG image"),
    extensions="png",
    content_types="image/png",
    as_attachment=False,
    is_image=True,
)
filetypes.add_filetype(
    id="webp",
    name=pgettext_lazy("file type", "WebP image"),
    extensions="webp",
    content_types="image/webp",
    as_attachment=False,
    is_image=True,
)

# Video
filetypes.add_filetype(
    id="mp4",
    name=pgettext_lazy("file type", "MP4 video"),
    extensions="mp4",
    content_types="video/mp4",
    as_attachment=False,
    is_video=True,
)
filetypes.add_filetype(
    id="webm",
    name=pgettext_lazy("file type", "WebM video"),
    extensions="webm",
    content_types="video/webm",
    as_attachment=False,
    is_video=True,
)

# Archives
filetypes.add_filetype(
    id="7z",
    name=pgettext_lazy("file type", "7-Zip archive"),
    extensions="7z",
    content_types="application/x-7z-compressed",
    is_archive=True,
)
filetypes.add_filetype(
    id="gzip",
    name=pgettext_lazy("file type", "Gzip tar archive"),
    extensions="tar.gz",
    content_types="application/gzip",
    is_archive=True,
)
filetypes.add_filetype(
    id="bzip2",
    name=pgettext_lazy("file type", "bzip2 tar archive"),
    extensions="tar.bz2",
    content_types="application/x-bzip2",
    is_archive=True,
)
filetypes.add_filetype(
    id="xz",
    name=pgettext_lazy("file type", "XZ archive"),
    extensions="tar.xz",
    content_types="application/x-xz",
    is_archive=True,
)
filetypes.add_filetype(
    id="rar",
    name=pgettext_lazy("file type", "RAR archive"),
    extensions="rar",
    content_types="application/vnd.rar",
    is_archive=True,
)
filetypes.add_filetype(
    id="tar",
    name=pgettext_lazy("file type", "Tar archive"),
    extensions="tar",
    content_types="application/x-tar",
    is_archive=True,
)
filetypes.add_filetype(
    id="zip",
    name=pgettext_lazy("file type", "ZIP archive"),
    extensions=("zip", "zipx"),
    content_types="application/zip",
    is_archive=True,
)

# Other
filetypes.add_filetype(
    id="pdf",
    name=pgettext_lazy("file type", "PDF"),
    extensions="pdf",
    content_types=(
        "application/pdf",
        "application/x-pdf",
        "application/x-bzpdf",
        "application/x-gzpdf",
    ),
    as_attachment=False,
    is_document=True,
)
filetypes.add_filetype(
    id="txt",
    name=pgettext_lazy("file type", "Text file"),
    extensions="txt",
    content_types="text/plain",
    as_attachment=False,
    is_document=True,
)
filetypes.add_filetype(
    id="md",
    name=pgettext_lazy("file type", "Markdown document"),
    extensions="md",
    content_types="text/markdown",
    as_attachment=False,
    is_document=True,
)
filetypes.add_filetype(
    id="rst",
    name=pgettext_lazy("file type", "reStructuredText document"),
    extensions="rst",
    content_types=("text/x-rst", "application/octet-stream"),
    as_attachment=False,
    is_document=True,
)
