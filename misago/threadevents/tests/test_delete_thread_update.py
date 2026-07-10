import pytest

from ..delete import delete_thread_update
from ..models import ThreadEvent


def test_delete_thread_deletes_thread_update(thread_update):
    delete_thread_update(thread_update)

    with pytest.raises(ThreadEvent.DoesNotExist):
        thread_update.refresh_from_db()

    assert not ThreadEvent.objects.exists()
