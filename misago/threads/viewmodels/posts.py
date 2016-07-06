from django.conf import settings

from misago.acl import add_acl
from misago.core.shortcuts import paginate, pagination_dict
from misago.readtracker.threadstracker import make_posts_read_aware
from misago.threads.permissions.threads import exclude_invisible_posts
from misago.threads.serializers import ThreadPostSerializer
from misago.users.online.utils import make_users_status_aware


class ViewModel(object):
    def __init__(self, request, thread, page):
        posts_queryset = self.get_queryset(request, thread.thread)

        list_page = paginate(posts_queryset, page, settings.MISAGO_POSTS_PER_PAGE, settings.MISAGO_POSTS_TAIL)
        paginator = pagination_dict(list_page, include_page_range=False)

        posts = list(list_page.object_list)
        posters = []

        for post in posts:
            post.category = thread.category
            post.thread = thread.thread

            if post.poster and post.poster not in posters:
                posters.append(post.poster)

        add_acl(request.user, posts)

        make_posts_read_aware(request.user, thread.thread, posts)
        make_users_status_aware(request.user, posters)

        self.posts = posts
        self.paginator = paginator

    def get_queryset(self, request, thread):
        queryset = thread.post_set.select_related(
            'poster',
            'poster__rank',
            'poster__ban_cache',
            'poster__online_tracker'
        ).order_by('id')
        return exclude_invisible_posts(request.user, thread.category, queryset)

    def get_frontend_context(self):
        context = {
            'results': ThreadPostSerializer(self.posts, many=True).data
        }

        context.update(self.paginator)

        return context

    def get_template_context(self):
        return {
            'posts': self.posts,
            'paginator': self.paginator
        }


class ThreadPosts(ViewModel):
    pass
