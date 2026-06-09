from django.http import HttpRequest
from django.utils import timezone

from ..categories.models import Category
from ..core.utils import slugify
from .enums import ThreadPinned
from .hide import hide_thread
from .hooks import create_thread_hook
from .lock import lock_thread
from .models import Thread
from .pin import pin_thread


def create_thread(
    category: Category,
    title: str,
    *,
    pinned: ThreadPinned = ThreadPinned.NONE,
    is_locked: bool = False,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> Thread:
    return create_thread_hook(
        _create_thread_action,
        category,
        title,
        pinned=pinned,
        is_locked=is_locked,
        is_hidden=is_hidden,
        commit=commit,
        request=request,
    )


def _create_thread_action(
    category: Category,
    title: str,
    *,
    pinned: ThreadPinned = ThreadPinned.NONE,
    is_locked: bool = False,
    is_hidden: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> Thread:
    timestamp = timezone.now()

    thread = Thread(
        category=category,
        title=title,
        slug=slugify(title),
        started_at=timestamp,
        last_posted_at=timestamp,
        starter_name="Misago",
        starter_slug="misago",
        last_poster_name="Misago",
        last_poster_slug="misago",
    )

    if pinned:
        pin_thread(
            thread,
            everywhere=pinned == ThreadPinned.EVERYWHERE,
            commit=False,
            request=request,
        )

    if is_locked:
        lock_thread(thread, commit=False, request=request)

    if is_hidden:
        if request:
            hide_thread(thread, request.user, commit=False, request=request)
        else:
            hide_thread(thread, "Misago", commit=False, request=request)

    if commit:
        thread.save()

    return thread
