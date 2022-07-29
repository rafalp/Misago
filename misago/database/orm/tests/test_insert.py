import pytest

from ....attachments.models import AttachmentType
from ....tables import attachment_types
from ..exceptions import InvalidColumnError
from ..mapper import ObjectMapper

mapper = ObjectMapper()

mapper.set_mapping(attachment_types, AttachmentType)


@pytest.mark.asyncio
async def test_data_can_be_inserted_to_database_and_object_is_returned(db):
    result = await mapper.query_table(attachment_types).insert(
        {
            "name": "Test",
            "extensions": [".c", ".b", ".a"],
            "mimetypes": [],
            "size_limit": 42,
            "is_active": True,
        }
    )

    assert isinstance(result, AttachmentType)
    assert result.id
    assert result.name == "Test"
    assert result.extensions == [".c", ".b", ".a"]
    assert result.mimetypes == []
    assert result.size_limit == 42
    assert result.is_active is True


@pytest.mark.asyncio
async def test_insert_raises_error_if_column_name_is_invalid(db):
    with pytest.raises(InvalidColumnError):
        await mapper.query_table(attachment_types).insert(
            {
                "name": "Test",
                "extensions": [".c", ".b", ".a"],
                "invalid": True,
                "size_limit": 42,
                "is_active": True,
            }
        )


@pytest.mark.asyncio
async def test_data_can_be_bulk_inserted_to_database(db):
    root_query = mapper.query_table(attachment_types)
    org_count = await root_query.count()

    await root_query.bulk_insert(
        [
            {
                "name": "Test",
                "extensions": [".c", ".b", ".a"],
                "mimetypes": [],
                "size_limit": 42,
                "is_active": True,
            },
            {
                "name": "Test2",
                "extensions": [".z", ".g"],
                "mimetypes": ["some/test"],
                "size_limit": 72,
                "is_active": False,
            },
        ]
    )

    new_count = await root_query.count()
    assert new_count - org_count == 2
