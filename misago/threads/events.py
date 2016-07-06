from django.utils import timezone

from misago.threads.models import Post


def record_event(request, thread, event, context=None, commit=True):
    time_now = timezone.now()

    event_post = Post.objects.create(
        category=thread.category,
        thread=thread,
        poster=request.user,
        poster_name=request.user.username,
        poster_ip=request.user_ip,
        original='-',
        parsed='-',
        posted_on=time_now,
        updated_on=time_now,
        is_event=True,
        event_type=event,
        event_context=context,
    )

    thread.set_last_post(event_post)
    if commit:
        thread.save()

    if not (thread.is_hidden and thread.is_unapproved):
        thread.category.set_last_thread(thread)
        if commit:
            thread.category.save()

    return event_post
