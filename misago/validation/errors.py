from pydantic import PydanticValueError


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
