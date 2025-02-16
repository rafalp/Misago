import pytest

from ..attachments.models import Attachment


@pytest.fixture()
def teardown_attachments(db):
    existing_attachments: list[int] = list(
        Attachment.objects.values_list("id", flat=True)
    )

    try:
        yield
    finally:
        for attachment in Attachment.objects.exclude(id__in=existing_attachments):
            attachment.delete()
