from django.db.models import Q
from django.shortcuts import redirect

from misago.acl import add_acl
from misago.forums.lists import get_forum_path
from misago.readtracker import threadstracker
from misago.users.online.utils import get_user_state

from misago.threads.events import add_events_to_posts
from misago.threads.paginator import paginate
from misago.threads.views.generic.base import ViewBase


__all__ = ['ThreadView']


class ThreadView(ViewBase):
    """
    Basic view for threads
    """
    template = 'misago/thread/replies.html'

    def get_posts(self, user, forum, thread, kwargs):
        queryset = self.get_posts_queryset(user, forum, thread)
        page = paginate(queryset, kwargs.get('page', 0), 10, 5)

        posts = []
        for post in page.object_list:
            add_acl(user, post)
            if post.poster:
                poster_state = get_user_state(post.poster, user.acl)
                post.poster.online_state = poster_state
            posts.append(post)

        if page.next_page_first_item:
            add_events_to_posts(
                user, thread, posts, page.next_page_first_item.posted_on)
        else:
            add_events_to_posts(user, thread, posts)

        return page, posts

    def get_posts_queryset(self, user, forum, thread):
        queryset = thread.post_set.select_related(
            'poster', 'poster__rank', 'poster__bancache', 'poster__online')

        if user.is_authenticated():
            if forum.acl['can_review_moderated_content']:
                visibility_condition = Q(is_moderated=False) | Q(poster=user)
                queryset = queryset.filter(visibility_condition)
        else:
            queryset = queryset.filter(is_moderated=False)

        return queryset

    def dispatch(self, request, *args, **kwargs):
        relations = ['forum', 'starter', 'last_poster', 'first_post']
        thread = self.fetch_thread(request, select_related=relations, **kwargs)
        forum = thread.forum

        self.check_forum_permissions(request, forum)
        self.check_thread_permissions(request, thread)

        threadstracker.make_read_aware(request.user, thread)

        page, posts = self.get_posts(request.user, forum, thread, kwargs)
        threadstracker.make_posts_read_aware(thread, posts)
        threadstracker.read_thread(request.user, thread, posts[-1])

        return self.render(request, {
            'forum': forum,
            'path': get_forum_path(forum),
            'thread': thread,
            'posts': posts,
            'page': page,
            'paginator': page.paginator,
        })
