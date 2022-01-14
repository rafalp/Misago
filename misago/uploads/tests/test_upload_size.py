import pytest
from starlette.datastructures import UploadFile

from ..utils import get_upload_size


@pytest.mark.asyncio
async def test_get_upload_size_returns_accurate_size_of_upload():
    file = UploadFile("test.txt", content_type="text")
    await file.write("test".encode("utf-8"))
    assert await get_upload_size(file) == 4
