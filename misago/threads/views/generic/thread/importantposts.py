from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.threads.permissions import exclude_invisible_posts
from misago.threads.views.generic.base import ViewBase


__all__ = ['ModeratedPostsView', 'ReportedPostsView']


class ModeratedPostsView(ViewBase):
    template = ''

    def allow_action(self, forum):
        pass

    def filter_posts_queryset(self, queryset):
        return queryset.filter(is_moderated=True)

    def dispatch(self, request, *args, **kwargs):
        relations = ['forum']
        thread = self.fetch_thread(request, select_related=relations, **kwargs)
        forum = thread.forum

        self.check_forum_permissions(request, forum)
        self.check_thread_permissions(request, thread)

        self.allow_action(forum)

        if not request.is_ajax():
            response = render(request, 'misago/errorpages/wrong_way.html')
            response.status_code = 405
            return response

        queryset = exclude_invisible_posts(
            thread.post_set, request.user, forum)
        queryset = self.filter_posts_queryset(queryset)

        return self.render(request, {
            'forum': forum,
            'thread': get_forum_path(forum),

            'posts_count': queryset.count(),
            'posts': queryset.order_by('-id')[:15]
        })


class ReportedPostsView(ModeratedPostsView):
    pass
