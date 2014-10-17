from django.db.models import F
from django.utils import timezone

from misago.threads.permissions import exclude_invisible_threads

from misago.readtracker import signals
from misago.readtracker.dates import is_date_tracked
from misago.readtracker.models import ForumRead


__all__ = ['make_read_aware', 'sync_record']


def make_read_aware(user, forums):
    if not hasattr(forums, '__iter__'):
        forums = [forums]

    if user.is_anonymous():
        make_read(forums)
        return None

    forums_dict = {}
    for forum in forums:
        forum.last_read_on = user.reads_cutoff
        forum.is_read = not is_date_tracked(forum.last_post_on, user)
        if not forum.is_read:
            forums_dict[forum.pk] = forum

    if forums_dict:
        for record in user.forumread_set.filter(forum__in=forums_dict.keys()):
            forum = forums_dict[record.forum_id]
            forum.last_read_on = record.last_read_on
            forum.is_read = forum.last_read_on >= forum.last_post_on


def make_read(forums):
    now = timezone.now()
    for forum in forums:
        forum.last_read_on = now
        forum.is_read = True


def sync_record(user, forum):
    cutoff_date = user.reads_cutoff

    try:
        forum_record = user.forumread_set.get(forum=forum)
        if forum_record.last_read_on > cutoff_date:
            cutoff_date = forum_record.last_read_on
    except ForumRead.DoesNotExist:
        forum_record = None

    recorded_threads = forum.thread_set.filter(last_post_on__gt=cutoff_date)
    recorded_threads = exclude_invisible_threads(recorded_threads, user, forum)

    all_threads_count = recorded_threads.count()

    read_threads = user.threadread_set.filter(
        forum=forum, last_read_on__gt=cutoff_date)
    read_threads_count = read_threads.filter(
        thread__last_post_on__lte=F("last_read_on")).count()

    forum_is_read = read_threads_count == all_threads_count

    if forum_is_read:
        signals.forum_read.send(sender=user, forum=forum)

    if forum_record:
        if forum_is_read:
            forum_record.last_read_on = forum_record.last_read_on
        else:
            forum_record.last_read_on = cutoff_date
        forum_record.save(update_fields=['last_read_on'])
    else:
        if forum_is_read:
            last_read_on = timezone.now()
        else:
            last_read_on = cutoff_date

        forum_record = user.forumread_set.create(
            forum=forum,
            last_read_on=last_read_on)


def read_forum(user, forum):
    try:
        forum_record = user.forumread_set.get(forum=forum)
        forum_record.last_read_on = timezone.now()
        forum_record.save(update_fields=['last_read_on'])
    except ForumRead.DoesNotExist:
        user.forumread_set.create(forum=forum, last_read_on=timezone.now())
    signals.forum_read.send(sender=user, forum=forum)

