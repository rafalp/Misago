from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.core.shortcuts import validate_slug
from misago.forums.lists import get_forum_path
from misago.readtracker import threadstracker
from misago.users.online.utils import get_user_state

from misago.threads.events import add_events_to_posts
from misago.threads.paginator import paginate
from misago.threads.permissions import allow_reply_thread
from misago.threads.reports import make_posts_reports_aware
from misago.threads.views.generic.base import ViewBase
from misago.threads.views.generic.thread.postsactions import PostsActions
from misago.threads.views.generic.thread.threadactions import ThreadActions


__all__ = ['ThreadView']


class ThreadView(ViewBase):
    """
    Basic view for threads
    """
    ThreadActions = ThreadActions
    PostsActions = PostsActions
    template = 'misago/thread/replies.html'

    def get_posts(self, user, forum, thread, kwargs):
        queryset = self.get_posts_queryset(user, forum, thread)
        queryset = self.exclude_invisible_posts(queryset, user, forum, thread)
        page = paginate(queryset, kwargs.get('page', 0),
                        settings.MISAGO_POSTS_PER_PAGE,
                        settings.MISAGO_THREAD_TAIL)

        posts = []
        for post in page.object_list:
            post.forum = forum
            post.thread = thread

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
        return thread.post_set.select_related(
            'poster',
            'poster__rank',
            'poster__ban_cache',
            'poster__online_tracker'
        ).order_by('id')

    def allow_reply_thread(self, user, thread):
        allow_reply_thread(user, thread)

    def dispatch(self, request, *args, **kwargs):
        relations = ['forum', 'starter', 'last_poster', 'first_post']
        thread = self.fetch_thread(request, select_related=relations, **kwargs)
        forum = thread.forum

        self.check_forum_permissions(request, forum)
        self.check_thread_permissions(request, thread)

        validate_slug(thread, kwargs['thread_slug'])

        threadstracker.make_read_aware(request.user, thread)

        thread_actions = self.ThreadActions(user=request.user, thread=thread)
        posts_actions = self.PostsActions(user=request.user, thread=thread)

        if request.method == 'POST':
            if thread_actions.query_key in request.POST:
                response = thread_actions.handle_post(request, thread)
                if response:
                    return response
            if posts_actions.query_key in request.POST:
                queryset = self.get_posts_queryset(request.user, forum, thread)
                response = posts_actions.handle_post(request, queryset)
                if response:
                    return response

        page, posts = self.get_posts(request.user, forum, thread, kwargs)
        make_posts_reports_aware(request.user, thread, posts)

        threadstracker.make_posts_read_aware(request.user, thread, posts)
        threadstracker.read_thread(request.user, thread, posts[-1])

        try:
            allow_reply_thread(request.user, thread)
            thread_reply_message = None
        except PermissionDenied as e:
            thread_reply_message = unicode(e)

        return self.render(request, {
            'link_name': request.resolver_match.view_name,
            'links_params': {
                'thread_id': thread.id, 'thread_slug': thread.slug
            },

            'forum': forum,
            'path': get_forum_path(forum),

            'thread': thread,
            'thread_actions': thread_actions,
            'thread_reply_message': thread_reply_message,

            'posts': posts,
            'posts_actions': posts_actions,
            'selected_posts': posts_actions.get_selected_ids(),

            'paginator': page.paginator,
            'page': page,
        })
