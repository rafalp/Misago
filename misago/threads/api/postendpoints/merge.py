from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.acl import add_acl
from misago.conf import settings
from misago.threads.permissions import exclude_invisible_posts
from misago.threads.serializers import PostSerializer


MERGE_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL


class MergeError(Exception):
    def __init__(self, msg):
        self.msg = msg


def posts_merge_endpoint(request, thread):
    if not thread.acl['can_merge_posts']:
        raise PermissionDenied(_("You can't merge posts in this thread."))

    try:
        posts = clean_posts_for_merge(request, thread)
    except MergeError as e:
        return Response({'detail': e.msg}, status=400)

    first_post, merged_posts = posts[0], posts[1:]
    for post in merged_posts:
        post.merge(first_post)
        post.delete()

    if first_post.pk == thread.first_post_id:
        first_post.set_search_document(thread.title)
    else:
        first_post.set_search_document()

    first_post.save()

    first_post.update_search_vector()
    first_post.save(update_fields=['search_vector'])

    thread.synchronize()
    thread.save()

    thread.category.synchronize()
    thread.category.save()

    first_post.thread = thread
    first_post.category = thread.category

    add_acl(request.user, first_post)

    return Response(PostSerializer(first_post, context={'user': request.user}).data)


def clean_posts_for_merge(request, thread):
    try:
        posts_ids = list(map(int, request.data.get('posts', [])))
    except (ValueError, TypeError):
        raise MergeError(_("One or more post ids received were invalid."))

    if len(posts_ids) < 2:
        raise MergeError(_("You have to select at least two posts to merge."))
    elif len(posts_ids) > MERGE_LIMIT:
        message = ungettext(
            "No more than %(limit)s post can be merged at single time.",
            "No more than %(limit)s posts can be merged at single time.",
            MERGE_LIMIT,
        )
        raise MergeError(message % {'limit': MERGE_LIMIT})

    posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)
    posts_queryset = posts_queryset.select_for_update().filter(id__in=posts_ids).order_by('id')

    posts = []
    for post in posts_queryset:
        if post.is_event:
            raise MergeError(_("Events can't be merged."))
        if post.is_hidden and not (
                post.pk == thread.first_post_id or thread.category.acl['can_hide_posts']
        ):
            raise MergeError(_("You can't merge posts the content you can't see."))

        if not posts:
            posts.append(post)
        else:
            authorship_error = _("Posts made by different users can't be merged.")
            if posts[0].poster_id:
                if post.poster_id != posts[0].poster_id:
                    raise MergeError(authorship_error)
            else:
                if post.poster_id or post.poster_name != posts[0].poster_name:
                    raise MergeError(authorship_error)

            if posts[0].pk != thread.first_post_id:
                if (posts[0].is_hidden != post.is_hidden or
                        posts[0].is_unapproved != post.is_unapproved):
                    raise MergeError(_("Posts with different visibility can't be merged."))

            posts.append(post)

    if len(posts) != len(posts_ids):
        raise MergeError(_("One or more posts to merge could not be found."))

    return posts
