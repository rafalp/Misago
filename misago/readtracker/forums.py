from misago.readtracker.dates import is_date_tracked


__all__ = ['make_forums_read_aware', 'make_forums_read']


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

