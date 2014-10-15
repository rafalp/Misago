from django.db.models import F
from django.utils import timezone

from misago.threads.permissions import exclude_invisible_threads

from misago.readtracker import signals
from misago.readtracker.dates import is_date_tracked


__all__ = ['make_read_aware', 'sync_record']


def make_read_aware(user, forums):
    if user.is_anonymous():
        make_read(forums)
        return None

    forums_dict = {}
    for forum in forums:
        forum.is_read = not is_date_tracked(user, forum.last_post_on)
        forums_dict[forum.pk] = forum

    for record in user.forumread_set.filter(forum__in=forums_dict.keys()):
        if not forum.is_read and record.forum_id in forums_dict:
            forum = forums_dict[record.forum_id]
            forum.is_read = record.last_read_on >= forum.last_post_on


def make_read(forums):
    for forum in forums:
        forum.is_read = True


def sync_record(user, forum):
    recorded_threads = forum.thread_set.filter(
        last_post_on__gt=user.reads_cutoff)
    recorded_threads = exclude_invisible_threads(recorded_threads, user, forum)

    all_threads_count = recorded_threads.count()

    read_threads = user.threadread_set.filter(
        forum=forum, last_read_on__gt=user.joined_on)
    read_threads_count = read_threads.filter(
        thread__last_post_on__lte=F("last_read_on")).count()

    forum_is_read = read_threads_count == all_threads_count

    if forum_is_read:
        signals.forum_read.send(sender=user, forum=forum)

    try:
        forum_record = user.forumread_set.filter(forum=forum).all()[0]
        if forum_is_read:
            forum_record.last_read_on = forum_record.last_read_on
        else:
            forum_record.last_read_on = user.reads_cutoff
        forum_record.save(update_fields=['last_read_on'])
    except IndexError:
        if forum_is_read:
            last_read_on = timezone.now()
        else:
            last_read_on = user.joined_on

        forum_record = user.forumread_set.create(
            forum=forum,
            last_read_on=last_read_on)
