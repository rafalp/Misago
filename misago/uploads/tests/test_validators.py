import os
from unittest.mock import Mock

import pytest
from starlette.datastructures import UploadFile

from ..errors import (
    UploadContentTypeError,
    UploadImageError,
    UploadImageMaxSizeError,
    UploadImageMinSizeError,
    UploadMaxSizeError,
)
from ..validators import (
    UploadContentTypeValidator,
    UploadImageValidator,
    UploadSizeValidator,
)

TEST_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")


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


async def create_upload_file(filename):
    upload = UploadFile(filename)
    with open(os.path.join(TEST_FILES_DIR, filename), "rb") as fp:
        await upload.write(fp.read())
    return upload


@pytest.mark.asyncio
async def test_upload_image_validator_passes_valid_image_file():
    upload = await create_upload_file("image.png")
    image_validator = UploadImageValidator()
    assert await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_raises_error_if_upload_is_not_image():
    upload = await create_upload_file("text_file.txt")
    image_validator = UploadImageValidator()
    with pytest.raises(UploadImageError):
        await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_passes_image_file_with_valid_min_dimensions():
    upload = await create_upload_file("image.png")
    image_validator = UploadImageValidator(min_size=(30, 20))
    assert await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_raises_error_if_uploaded_image_is_too_small():
    upload = await create_upload_file("image.png")

    with pytest.raises(UploadImageMinSizeError):
        image_validator = UploadImageValidator(min_size=(30, 31))
        await image_validator(upload)

    with pytest.raises(UploadImageMinSizeError):
        image_validator = UploadImageValidator(min_size=(31, 30))
        await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_passes_image_file_with_valid_max_dimensions():
    upload = await create_upload_file("image.png")
    image_validator = UploadImageValidator(max_size=(40, 30))
    assert await image_validator(upload)


@pytest.mark.asyncio
async def test_upload_image_validator_raises_error_if_uploaded_image_is_too_large():
    upload = await create_upload_file("image.png")

    with pytest.raises(UploadImageMaxSizeError):
        image_validator = UploadImageValidator(max_size=(29, 30))
        await image_validator(upload)

    with pytest.raises(UploadImageMaxSizeError):
        image_validator = UploadImageValidator(max_size=(30, 29))
        await image_validator(upload)
