from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AttachmentFileType:
    name: str
    extensions: Iterable[str]
    content_types: Iterable[str] | None = None
    is_image: bool = False
    is_video: bool = False
    is_archive: bool = False
    is_document: bool = False

    @property
    def is_file(self):
        return not bool(self.is_image or self.is_video)


class AttachmentFileTypes:
    _filetypes: dict[str, AttachmentFileType]

    def __init__(self):
        self._filetypes = {}

    def add_filetype(
        self,
        name: str,
        extensions: str | Iterable[str],
        content_types: str | Iterable[str] | None = None,
        is_image: bool = False,
        is_video: bool = False,
        is_archive: bool = False,
        is_document: bool = False,
    ) -> AttachmentFileType:
        filetype = AttachmentFileType(
            name=name,
            extensions=(extensions,) if isinstance(extensions, str) else extensions,
            content_types=content_types,
            is_image=is_image,
            is_video=is_video,
            is_archive=is_archive,
            is_document=is_document,
        )

        self._filetypes[name] = filetype
        return filetype

    def get_filetype(self, name: str) -> AttachmentFileType:
        try:
            return self._filetypes[name]
        except KeyError:
            raise ValueError(f"'{name}' filetype is not supported")

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
            (t.name, f"{t.name} ({', '.join(t.extensions)})")
            for t in sorted(self._filetypes.values(), key=lambda x: x.name)
        )

    def get_accept_attr_str(self) -> str:
        items: list[str] = []
        for filetype in self._filetypes.values():
            items.extend(f".{extension}" for extension in filetype.extensions)

        return ", ".join(items)


filetypes = AttachmentFileTypes()

# Images
filetypes.add_filetype(
    name="GIF",
    extensions="gif",
    content_types="image/gif",
    is_image=True,
)
filetypes.add_filetype(
    name="JPEG",
    extensions=("jpeg", "jpg"),
    content_types="image/jpeg",
    is_image=True,
)
filetypes.add_filetype(
    name="PNG",
    extensions="png",
    content_types="image/png",
    is_image=True,
)
filetypes.add_filetype(
    name="WEBP",
    extensions="webp",
    content_types="image/webp",
    is_image=True,
)

# Video
filetypes.add_filetype(
    name="MP4",
    extensions="mp4",
    content_types="video/mp4",
    is_video=True,
)

# Archives
filetypes.add_filetype(
    name="7z",
    extensions="7z",
    content_types="application/x-7z-compressed",
    is_archive=True,
)
filetypes.add_filetype(
    name="GZ",
    extensions="gz",
    content_types="application/gzip",
    is_archive=True,
)
filetypes.add_filetype(
    name="RAR",
    extensions="rar",
    content_types="application/vnd.rar",
    is_archive=True,
)
filetypes.add_filetype(
    name="TAR",
    extensions="tar",
    content_types="application/x-tar",
    is_archive=True,
)
filetypes.add_filetype(
    name="ZIP",
    extensions=("zip", "zipx"),
    content_types="application/zip",
    is_archive=True,
)

# Other
filetypes.add_filetype(
    name="PDF",
    extensions="pdf",
    content_types=(
        "application/pdf",
        "application/x-pdf",
        "application/x-bzpdf",
        "application/x-gzpdf",
    ),
    is_document=True,
)
filetypes.add_filetype(
    name="Text",
    extensions="txt",
    content_types="text/plain",
    is_document=True,
)
filetypes.add_filetype(
    name="Markdown",
    extensions="md",
    content_types="text/markdown",
    is_document=True,
)
filetypes.add_filetype(
    name="reStructuredText",
    extensions="rst",
    content_types="text/x-rst",
    is_document=True,
)
