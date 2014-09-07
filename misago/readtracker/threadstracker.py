from misago.readtracker import forumstracker
from misago.readtracker.dates import cutoff_date, is_date_tracked


__all__ = ['make_read_aware', 'read_thread']


def make_read_aware(user, target):
    if hasattr(target, '__iter__'):
        make_threads_read_aware(user, target)
    else:
        make_thread_read_aware(user, target)


def make_threads_read_aware(user, threads):
    if user.is_anonymous():
        make_read(threads)
        return None

    threads_dict = {}
    for thread in threads:
        thread.is_read = not is_date_tracked(thread.last_post_on)
        if thread.is_read:
            thread.unread_replies = 0
        else:
            thread.unread_replies = thread.replies
        threads_dict[thread.pk] = thread

    for record in user.threadread_set.filter(thread__in=threads_dict.keys()):
        if record.thread_id in threads_dict:
            thread = threads_dict[record.thread_id]
            thread.is_read = record.last_read_on >= thread.last_post_on
            if thread.is_read:
                thread.unread_replies = 0
            else:
                thread.unread_replies = thread.replies - record.read_replies


def make_read(threads):
    for thread in threads:
        thread.unread_replies = 0
        thread.is_read = True


def make_thread_read_aware(user, thread):
    thread.is_read = True
    if user.is_authenticated() and is_date_tracked(thread.last_post_on):
        try:
            record = user.threadread_set.filter(thread=thread).all()[0]
            thread.last_read_on = record.last_read_on
            thread.is_read = thread.last_post_on <= record.last_read_on
            thread.read_record = record
        except IndexError:
            thread.read_record = None
            thread.is_read = False
            thread.last_read_on = cutoff_date()


def make_posts_read_aware(thread, posts):
    try:
        is_thread_read = thread.is_read
    except AttributeError:
        raise ValueError("thread passed make_posts_read_aware should be "
                         "read aware too via make_thread_read_aware")

    if is_thread_read:
        for post in posts:
            post.is_read = True
    else:
        for post in posts:
            if is_date_tracked(post.updated_on):
                post.is_read = post.updated_on <= thread.last_read_on
            else:
                post.is_read = True


def count_read_replies(user, thread, last_read_reply):
    if last_read_reply.updated_on >= thread.last_read_on:
        return 0
    else:
        last_reply_date = last_read_reply.last_read_on
        queryset = thread.post_set.filter(last_read_on__lte=last_reply_date)
        queryset = queryset.filter(is_moderated=False)
        return queryset.count()


def read_thread(user, thread, last_read_reply):
    if not thread.is_read:
        if thread.last_read_on < last_read_reply.updated_on:
            sync_record(user, thread, last_read_reply)


def sync_record(user, thread, last_read_reply):
    read_replies = count_read_replies(user, thread, last_read_reply)
    if thread.read_record:
        thread.read_record.read_replies = read_replies
        thread.read_record.last_read_on = last_read_reply.updated_on
        thread.read_record.save(update_fields=['read_replies', 'last_read_on'])
    else:
         user.threadread_set.create(
            forum=thread.forum,
            thread=thread,
            read_replies=read_replies,
            last_read_on=last_read_reply.updated_on)

    if last_read_reply.updated_on == thread.last_post_on:
        forumstracker.sync_record(user, thread.forum)
