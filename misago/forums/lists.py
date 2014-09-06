from misago.acl import add_acl
from misago.readtracker import make_forums_read_aware

from misago.forums.models import Forum


__all__ = ['get_forums_list', 'get_forum_path']


def get_forums_list(user, parent=None):
    if not user.acl['visible_forums']:
        return []

    if parent:
        queryset = parent.get_descendants().order_by('lft')
    else:
        queryset = Forum.objects.all_forums()
    queryset_with_acl = queryset.filter(id__in=user.acl['visible_forums'])

    visible_forums = [f for f in queryset_with_acl]

    forums_dict = {}
    forums_list = []

    parent_level = parent.level + 1 if parent else 1

    for forum in visible_forums:
        forum.subforums = []
        forums_dict[forum.pk] = forum
        forums_list.append(forum)

        if forum.level > parent_level:
            forums_dict[forum.parent_id].subforums.append(forum)

    add_acl(user, forums_list)
    make_forums_read_aware(user, forums_list)

    for forum in reversed(visible_forums):
        if forum.acl['can_browse']:
            forum_parent = forums_dict.get(forum.parent_id)
            if forum_parent:
                forum_parent.threads += forum.threads
                forum_parent.posts += forum.posts

                if forum_parent.last_post_on and forum.last_post_on:
                    parent_last_post = forum_parent.last_post_on
                    forum_last_post = forum.last_post_on
                    update_last_thead = parent_last_post < forum_last_post
                elif not forum_parent.last_post_on and forum.last_post_on:
                    update_last_thead = True
                else:
                    update_last_thead = False

                if update_last_thead:
                    forum_parent.last_post_on = forum.last_post_on
                    forum_parent.last_thread_id = forum.last_thread_id
                    forum_parent.last_thread_title = forum.last_thread_title
                    forum_parent.last_thread_slug = forum.last_thread_slug
                    forum_parent.last_poster_name = forum.last_poster_name
                    forum_parent.last_poster_slug = forum.last_poster_slug

                if not forum.is_read:
                    forum_parent.is_read = False

    flat_list = []
    for forum in forums_list:
        if forum.role != "category" or forum.subforums:
            flat_list.append(forum)

    return flat_list


def get_forum_path(forum):
    forums_dict = Forum.objects.get_cached_forums_dict()

    forum_path = []
    while forum.level > 0:
        forum_path.append(forum)
        forum = forums_dict[forum.parent_id]
    return [f for f in reversed(forum_path)]
