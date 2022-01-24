from unittest.mock import Mock

import pytest
from starlette.datastructures import UploadFile

from ..errors import (
    ImageError,
    ImageMaxSizeError,
    ImageMinSizeError,
    UploadContentTypeError,
    UploadMaxSizeError,
)
from ..validators import (
    UploadContentTypeValidator,
    UploadImageValidator,
    UploadSizeValidator,
)


def test_content_type_validator_passes_allowed_types():
    upload = Mock(content_type="image/jpeg")

    single_type_validator = UploadContentTypeValidator(["image/jpeg"])
    assert single_type_validator(upload) == upload

    multiple_types_validator = UploadContentTypeValidator(["image/jpeg", "image/gif"])
    assert multiple_types_validator(upload) == upload


def test_content_type_validator_raises_error_for_invalid_type():
    with pytest.raises(UploadContentTypeError):
        upload = Mock(content_type="image/png")
        single_type_validator = UploadContentTypeValidator(["image/jpeg"])
        single_type_validator(upload)


@pytest.mark.asyncio
async def test_upload_size_validator_passes_valid_sizes():
    upload = UploadFile("test.txt", content_type="text/plain")
    await upload.write(str("a" * 128).encode("utf-8"))

    exact_size_validator = UploadSizeValidator(128)
    assert await exact_size_validator(upload) == upload

    greater_size_validator = UploadSizeValidator(256)
    assert await greater_size_validator(upload) == upload


@pytest.mark.asyncio
async def test_upload_size_validator_raises_error_for_too_large_uploads():
    upload = UploadFile("test.txt", content_type="text/plain")
    await upload.write(str("a" * 128).encode("utf-8"))

    with pytest.raises(UploadMaxSizeError):
        exact_size_validator = UploadSizeValidator(64)
        await exact_size_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_passes_valid_image_file(create_upload_file):
    upload = await create_upload_file("image.png")
    image_validator = UploadImageValidator()
    assert await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_raises_error_if_upload_is_not_image(
    create_upload_file,
):
    upload = await create_upload_file("text_file.txt")
    image_validator = UploadImageValidator()
    with pytest.raises(ImageError):
        await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_passes_image_file_with_valid_min_dimensions(
    create_upload_file,
):
    upload = await create_upload_file("image.png")
    image_validator = UploadImageValidator(min_size=(30, 20))
    assert await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_raises_error_if_uploaded_image_is_too_small(
    create_upload_file,
):
    upload = await create_upload_file("image.png")

    with pytest.raises(ImageMinSizeError):
        image_validator = UploadImageValidator(min_size=(30, 31))
        await image_validator(upload)

    with pytest.raises(ImageMinSizeError):
        image_validator = UploadImageValidator(min_size=(31, 30))
        await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_passes_image_file_with_valid_max_dimensions(
    create_upload_file,
):
    upload = await create_upload_file("image.png")
    image_validator = UploadImageValidator(max_size=(40, 30))
    assert await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_raises_error_if_uploaded_image_is_too_large(
    create_upload_file,
):
    upload = await create_upload_file("image.png")

    with pytest.raises(ImageMaxSizeError):
        image_validator = UploadImageValidator(max_size=(29, 30))
        await image_validator(upload)

    with pytest.raises(ImageMaxSizeError):
        image_validator = UploadImageValidator(max_size=(30, 29))
        await image_validator(upload)
