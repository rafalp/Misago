from django.conf import settings

from misago.acl import add_acl
from misago.core.shortcuts import paginate, pagination_dict
from misago.readtracker.threadstracker import make_posts_read_aware
from misago.users.online.utils import make_users_status_aware

from ..permissions.threads import exclude_invisible_posts
from ..serializers import PostSerializer
from ..utils import add_likes_to_posts


class ViewModel(object):
    def __init__(self, request, thread, page):
        try:
            thread_model = thread.unwrap()
        except AttributeError:
            thread_model = thread

        posts_queryset = self.get_queryset(request, thread_model)

        list_page = paginate(posts_queryset, page, settings.MISAGO_POSTS_PER_PAGE, settings.MISAGO_POSTS_TAIL)
        paginator = pagination_dict(list_page, include_page_range=False)

        posts = list(list_page.object_list)
        posters = []

        for post in posts:
            post.category = thread.category
            post.thread = thread_model

            if post.poster:
                posters.append(post.poster)

        add_acl(request.user, posts)

        make_posts_read_aware(request.user, thread_model, posts)
        make_users_status_aware(request.user, posters)

        if thread.category.acl['can_see_posts_likes']:
            add_likes_to_posts(request.user, posts)

        self._user = request.user

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
            'results': PostSerializer(self.posts, many=True, context={'user': self._user}).data
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
