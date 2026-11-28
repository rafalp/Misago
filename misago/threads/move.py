from django.http import HttpRequest

from ..attachments.models import Attachment
from ..categories.models import Category
from ..likes.models import Like
from ..notifications.models import Notification, WatchedThread
from ..polls.models import Poll, PollVote
from ..postedits.models import PostEdit
from ..readtracker.models import ReadThread
from ..search.threads import threads_search
from ..threadevents.models import ThreadEvent
from .hooks import move_post_hook, move_thread_hook
from .models import Post, Thread


def move_thread(
    thread: Thread,
    new_category: Category,
    update_search: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return move_thread_hook(
        _move_thread_action, thread, new_category, update_search, commit, request
    )


def _move_thread_action(
    thread: Thread,
    new_category: Category,
    update_search: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    if thread.category_id == new_category.id:
        return False

    thread.category = new_category

    Attachment.objects.filter(thread=thread).update(category=new_category)
    Like.objects.filter(thread=thread).update(category=new_category)
    Notification.objects.filter(thread=thread).update(category=new_category)
    Post.objects.filter(thread=thread).update(category=new_category)
    PostEdit.objects.filter(thread=thread).update(category=new_category)
    Poll.objects.filter(thread=thread).update(category=new_category)
    PollVote.objects.filter(thread=thread).update(category=new_category)
    ReadThread.objects.filter(thread=thread).update(category=new_category)
    ThreadEvent.objects.filter(thread=thread).update(category=new_category)
    WatchedThread.objects.filter(thread=thread).update(category=new_category)

    if commit:
        thread.save()

    if update_search:
        threads_search.update_thread(thread, {"category": new_category})
        threads_search.bulk_update_thread_posts(thread, {"category": new_category})

    return True


def move_post(
    post: Post,
    new_thread: Thread,
    update_search: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return move_post_hook(
        _move_post_action, post, new_thread, update_search, commit, request
    )


def _move_post_action(
    post: Post,
    new_thread: Thread,
    update_search: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    if post.thread_id == new_thread.id:
        return False

    new_category = new_thread.category

    post.thread = new_thread
    post.category = new_category

    Attachment.objects.filter(post=post).update(
        thread=new_thread, category=new_category
    )
    Like.objects.filter(post=post).update(thread=new_thread, category=new_category)
    Notification.objects.filter(post=post).update(
        thread=new_thread, category=new_category
    )
    PostEdit.objects.filter(post=post).update(thread=new_thread, category=new_category)

    if commit:
        post.save()

    if update_search:
        threads_search.update_post(
            post,
            {
                "category": new_category,
                "thread": new_thread,
                "thread_title": new_thread.title,
                "thread_is_hidden": new_thread.is_hidden,
                "thread_is_unapproved": new_thread.is_unapproved,
            },
        )

    return True
