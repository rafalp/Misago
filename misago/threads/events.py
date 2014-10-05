from cgi import escape

from misago.acl import add_acl

from misago.threads.checksums import update_event_checksum
from misago.threads.models import Event


__all__ = ['record_event', 'add_events_to_posts']


LINK_TEMPLATE = '<a href="%s" class="event-%s">%s</a>'
NAME_TEMPLATE = '<strong class="event-%s">%s</strong>'


def format_message(message, links):
    if links:
        formats = {}
        for name, value in links.items():
            if isinstance(value, basestring):
                formats[name] = NAME_TEMPLATE % (escape(name), escape(value))
            else:
                try:
                    replaces = (
                        escape(value.get_absolute_url()),
                        escape(name),
                        escape(unicode(value))
                    )
                except AttributeError:
                    replaces = (
                        escape(value[1]),
                        escape(name),
                        escape(value[0])
                    )

                formats[name] = LINK_TEMPLATE % replaces
        return message % formats
    else:
        return message


def record_event(user, thread, icon, message, links=None):
    event = Event.objects.create(
        forum=thread.forum,
        thread=thread,
        author=user,
        author_name=user.username,
        author_slug=user.slug,
        icon=icon,
        message=format_message(message, links))

    update_event_checksum(event)
    event.save(update_fields=['checksum'])

    thread.has_events = True
    return event


def add_events_to_posts(user, thread, posts, delimeter=None):
    if thread.has_events:
        real_add_events_to_posts(user, thread, posts, delimeter)
    else:
        for post in posts:
            post.events = []


def real_add_events_to_posts(user, thread, posts, delimeter=None):
    start_date = posts[0].posted_on
    events_queryset = thread.event_set.filter(occured_on__gte=start_date)
    if delimeter:
        events_queryset = events_queryset.filter(occured_on__lt=delimeter)
    events_queryset = events_queryset.order_by('id')

    acl = user.acl['forums'].get(thread.forum_id, {})
    if not acl.get('can_hide_events'):
        events_queryset = events_queryset.filter(is_hidden=False)

    events = [e for e in events_queryset]
    add_acl(user, events)

    for i, post in enumerate(posts[:-1]):
        post.events = []
        while events and events[0].occured_on < posts[i + 1].posted_on:
            post.events.append(events.pop(0))

    posts[-1].events = events
