from typing import List

from pydantic import PydanticValueError


class UploadContentTypeError(PydanticValueError):
    code = "upload.content_type"
    msg_template = "ensure uploaded file is one of type: {limit_value}"

    def __init__(self, *, limit_value: List[str]) -> None:
        # pylint: disable=useless-super-delegation
        super().__init__(limit_value=", ".join(limit_value))


class UploadMaxSizeError(PydanticValueError):
    code = "upload.max_size"
    msg_template = "ensure uploaded file size is not larger than {limit_value} bytes"


class ImageError(PydanticValueError):
    code = "image"
    msg_template = "ensure value is valid image"


class ImageMinSizeError(PydanticValueError):
    code = "image.min_size"
    msg_template = (
        "ensure image size is at least "
        "{limit_width_value}x{limit_height_value} pixels"
    )


class ImageMaxSizeError(PydanticValueError):
    code = "image.max_size"
    msg_template = (
        "ensure image size is not bigger than "
        "{limit_width_value}x{limit_height_value} pixels"
    )
