from django.utils import timezone

from ..readtracker import poststracker
from .models import Post


def record_event(request, thread, event_type, context=None, commit=True):
    time_now = timezone.now()

    event = Post.objects.create(
        category=thread.category,
        thread=thread,
        poster=request.user,
        poster_name=request.user.username,
        original="-",
        parsed="-",
        posted_on=time_now,
        updated_on=time_now,
        is_event=True,
        event_type=event_type,
        event_context=context,
    )

    thread.has_events = True
    thread.set_last_post(event)
    if commit:
        thread.save()

    if not (thread.is_hidden and thread.is_unapproved):
        thread.category.set_last_thread(thread)
        if commit:
            thread.category.save()

    poststracker.save_read(request.user, event)

    return event
