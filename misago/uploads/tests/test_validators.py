from unittest.mock import Mock, patch

import pytest

from ..errors import UploadContentTypeError, UploadMaxSizeError
from ..validators import UploadContentTypeValidator, UploadSizeValidator


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
    upload = Mock(file=Mock(seek=Mock(), tell=Mock(return_value=1024)))

    exact_size_validator = UploadSizeValidator(1024)
    assert await exact_size_validator(upload) == upload

    greater_size_validator = UploadSizeValidator(2048)
    assert await greater_size_validator(upload) == upload


@pytest.mark.asyncio
async def test_upload_size_validator_raises_error_for_too_large_uploads():
    with pytest.raises(UploadMaxSizeError):
        upload = Mock(file=Mock(seek=Mock(), tell=Mock(return_value=1024)))
        exact_size_validator = UploadSizeValidator(512)
        await exact_size_validator(upload)
