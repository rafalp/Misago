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
