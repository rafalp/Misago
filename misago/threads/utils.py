from urllib.parse import urlparse

from django.db import transaction
from django.urls import Resolver404, resolve

from ..attachments.models import Attachment
from ..likes.models import Like
from ..polls.models import Poll, PollVote
from ..postedits.models import PostEdit
from ..threadevents.models import ThreadEvent

from .anonymize import anonymize_post_last_likes
from .models import Post, Thread


SUPPORTED_THREAD_ROUTES = {
    "misago:thread": "thread_id",
    "misago:thread-post": "thread_id",
    "misago:thread-post-last": "thread_id",
    "misago:thread-post-unapproved": "thread_id",
    "misago:thread-post-unread": "thread_id",
    "misago:thread-post-solution": "thread_id",
}


def get_thread_id_from_url(request, url):
    clean_url = str(url).strip()
    url_bits = urlparse(clean_url)

    if url_bits.netloc and url_bits.netloc != request.get_host():
        return None

    if url_bits.path.startswith(request.get_host()):
        clean_path = url_bits.path.lstrip(request.get_host())
    else:
        clean_path = url_bits.path

    wsgi_alias = request.path_info[: len(request.path_info) * -1]
    if wsgi_alias and not clean_path.startswith(wsgi_alias):
        return None

    try:
        resolution = resolve(clean_path[len(wsgi_alias) :])
    except Resolver404:
        return None

    if not resolution.namespaces:
        return None

    url_name = "%s:%s" % (":".join(resolution.namespaces), resolution.url_name)
    kwargname = SUPPORTED_THREAD_ROUTES.get(url_name)

    if not kwargname:
        return None

    try:
        return int(resolution.kwargs.get(kwargname))
    except (TypeError, ValueError):
        return None


def remove_private_threads_without_members(user):
    queryset = Thread.objects.filter(
        id__in=user.privatethreadmember_set.values("thread_id"),
    ).order_by("-id")
    for thread in queryset.iterator(chunk_size=50):
        if thread.privatethreadmember_set.count() <= 1:
            with transaction.atomic():
                thread.delete()


def anonymize_user_in_thread_events(user, **kwargs):
    ThreadEvent.objects.filter(actor=user).update(actor_name=user.username)
    ThreadEvent.objects.filter(hidden_by=user).update(hidden_by_name=user.username)
    ThreadEvent.objects.content_object(user).update(detail=user.username)


def anonymize_user_in_likes(user, **kwargs):
    queryset = Post.objects.filter(
        id__in=Like.objects.filter(user=user).values("post_id")
    ).order_by("-id")

    for post in queryset.iterator(chunk_size=50):
        anonymize_post_last_likes(user, post)


def update_usernames(user, **kwargs):
    Thread.objects.filter(starter=user).update(
        starter_name=user.username, starter_slug=user.slug
    )

    Thread.objects.filter(last_poster=user).update(
        last_poster_name=user.username, last_poster_slug=user.slug
    )

    Thread.objects.filter(solution_by=user).update(
        solution_by_name=user.username,
        solution_by_slug=user.slug,
    )
    Thread.objects.filter(solution_selected_by=user).update(
        solution_selected_by_name=user.username,
        solution_selected_by_slug=user.slug,
    )

    ThreadEvent.objects.filter(actor=user).update(actor_name=user.username)
    ThreadEvent.objects.filter(hidden_by=user).update(hidden_by_name=user.username)
    ThreadEvent.objects.content_object(user).update(detail=user.username)

    Post.objects.filter(poster=user).update(poster_name=user.username)
    Post.objects.filter(last_editor=user).update(
        last_editor_name=user.username, last_editor_slug=user.slug
    )
    Post.objects.filter(hidden_by=user).update(
        hidden_by_name=user.username, hidden_by_slug=user.slug
    )

    PostEdit.objects.filter(user=user).update(
        user_name=user.username, user_slug=user.slug
    )
    PostEdit.objects.filter(hidden_by=user).update(
        hidden_by_name=user.username, hidden_by_slug=user.slug
    )

    Like.objects.filter(user=user).update(
        user_name=user.username, user_slug=user.slug
    )

    liked_posts = Post.objects.filter(
        id__in=Like.objects.filter(user=user).values("post_id"),
    )
    for post in liked_posts.iterator(chunk_size=50):
        update_post_last_likes = False
        for like in post.last_likes:
            if like["id"] == user.id:
                like["username"] = user.username
                update_post_last_likes = True
        if update_post_last_likes:
            post.save(update_fields=["last_likes"])

    Attachment.objects.filter(uploader=user).update(
        uploader_name=user.username, uploader_slug=user.slug
    )

    Poll.objects.filter(starter=user).update(
        starter_name=user.username, starter_slug=user.slug
    )

    PollVote.objects.filter(voter=user).update(
        voter_name=user.username, voter_slug=user.slug
    )
