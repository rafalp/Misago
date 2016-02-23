from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.categories.lists import get_category_path
from misago.core.shortcuts import validate_slug
from misago.readtracker import threadstracker

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

    def get_posts(self, user, category, thread, kwargs):
        queryset = self.get_posts_queryset(user, category, thread)
        queryset = self.exclude_invisible_posts(queryset, user, category, thread)
        page = paginate(queryset, kwargs.get('page', 0),
                        settings.MISAGO_POSTS_PER_PAGE,
                        settings.MISAGO_THREAD_TAIL)

        posts = []
        for post in page.object_list:
            post.category = category
            post.thread = thread

            add_acl(user, post)
            posts.append(post)

        if page.next_page_first_item:
            add_events_to_posts(
                user, thread, posts, page.next_page_first_item.posted_on)
        else:
            add_events_to_posts(user, thread, posts)

        return page, posts

    def get_posts_queryset(self, user, category, thread):
        return thread.post_set.select_related(
            'poster',
            'poster__rank',
            'poster__ban_cache',
            'poster__online_tracker'
        ).order_by('id')

    def allow_reply_thread(self, user, thread):
        allow_reply_thread(user, thread)

    def dispatch(self, request, *args, **kwargs):
        relations = ['category', 'starter', 'last_poster', 'first_post']
        thread = self.fetch_thread(request, select_related=relations, **kwargs)
        category = thread.category

        self.check_category_permissions(request, category)
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
                queryset = self.get_posts_queryset(request.user, category, thread)
                response = posts_actions.handle_post(request, queryset)
                if response:
                    return response

        page, posts = self.get_posts(request.user, category, thread, kwargs)
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

            'category': category,
            'path': get_category_path(category),

            'thread': thread,
            'thread_actions': thread_actions,
            'thread_reply_message': thread_reply_message,

            'posts': posts,
            'posts_actions': posts_actions,
            'selected_posts': posts_actions.get_selected_ids(),

            'paginator': page.paginator,
            'page': page,
        })
