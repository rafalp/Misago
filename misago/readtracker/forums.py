from django.db.models import F
from django.utils import timezone

from misago.threads.permissions import exclude_invisible_threads

from misago.readtracker.dates import cutoff_date, is_date_tracked


__all__ = ['make_forums_read_aware', 'make_forums_read', 'sync_forum_record']


def make_forums_read_aware(user, forums):
    if user.is_anonymous():
        make_forums_read(forums)
        return None

    forums_dict = {}
    for forum in forums:
        forum.is_read = not is_date_tracked(forum.last_post_on)
        forums_dict[forum.pk] = forum

    for record in user.forumread_set.filter(forum__in=forums_dict.keys()):
        if record.forum_id in forums_dict:
            forum = forums_dict[record.forum_id]
            forum.is_read = record.last_cleared_on >= forum.last_post_on


def make_forums_read(forums):
    for forum in forums:
        forum.is_read = True


def sync_forum_record(user, forum):
    recorded_threads = forum.thread_set.filter(last_post_on__gt=cutoff_date())
    recorded_threads = exclude_invisible_threads(user, forum, recorded_threads)

    all_threads_count = recorded_threads.count()

    read_threads = user.threadread_set.filter(
        forum=forum, last_read_on__gt=cutoff_date())
    read_threads_count = read_threads.filter(
        thread__last_post_on__lte=F("last_read_on")).count()

    forum_is_read = read_threads_count == all_threads_count

    try:
        forum_record = user.forumread_set.filter(forum=forum).all()[0]
        forum_record.last_updated_on = timezone.now()
        if forum_is_read:
            forum_record.last_cleared_on = forum_record.last_updated_on
        forum_record.save(update_fields=['last_updated_on', 'last_cleared_on'])
    except IndexError:
        if forum_is_read:
            cleared_on = timezone.now()
        else:
            cleared_on = cutoff_date()

        forum_record = user.forumread_set.create(
            forum=forum,
            last_updated_on=timezone.now(),
            last_cleared_on=cleared_on)
