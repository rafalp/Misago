from .models import Thread


def lock_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return _lock_thread_action(thread, commit, request)


def _lock_thread_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if not thread.is_locked:
        return False

    thread.is_locked = True

    if commit:
        thread.save()

    return True


def unlock_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return _unlock_thread_action(thread, commit, request)


def _unlock_thread_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if thread.is_locked:
        return False

    thread.is_locked = False

    if commit:
        thread.save()

    return True
