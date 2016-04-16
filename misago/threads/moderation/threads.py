from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import ugettext as _

from misago.threads.events import record_event


@atomic
def pin_thread_globally(user, thread):
    if thread.weight != 2:
        message = _("%(user)s pinned thread globally.")
        record_event(user, thread, "bookmark", message, {'user': user})

        thread.weight = 2
        thread.save(update_fields=['has_events', 'weight'])
        return True
    else:
        return False


@atomic
def pin_thread_locally(user, thread):
    if thread.weight != 1:
        message = _("%(user)s pinned thread locally.")
        record_event(user, thread, "bookmark", message, {'user': user})

        thread.weight = 1
        thread.save(update_fields=['has_events', 'weight'])
        return True
    else:
        return False


@atomic
def unpin_thread(user, thread):
    if thread.weight:
        message = _("%(user)s unpinned thread.")
        record_event(user, thread, "circle", message, {'user': user})

        thread.weight = 0
        thread.save(update_fields=['has_events', 'weight'])
        return True
    else:
        return False


@atomic
def move_thread(user, thread, new_category):
    if thread.category_id != new_category.pk:
        message = _("%(user)s moved thread from %(category)s.")
        record_event(user, thread, "arrow-right", message, {
            'user': user,
            'category': thread.category
        })

        thread.move(new_category)
        thread.save(update_fields=['has_events', 'category'])
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
    if thread.is_unapproved:
        message = _("%(user)s approved thread.")
        record_event(user, thread, "check", message, {'user': user})

        thread.is_closed = False
        thread.first_post.is_unapproved = False
        thread.first_post.save(update_fields=['is_unapproved'])
        thread.synchronize()
        thread.save(update_fields=['has_events', 'is_unapproved'])
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
        message = _("%(user)s hidden thread.")
        record_event(user, thread, "eye-slash", message, {'user': user})

        thread.first_post.is_hidden = True
        thread.first_post.hidden_by = user
        thread.first_post.hidden_by_name = user.username
        thread.first_post.hidden_by_slug = user.slug
        thread.first_post.hidden_on = timezone.now()
        thread.first_post.save(update_fields=[
            'is_hidden',
            'hidden_by',
            'hidden_by_name',
            'hidden_by_slug',
            'hidden_on',
        ])

        thread.is_hidden = True
        thread.save(update_fields=['has_events', 'is_hidden'])
        return True
    else:
        return False


@atomic
def delete_thread(user, thread):
    thread.delete()
    return True
