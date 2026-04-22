from ..threads.models import Thread


def set_thread_has_updates(thread: Thread, commit: bool = True) -> bool:
    if thread.has_updates:
        return False

    thread.has_updates = True

    if commit:
        thread.save(update_fields=["has_updates"])

    return True
