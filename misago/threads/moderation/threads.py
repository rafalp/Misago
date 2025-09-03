from django.db import transaction
from django.utils import timezone

from ...notifications.tasks import delete_duplicate_watched_threads

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

    thread.set_title(new_title)
    thread.save(update_fields=["title", "slug"])

    thread.first_post.set_search_document(thread, "FIXME")
    thread.first_post.save(update_fields=["search_document"])

    thread.first_post.set_search_vector()
    thread.first_post.save(update_fields=["search_vector"])

    return True


@transaction.atomic
def pin_thread_globally(request, thread):
    if thread.weight == 2:
        return False

    thread.weight = 2
    thread.save(update_fields=["weight"])

    return True


@transaction.atomic
def pin_thread_locally(request, thread):
    if thread.weight == 1:
        return False

    thread.weight = 1
    thread.save(update_fields=["weight"])

    return True


@transaction.atomic
def unpin_thread(request, thread):
    if thread.weight == 0:
        return False

    thread.weight = 0
    thread.save(update_fields=["weight"])

    return True


@transaction.atomic
def move_thread(request, thread, new_category):
    if thread.category_id == new_category.pk:
        return False

    thread.move(new_category)
    thread.save()

    return True


@transaction.atomic
def merge_thread(request, thread, other_thread):
    thread.merge(other_thread)
    other_thread.delete()

    delete_duplicate_watched_threads.delay(thread.id)
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
    thread.save(update_fields=["is_unapproved", "has_unapproved_posts"])

    return True


@transaction.atomic
def open_thread(request, thread):
    if not thread.is_closed:
        return False

    thread.is_closed = False
    thread.save(update_fields=["is_closed"])

    return True


@transaction.atomic
def close_thread(request, thread):
    if thread.is_closed:
        return False

    thread.is_closed = True
    thread.save(update_fields=["is_closed"])

    return True


@transaction.atomic
def unhide_thread(request, thread):
    if not thread.is_hidden:
        return False

    thread.first_post.is_hidden = False
    thread.first_post.save(update_fields=["is_hidden"])
    thread.is_hidden = False
    thread.save(update_fields=["is_hidden"])

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
    thread.first_post.hidden_at = timezone.now()
    thread.first_post.save(
        update_fields=[
            "is_hidden",
            "hidden_by",
            "hidden_by_name",
            "hidden_by_slug",
            "hidden_at",
        ]
    )
    thread.is_hidden = True
    thread.save(update_fields=["is_hidden"])

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
