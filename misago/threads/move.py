from django.http import HttpRequest

from ..attachments.models import Attachment
from ..categories.models import Category
from ..likes.models import Like
from ..notifications.models import Notification, WatchedThread
from ..polls.models import Poll, PollVote
from ..postedits.models import PostEdit
from ..readtracker.models import ReadThread
from ..threadupdates.models import ThreadUpdate
from .hooks import move_thread_hook
from .models import Post, Thread


def move_thread(
    thread: Thread,
    new_category: Category,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return move_thread_hook(_move_thread_action, thread, new_category, commit, request)


def _move_thread_action(
    thread: Thread,
    new_category: Category,
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
    ThreadUpdate.objects.filter(thread=thread).update(category=new_category)
    WatchedThread.objects.filter(thread=thread).update(category=new_category)

    if commit:
        thread.save()

    return True
