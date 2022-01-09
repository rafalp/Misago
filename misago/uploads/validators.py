from typing import List

from starlette.datastructures import UploadFile

from .errors import UploadContentTypeError, UploadMaxSizeError
from .utils import get_upload_size


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
