from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from ..acl.test import patch_user_acl
from ..categories.models import Category
from ..core.utils import slugify
from ..users.test import create_test_user
from .checksums import update_post_checksum
from .models import Poll, Post, Thread

default_category_acl = {
    "can_see": 1,
    "can_browse": 1,
    "can_see_all_threads": 1,
    "can_see_own_threads": 0,
    "can_hide_threads": 0,
    "can_approve_content": 0,
    "can_edit_posts": 0,
    "can_hide_posts": 0,
    "can_hide_own_posts": 0,
    "can_merge_threads": 0,
    "can_close_threads": 0,
}


def patch_category_acl(acl_patch=None):
    def patch_acl(_, user_acl):
        category = Category.objects.get(slug="first-category")
        category_acl = user_acl["categories"][category.id]
        category_acl.update(default_category_acl)
        if acl_patch:
            category_acl.update(acl_patch)
        cleanup_patched_acl(user_acl, category_acl, category)

    return patch_user_acl(patch_acl)


def patch_other_user_category_acl(acl_patch=None):
    def patch_acl(user, user_acl):
        if user.slug != "otheruser":
            return

        category = Category.objects.get(slug="first-category")
        category_acl = user_acl["categories"][category.id]
        category_acl.update(default_category_acl)
        if acl_patch:
            category_acl.update(acl_patch)
        cleanup_patched_acl(user_acl, category_acl, category)

    return patch_user_acl(patch_acl)


def patch_other_category_acl(acl_patch=None):
    def patch_acl(_, user_acl):
        src_category = Category.objects.get(slug="first-category")
        category_acl = user_acl["categories"][src_category.id].copy()

        dst_category = Category.objects.get(slug="other-category")
        user_acl["categories"][dst_category.id] = category_acl

        category_acl.update(default_category_acl)
        if acl_patch:
            category_acl.update(acl_patch)

        cleanup_patched_acl(user_acl, category_acl, dst_category)

    return patch_user_acl(patch_acl)


def patch_private_threads_acl(acl_patch=None):
    def patch_acl(_, user_acl):
        category = Category.objects.private_threads()
        category_acl = user_acl["categories"][category.id]
        category_acl.update(default_category_acl)
        if acl_patch:
            category_acl.update(acl_patch)
        cleanup_patched_acl(user_acl, category_acl, category)

    return patch_user_acl(patch_acl)


def other_user_cant_use_private_threads(user, user_acl):
    if user.slug == "otheruser":
        user_acl.update({"can_use_private_threads": False})


def create_category_acl_patch(category_slug, acl_patch):
    def created_category_acl_patch(_, user_acl):
        category = Category.objects.get(slug=category_slug)
        category_acl = user_acl["categories"].get(category.id, {})
        category_acl.update(default_category_acl)
        if acl_patch:
            category_acl.update(acl_patch)
        cleanup_patched_acl(user_acl, category_acl, category)

    return created_category_acl_patch


def cleanup_patched_acl(user_acl, category_acl, category):
    visible_categories = user_acl["visible_categories"]
    browseable_categories = user_acl["browseable_categories"]

    if not category_acl["can_see"] and category.id in visible_categories:
        visible_categories.remove(category.id)

    if not category_acl["can_see"] and category.id in browseable_categories:
        browseable_categories.remove(category.id)

    if not category_acl["can_browse"] and category.id in browseable_categories:
        browseable_categories.remove(category.id)

    if category_acl["can_see"] and category.id not in visible_categories:
        visible_categories.append(category.id)

    if category_acl["can_browse"] and category.id not in browseable_categories:
        browseable_categories.append(category.id)


User = get_user_model()


def post_thread(
    category,
    title="Test thread",
    poster="Tester",
    is_global=False,
    is_pinned=False,
    is_unapproved=False,
    is_hidden=False,
    is_closed=False,
    started_on=None,
):
    started_on = started_on or timezone.now()

    kwargs = {
        "category": category,
        "title": title,
        "slug": slugify(title),
        "started_on": started_on,
        "last_post_on": started_on,
        "is_unapproved": is_unapproved,
        "is_hidden": is_hidden,
        "is_closed": is_closed,
    }

    if is_global:
        kwargs["weight"] = 2
    elif is_pinned:
        kwargs["weight"] = 1

    try:
        kwargs.update(
            {
                "starter": poster,
                "starter_name": poster.username,
                "starter_slug": poster.slug,
                "last_poster": poster,
                "last_poster_name": poster.username,
                "last_poster_slug": poster.slug,
            }
        )
    except AttributeError:
        kwargs.update(
            {
                "starter_name": poster,
                "starter_slug": slugify(poster),
                "last_poster_name": poster,
                "last_poster_slug": slugify(poster),
            }
        )

    thread = Thread.objects.create(**kwargs)
    reply_thread(
        thread,
        poster=poster,
        posted_on=started_on,
        is_hidden=is_hidden,
        is_unapproved=is_unapproved,
    )

    return thread


def reply_thread(
    thread,
    poster="Tester",
    message="I am test message",
    is_unapproved=False,
    is_hidden=False,
    is_event=False,
    is_protected=False,
    has_reports=False,
    has_open_reports=False,
    posted_on=None,
):
    posted_on = posted_on or thread.last_post_on + timedelta(minutes=5)

    kwargs = {
        "category": thread.category,
        "thread": thread,
        "original": message,
        "parsed": message,
        "checksum": "nope",
        "posted_on": posted_on,
        "updated_on": posted_on,
        "is_event": is_event,
        "is_unapproved": is_unapproved,
        "is_hidden": is_hidden,
        "is_protected": is_protected,
        "has_reports": has_reports,
        "has_open_reports": has_open_reports,
    }

    try:
        kwargs.update({"poster": poster, "poster_name": poster.username})
    except AttributeError:
        kwargs.update({"poster_name": poster})

    post = Post.objects.create(**kwargs)

    update_post_checksum(post)
    post.save()

    thread.synchronize()
    thread.save()
    thread.category.synchronize()
    thread.category.save()

    return post


def post_poll(thread, poster):
    poll = Poll.objects.create(
        category=thread.category,
        thread=thread,
        poster=poster,
        poster_name=poster.username,
        poster_slug=poster.slug,
        question="Lorem ipsum dolor met?",
        choices=[
            {"hash": "aaaaaaaaaaaa", "label": "Alpha", "votes": 1},
            {"hash": "bbbbbbbbbbbb", "label": "Beta", "votes": 0},
            {"hash": "gggggggggggg", "label": "Gamma", "votes": 2},
            {"hash": "dddddddddddd", "label": "Delta", "votes": 1},
        ],
        allowed_choices=2,
        votes=4,
    )

    # one user voted for Alpha choice
    try:
        user = User.objects.get(slug="user")
    except User.DoesNotExist:
        user = create_test_user("User", "user@example.com")

    poll.pollvote_set.create(
        category=thread.category,
        thread=thread,
        voter=user,
        voter_name=user.username,
        voter_slug=user.slug,
        choice_hash="aaaaaaaaaaaa",
    )

    # test user voted on third and last choices
    poll.pollvote_set.create(
        category=thread.category,
        thread=thread,
        voter=poster,
        voter_name=poster.username,
        voter_slug=poster.slug,
        choice_hash="gggggggggggg",
    )
    poll.pollvote_set.create(
        category=thread.category,
        thread=thread,
        voter=poster,
        voter_name=poster.username,
        voter_slug=poster.slug,
        choice_hash="dddddddddddd",
    )

    # somebody else voted on third option before being deleted
    poll.pollvote_set.create(
        category=thread.category,
        thread=thread,
        voter_name="deleted",
        voter_slug="deleted",
        choice_hash="gggggggggggg",
    )

    return poll


def like_post(post, liker=None, username=None):
    if not post.last_likes:
        post.last_likes = []

    if liker:
        like = post.postlike_set.create(
            category=post.category,
            thread=post.thread,
            liker=liker,
            liker_name=liker.username,
            liker_slug=liker.slug,
        )

        post.last_likes = [
            {"id": liker.id, "username": liker.username}
        ] + post.last_likes
    else:
        like = post.postlike_set.create(
            category=post.category,
            thread=post.thread,
            liker_name=username,
            liker_slug=slugify(username),
        )

        post.last_likes = [{"id": None, "username": username}] + post.last_likes

    post.likes += 1
    post.save()

    return like
