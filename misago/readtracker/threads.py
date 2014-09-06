from misago.readtracker.dates import is_date_tracked


__all__ = ['make_threads_read_aware', 'make_threads_read']


def make_threads_read_aware(user, threads):
    if user.is_anonymous():
        make_threads_read(threads)
        return None

    threads_dict = {}
    for thread in threads:
        thread.is_read = not is_date_tracked(thread.last_post_on)
        if thread.is_read:
            thread.unread_posts = 0
        else:
            thread.unread_posts = thread.replies
        threads_dict[thread.pk] = thread

    for record in user.threadread_set.filter(thread__in=threads_dict.keys()):
        if record.thread_id in threads_dict:
            thread = threads_dict[record.thread_id]
            thread.is_read = record.last_read_on >= thread.last_post_on
            if thread.is_read:
                thread.unread_posts = 0
            else:
                thread.unread_posts = thread.replies - record.read_replies


def make_threads_read(threads):
    for thread in threads:
        thread.unread_posts = 0
        thread.is_read = True

