from ..threads.models import Thread
from .models import ThreadUpdate


def set_thread_has_updates(thread: Thread, commit: bool = True) -> bool:
    if thread.has_updates:
        return False

    thread.has_updates = True

    if commit:
        thread.save(update_fields=["has_updates"])

    return True


def sync_thread_has_updates(thread: Thread, commit: bool = True) -> bool:
    org_has_updates = thread.has_updates

    thread.has_updates = ThreadUpdate.objects.filter(thread=thread).exists()

    if org_has_updates == thread.has_updates:
        return False

    if commit:
        thread.save(update_fields=["has_updates"])

    return True
