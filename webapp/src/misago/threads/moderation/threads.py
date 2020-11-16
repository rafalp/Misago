from django.db import transaction
from django.utils import timezone

from ..events import record_event

__all__ = [
    "change_thread_title",
    "pin_thread_globally",
    "pin_thread_locally",
    "unpin_thread",
    "move_thread",
    "merge_thread",
    "approve_thread",
    "open_thread",
    "close_thread",
    "unhide_thread",
    "hide_thread",
    "delete_thread",
]


@transaction.atomic
def change_thread_title(request, thread, new_title):
    if thread.title == new_title:
        return False

    old_title = thread.title
    thread.set_title(new_title)
    thread.save(update_fields=["title", "slug"])

    thread.first_post.set_search_document(thread.title)
    thread.first_post.save(update_fields=["search_document"])

    thread.first_post.update_search_vector()
    thread.first_post.save(update_fields=["search_vector"])

    record_event(request, thread, "changed_title", {"old_title": old_title})
    return True


@transaction.atomic
def pin_thread_globally(request, thread):
    if thread.weight == 2:
        return False

    thread.weight = 2
    record_event(request, thread, "pinned_globally")
    return True


@transaction.atomic
def pin_thread_locally(request, thread):
    if thread.weight == 1:
        return False

    thread.weight = 1
    record_event(request, thread, "pinned_locally")
    return True


@transaction.atomic
def unpin_thread(request, thread):
    if thread.weight == 0:
        return False

    thread.weight = 0
    record_event(request, thread, "unpinned")
    return True


@transaction.atomic
def move_thread(request, thread, new_category):
    if thread.category_id == new_category.pk:
        return False

    from_category = thread.category
    thread.move(new_category)

    record_event(
        request,
        thread,
        "moved",
        {
            "from_category": {
                "name": from_category.name,
                "url": from_category.get_absolute_url(),
            }
        },
    )
    return True


@transaction.atomic
def merge_thread(request, thread, other_thread):
    thread.merge(other_thread)
    other_thread.delete()

    record_event(request, thread, "merged", {"merged_thread": other_thread.title})
    return True


@transaction.atomic
def approve_thread(request, thread):
    if not thread.is_unapproved:
        return False

    thread.first_post.is_unapproved = False
    thread.first_post.save(update_fields=["is_unapproved"])

    thread.is_unapproved = False

    unapproved_post_qs = thread.post_set.filter(is_unapproved=True)
    thread.has_unapproved_posts = unapproved_post_qs.exists()

    record_event(request, thread, "approved")
    return True


@transaction.atomic
def open_thread(request, thread):
    if not thread.is_closed:
        return False

    thread.is_closed = False
    record_event(request, thread, "opened")
    return True


@transaction.atomic
def close_thread(request, thread):
    if thread.is_closed:
        return False

    thread.is_closed = True
    record_event(request, thread, "closed")
    return True


@transaction.atomic
def unhide_thread(request, thread):
    if not thread.is_hidden:
        return False

    thread.first_post.is_hidden = False
    thread.first_post.save(update_fields=["is_hidden"])
    thread.is_hidden = False

    record_event(request, thread, "unhid")

    if thread.pk == thread.category.last_thread_id:
        thread.category.synchronize()
        thread.category.save()

    return True


@transaction.atomic
def hide_thread(request, thread):
    if thread.is_hidden:
        return False

    thread.first_post.is_hidden = True
    thread.first_post.hidden_by = request.user
    thread.first_post.hidden_by_name = request.user.username
    thread.first_post.hidden_by_slug = request.user.slug
    thread.first_post.hidden_on = timezone.now()
    thread.first_post.save(
        update_fields=[
            "is_hidden",
            "hidden_by",
            "hidden_by_name",
            "hidden_by_slug",
            "hidden_on",
        ]
    )
    thread.is_hidden = True

    record_event(request, thread, "hid")

    if thread.pk == thread.category.last_thread_id:
        thread.category.synchronize()
        thread.category.save()

    return True


@transaction.atomic
def delete_thread(request, thread):
    thread.delete()

    thread.category.synchronize()
    thread.category.save()

    return True
