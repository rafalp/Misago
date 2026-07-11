from ..threads.models import Thread
from .models import ThreadEvent


def ensure_thread_has_events(thread: Thread, commit: bool = True) -> bool:
    if thread.has_events:
        return False

    thread.has_events = True

    if commit:
        thread.save(update_fields=["has_events"])

    return True


def sync_thread_has_updates(thread: Thread, commit: bool = True) -> bool:
    org_has_updates = thread.has_events

    thread.has_events = ThreadEvent.objects.filter(thread=thread).exists()

    if org_has_updates == thread.has_events:
        return False

    if commit:
        thread.save(update_fields=["has_events"])

    return True
