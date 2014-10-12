from django.db.transaction import atomic
from django.utils.translation import ugettext_lazy, ugettext as _

from misago.threads.events import record_event


@atomic
def label_thread(user, thread, label):
    if not thread.label_id or thread.label_id != label.pk:
        if thread.label_id:
            message = _("%(user)s changed thread label to %(label)s.")
        else:
            message = _("%(user)s set thread label to %(label)s.")

        record_event(user, thread, "tag", message, {
            'user': user,
            'label': label.name
        })

        thread.label = label

        thread.save(update_fields=['has_events', 'label'])
        return True
    else:
        return False


@atomic
def unlabel_thread(user, thread):
    if thread.label_id:
        thread.label = None

        message = _("%(user)s removed thread label.")
        record_event(user, thread, "tag", message, {'user': user})

        thread.save(update_fields=['has_events', 'label'])
        return True
    else:
        return False


@atomic
def pin_thread(user, thread):
    if not thread.is_pinned:
        thread.is_pinned = True

        message = _("%(user)s pinned thread.")
        record_event(user, thread, "star", message, {'user': user})

        thread.save(update_fields=['has_events', 'is_pinned'])
        return True
    else:
        return False


@atomic
def unpin_thread(user, thread):
    if thread.is_pinned:
        message = _("%(user)s unpinned thread.")
        record_event(user, thread, "circle", message, {'user': user})

        thread.is_pinned = False
        thread.save(update_fields=['has_events', 'is_pinned'])
        return True
    else:
        return False


@atomic
def move_thread(user, thread, new_forum):
    if thread.forum_id != new_forum.pk:
        message = _("%(user)s moved thread from %(forum)s.")
        record_event(user, thread, "arrow-right", message, {
            'user': user,
            'forum': thread.forum
        })

        thread.move(new_forum)
        thread.save(update_fields=['has_events', 'forum'])
        return True
    else:
        return False


@atomic
def merge_thread(user, thread, other_thread):
    message = _("%(user)s merged in %(thread)s.")
    record_event(user, thread, "arrow-right", message, {
        'user': user,
        'thread': other_thread.title
    })

    thread.merge(other_thread)
    other_thread.delete()
    return True


@atomic
def approve_thread(user, thread):
    if thread.is_moderated:
        message = _("%(user)s approved thread.")
        record_event(user, thread, "check", message, {'user': user})

        thread.is_closed = False
        thread.first_post.is_moderated = False
        thread.first_post.save(update_fields=['is_moderated'])
        thread.synchronize()
        thread.save(update_fields=['has_events', 'is_moderated'])
        return True
    else:
        return False


@atomic
def open_thread(user, thread):
    if thread.is_closed:
        message = _("%(user)s opened thread.")
        record_event(user, thread, "unlock-alt", message, {'user': user})

        thread.is_closed = False
        thread.save(update_fields=['has_events', 'is_closed'])
        return True
    else:
        return False


@atomic
def close_thread(user, thread):
    if not thread.is_closed:
        message = _("%(user)s closed thread.")
        record_event(user, thread, "lock", message, {'user': user})

        thread.is_closed = True
        thread.save(update_fields=['has_events', 'is_closed'])
        return True
    else:
        return False


@atomic
def unhide_thread(user, thread):
    if thread.is_hidden:
        message = _("%(user)s made thread visible.")
        record_event(user, thread, "eye", message, {'user': user})

        thread.first_post.is_hidden = False
        thread.first_post.save(update_fields=['is_hidden'])
        thread.is_hidden = False
        thread.save(update_fields=['has_events', 'is_hidden'])
        thread.synchronize()
        thread.save()
        return True
    else:
        return False


@atomic
def hide_thread(user, thread):
    if not thread.is_hidden:
        message = _("%(user)s hid thread.")
        record_event(user, thread, "eye-slash", message, {'user': user})

        thread.is_hidden = True
        thread.save(update_fields=['has_events', 'is_hidden'])
        return True
    else:
        return False


@atomic
def delete_thread(user, thread):
    thread.delete()
    return True
