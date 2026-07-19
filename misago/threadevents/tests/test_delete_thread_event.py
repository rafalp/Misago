import pytest

from ..delete import delete_thread_event
from ..models import ThreadEvent


def test_delete_thread_deletes_thread_event(thread_event):
    delete_thread_event(thread_event)

    with pytest.raises(ThreadEvent.DoesNotExist):
        thread_event.refresh_from_db()

    assert not ThreadEvent.objects.exists()
