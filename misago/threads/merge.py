from typing import Iterable

from django import forms
from django.db.models import Model
from django.http import HttpRequest
from django.utils.translation import pgettext

from ..attachments.models import Attachment
from ..likes.models import Like
from ..likes.synchronize import synchronize_post_likes
from ..notifications.models import Notification, WatchedThread
from ..polls.models import Poll, PollVote
from ..postedits.models import PostEdit
from ..postgres.delete import delete_all
from ..readtracker.models import ReadThread
from ..threadupdates.models import ThreadUpdate
from .hooks import (
    get_post_merge_conflicts_hook,
    get_post_merge_form_fields_hook,
    get_thread_merge_conflicts_hook,
    get_thread_merge_form_fields_hook,
    merge_posts_hook,
    merge_threads_hook,
)
from .models import Post, Thread


def get_thread_merge_conflicts(
    threads: Iterable[Thread], request: HttpRequest | None = None
) -> dict[str, list[Model]]:
    return get_thread_merge_conflicts_hook(
        _get_thread_merge_conflicts_action, threads, request
    )


def _get_thread_merge_conflicts_action(
    threads: Iterable[Thread], request: HttpRequest | None = None
) -> dict[str, list[Model]]:
    threads_dict = {thread.id: thread for thread in threads}
    conflicts = {}

    if polls := list(Poll.objects.filter(thread__in=threads).order_by("thread")):
        for poll in polls:
            poll.thread = threads_dict[poll.thread_id]
            poll.category = poll.thread.category

        conflicts["poll"] = polls

    if solution := [thread for thread in threads if thread.solution_id]:
        conflicts["solution"] = sorted(solution, key=lambda t: t.id)

    return conflicts


def get_thread_merge_form_fields(
    conflicts: dict[str, list[Model]],
    request: HttpRequest | None = None,
) -> dict[str, forms.Field]:
    return get_thread_merge_form_fields_hook(
        _get_thread_merge_form_fields_action, conflicts, request
    )


def _get_thread_merge_form_fields_action(
    conflicts: dict[str, list[Model]],
    request: HttpRequest | None = None,
) -> dict[str, forms.Field]:
    fields: dict[str, forms.Field] = {}

    if "poll" in conflicts and len(conflicts["poll"]) > 1:
        fields["poll"] = forms.TypedChoiceField(
            label=pgettext("thread merge poll conflict", "Poll"),
            help_text=pgettext(
                "thread merge poll conflict",
                "Select poll to keep in the merged thread. Other polls will be deleted.",
            ),
            coerce=int,
            choices=[
                (poll.id, f"{poll.question} ({poll.thread.title})")
                for poll in conflicts["poll"]
            ],
        )

    if "solution" in conflicts and len(conflicts["solution"]) > 1:
        fields["solution"] = forms.TypedChoiceField(
            label=pgettext("thread merge solution conflict", "Solution"),
            help_text=pgettext(
                "thread merge solution conflict",
                "Select a solution to use in the merged thread. Other solutions will be unmarked. The selected solution can be changed later.",
            ),
            coerce=int,
            choices=[
                (thread.id, f"{thread.title}") for thread in conflicts["solution"]
            ],
        )

    return fields


def merge_threads(
    target: Thread,
    threads: Iterable[Thread],
    conflicts: dict[str, Model],
    request: HttpRequest | None = None,
) -> Thread:
    return merge_threads_hook(
        _merge_threads_action,
        target,
        threads,
        conflicts,
        request,
    )


def _merge_threads_action(
    target: Thread,
    threads: Iterable[Thread],
    conflicts: dict[str, Model],
    request: HttpRequest | None = None,
) -> Thread:
    new_category = target.category

    poll = conflicts.get("poll")
    if poll and poll.thread_id != target.id:
        if target.has_poll:
            delete_all(PollVote, thread=target)
            delete_all(Poll, thread=target)

        poll.category = new_category
        poll.thread = target
        poll.save()

        PollVote.objects.filter(poll=poll).update(thread=target, category=new_category)

    solution = conflicts.get("solution")
    if solution and solution != target:
        target.solution_id = solution.solution_id
        target.solution_posted_at = solution.solution_posted_at
        target.solution_by_id = solution.solution_by_id
        target.solution_by_name = solution.solution_by_name
        target.solution_by_slug = solution.solution_by_slug
        target.solution_selected_at = solution.solution_selected_at
        target.solution_selected_by_id = solution.solution_selected_by_id
        target.solution_selected_by_name = solution.solution_selected_by_name
        target.solution_selected_by_slug = solution.solution_selected_by_slug

    for thread in threads:
        category = thread.category
        if category.last_thread_id == thread.id:
            category.last_thread = None
            category.save(update_fields=["last_thread"])

    Attachment.objects.filter(thread__in=threads).update(
        thread=target, category=new_category
    )
    Like.objects.filter(thread__in=threads).update(thread=target, category=new_category)
    Notification.objects.filter(thread__in=threads).update(
        thread=target, category=new_category
    )
    Post.objects.filter(thread__in=threads).update(thread=target, category=new_category)
    PostEdit.objects.filter(thread__in=threads).update(
        thread=target, category=new_category
    )
    ThreadUpdate.objects.filter(thread__in=threads).update(
        thread=target, category=new_category
    )
    WatchedThread.objects.filter(thread__in=threads).update(
        thread=target, category=new_category
    )

    thread_ids = [thread.id for thread in threads]

    delete_all(PollVote, thread=thread_ids)
    delete_all(Poll, thread=thread_ids)
    delete_all(ReadThread, thread=thread_ids)

    delete_all(Thread, id=thread_ids)

    target.save()

    return target


def get_post_merge_conflicts(
    posts: Iterable[Post], request: HttpRequest | None = None
) -> dict[str, list[Model]]:
    return get_post_merge_conflicts_hook(
        _get_post_merge_conflicts_action, posts, request
    )


def _get_post_merge_conflicts_action(
    posts: Iterable[Post], request: HttpRequest | None = None
) -> dict[str, list[Model]]:
    return {}  # No post merge conflicts are possible in standard Misago


def get_post_merge_form_fields(
    conflicts: dict[str, list[Model]],
    request: HttpRequest | None = None,
) -> dict[str, forms.Field]:
    return get_post_merge_form_fields_hook(
        _get_post_merge_form_fields_action, conflicts, request
    )


def _get_post_merge_form_fields_action(
    conflicts: dict[str, list[Model]],
    request: HttpRequest | None = None,
) -> dict[str, forms.Field]:
    fields: dict[str, forms.Field] = {}
    return fields  # No post merge conflicts are possible in standard Misago


def merge_posts(
    target: Post,
    posts: Iterable[Post],
    conflicts: dict[str, Model],
    request: HttpRequest | None = None,
) -> Post:
    return merge_posts_hook(
        _merge_posts_action,
        target,
        posts,
        conflicts,
        request,
    )


MISAGO_POST_METADATA = (
    "attachments",
    "highlight_code",
    "posts",
    "mentions",
)


def _merge_posts_action(
    target: Post,
    posts: Iterable[Post],
    conflicts: dict[str, Model],
    request: HttpRequest | None = None,
) -> Post:
    thread = target.thread

    for post in posts:
        target.original += f"\n\n{post.original}"
        target.parsed += f"\n{post.parsed}"
        target.search_document += f"\n\n{post.search_document}"

        for key in MISAGO_POST_METADATA:
            merge_post_metadata(key, target, post)

        save_thread = False
        if thread.solution_id == post.id:
            thread.solution = target
            save_thread = True
        if thread.last_post_id == post.id:
            thread.last_post = target
            save_thread = True
        if save_thread:
            thread.save()

    Attachment.objects.filter(post__in=posts).update(post=target)
    Like.objects.filter(post__in=posts).update(post=target)
    Notification.objects.filter(post__in=posts).update(post=target)
    PostEdit.objects.filter(post__in=posts).update(post=target)

    post_ids = [post.id for post in posts]

    delete_all(Post, id=post_ids)

    synchronize_post_likes(target, commit=False, request=request)

    target.set_search_vector()
    target.save()

    return target


def merge_post_metadata(key: str, target: Post, source: Post):
    target_meta = target.metadata.get(key)
    source_meta = source.metadata.get(key)

    if target_meta and source_meta:
        target.metadata[key] = sorted(set(target_meta).union(set(source_meta)))
    elif source_meta:
        target.metadata[key] = source_meta
