import pytest

from ..models import ThreadUpdate
from ..delete import delete_thread_update


def test_delete_thread_deletes_thread_update(thread_update):
    delete_thread_update(thread_update)

    with pytest.raises(ThreadUpdate.DoesNotExist):
        thread_update.refresh_from_db()

    assert not ThreadUpdate.objects.exists()
