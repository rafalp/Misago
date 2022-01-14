from typing import List, Optional, Tuple

from PIL import Image, UnidentifiedImageError
from asgiref.sync import sync_to_async
from starlette.datastructures import UploadFile

from .errors import (
    UploadContentTypeError,
    UploadImageError,
    UploadImageMaxSizeError,
    UploadImageMinSizeError,
    UploadMaxSizeError,
)
from .utils import get_upload_size

__all__ = [
    "UploadContentTypeValidator",
    "UploadImageValidator",
    "UploadSizeValidator",
]


class UploadSizeValidator:
    limit_value: int

    def __init__(self, max_size_in_bytes: int):
        self.limit_value = max_size_in_bytes

    async def __call__(self, upload: UploadFile, *_):
        upload_size = await get_upload_size(upload)
        if upload_size > self.limit_value:
            raise UploadMaxSizeError(limit_value=self.limit_value)

        return upload


class UploadContentTypeValidator:
    content_types: List[str]

    def __init__(self, content_types: List[str]):
        self.content_types = content_types

    def __call__(self, upload: UploadFile, *_):
        if upload.content_type not in self.content_types:
            raise UploadContentTypeError(limit_value=self.content_types)

        return upload


class UploadImageValidator:
    min_size: Tuple[int, int]
    max_size: Optional[Tuple[int, int]]

    def __init__(
        self,
        min_size: Optional[Tuple[int, int]] = None,
        max_size: Optional[Tuple[int, int]] = None,
    ):
        self.min_size = min_size or (0, 0)
        self.max_size = max_size

    @sync_to_async
    def __call__(self, upload: UploadFile, *_):
        try:
            image = Image.open(upload.file)
            width, height = image.size
        except UnidentifiedImageError as exc:
            raise UploadImageError() from exc

        min_width, min_height = self.min_size
        if width < min_width or height < min_height:
            raise UploadImageMinSizeError(
                limit_width_value=min_width,
                limit_height_value=min_height,
            )

        if self.max_size:
            max_width, max_height = self.max_size
            if width > max_width or height > max_height:
                raise UploadImageMaxSizeError(
                    limit_width_value=max_width,
                    limit_height_value=max_height,
                )

        return upload
