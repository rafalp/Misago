import pytest

from ..models import AttachmentType


@pytest.mark.asyncio
async def test_attachment_type_is_created_with_required_fields(db):
    attachment_type = await AttachmentType.create(
        name="Test",
        extensions=[".c", ".b", ".a"],
    )

    assert attachment_type
    assert attachment_type.id
    assert attachment_type.name == "Test"
    assert attachment_type.extensions == [".a", ".b", ".c"]
    assert attachment_type.mimetypes == []
    assert attachment_type.size_limit is None
    assert attachment_type.is_active is True


@pytest.mark.asyncio
async def test_attachment_type_is_created_with_all_fields(db):
    attachment_type = await AttachmentType.create(
        name="Test",
        extensions=[".c", ".b", ".a"],
        mimetypes=["c", "b", "a"],
        size_limit=1024,
        is_active=False,
    )

    assert attachment_type
    assert attachment_type.id
    assert attachment_type.name == "Test"
    assert attachment_type.extensions == [".a", ".b", ".c"]
    assert attachment_type.mimetypes == ["a", "b", "c"]
    assert attachment_type.size_limit is 1024
    assert attachment_type.is_active is False


@pytest.mark.asyncio
async def test_attachment_type_size_limit_is_removed(db):
    attachment_type = await AttachmentType.create(
        name="Test",
        extensions=[".c", ".b", ".a"],
        size_limit=1000,
    )

    updated_type = await attachment_type.update(size_limit_clear=True)
    assert updated_type.size_limit is None

    type_from_db = await attachment_type.fetch_from_db()
    assert type_from_db.size_limit is None
