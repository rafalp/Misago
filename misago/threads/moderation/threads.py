from django.db.transaction import atomic
from django.utils import timezone

from misago.threads.events import record_event


__all__ = [
    'change_thread_title',
    'pin_thread_globally',
    'pin_thread_locally',
    'unpin_thread',
    'move_thread',
    'merge_thread',
    'approve_thread',
    'open_thread',
    'close_thread',
    'unhide_thread',
    'hide_thread',
    'delete_thread',
]


@atomic
def change_thread_title(request, thread, new_title):
    if thread.title != new_title:
        old_title = thread.title
        thread.set_title(new_title)
        thread.save(update_fields=['title', 'slug'])

        thread.first_post.set_search_document(thread.title)
        thread.first_post.save(update_fields=['search_document'])

        thread.first_post.update_search_vector()
        thread.first_post.save(update_fields=['search_vector'])

        record_event(request, thread, 'changed_title', {
            'old_title': old_title,
        })
        return True
    else:
        return False


@atomic
def pin_thread_globally(request, thread):
    if thread.weight != 2:
        thread.weight = 2
        record_event(request, thread, 'pinned_globally')
        return True
    else:
        return False


@atomic
def pin_thread_locally(request, thread):
    if thread.weight != 1:
        thread.weight = 1
        record_event(request, thread, 'pinned_locally')
        return True
    else:
        return False


@atomic
def unpin_thread(request, thread):
    if thread.weight:
        thread.weight = 0
        record_event(request, thread, 'unpinned')
        return True
    else:
        return False


@atomic
def move_thread(request, thread, new_category):
    if thread.category_id != new_category.pk:
        from_category = thread.category
        thread.move(new_category)

        record_event(
            request, thread, 'moved', {
                'from_category': {
                    'name': from_category.name,
                    'url': from_category.get_absolute_url(),
                },
            }
        )
        return True
    else:
        return False


@atomic
def merge_thread(request, thread, other_thread):
    thread.merge(other_thread)
    other_thread.delete()

    record_event(request, thread, 'merged', {
        'merged_thread': other_thread.title,
    })
    return True


@atomic
def approve_thread(request, thread):
    if thread.is_unapproved:
        thread.is_unapproved = False
        thread.first_post.is_unapproved = False
        thread.first_post.save(update_fields=['is_unapproved'])

        record_event(request, thread, 'approved')
        return True
    else:
        return False


@atomic
def open_thread(request, thread):
    if thread.is_closed:
        thread.is_closed = False
        record_event(request, thread, 'opened')
        return True
    else:
        return False


@atomic
def close_thread(request, thread):
    if not thread.is_closed:
        thread.is_closed = True
        record_event(request, thread, 'closed')
        return True
    else:
        return False


@atomic
def unhide_thread(request, thread):
    if thread.is_hidden:
        thread.first_post.is_hidden = False
        thread.first_post.save(update_fields=['is_hidden'])
        thread.is_hidden = False

        record_event(request, thread, 'unhid')

        if thread.pk == thread.category.last_thread_id:
            thread.category.synchronize()
            thread.category.save()

        return True
    else:
        return False


@atomic
def hide_thread(request, thread):
    if not thread.is_hidden:
        thread.first_post.is_hidden = True
        thread.first_post.hidden_by = request.user
        thread.first_post.hidden_by_name = request.user.username
        thread.first_post.hidden_by_slug = request.user.slug
        thread.first_post.hidden_on = timezone.now()
        thread.first_post.save(
            update_fields=[
                'is_hidden',
                'hidden_by',
                'hidden_by_name',
                'hidden_by_slug',
                'hidden_on',
            ]
        )
        thread.is_hidden = True

        record_event(request, thread, 'hid')

        if thread.pk == thread.category.last_thread_id:
            thread.category.synchronize()
            thread.category.save()

        return True
    else:
        return False


@atomic
def delete_thread(request, thread):
    thread.delete()

    thread.category.synchronize()
    thread.category.save()

    return True
