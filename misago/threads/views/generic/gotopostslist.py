from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.threads.views.generic.base import ViewBase


__all__ = ['ModeratedPostsListView', 'ReportedPostsListView']


class ModeratedPostsListView(ViewBase):
    template = 'misago/thread/gotolists/moderated.html'

    def allow_action(self, thread):
        if not thread.acl['can_review']:
            message = _("You don't have permission to review moderated posts.")
            raise PermissionDenied(message)

    def filter_posts_queryset(self, queryset):
        return queryset.filter(is_moderated=True)

    def dispatch(self, request, *args, **kwargs):
        relations = ['forum']
        thread = self.fetch_thread(request, select_related=relations, **kwargs)
        forum = thread.forum

        self.check_forum_permissions(request, forum)
        self.check_thread_permissions(request, thread)

        self.allow_action(thread)

        if not request.is_ajax():
            response = render(request, 'misago/errorpages/wrong_way.html')
            response.status_code = 405
            return response

        posts_qs = self.exclude_invisible_posts(
            thread.post_set, request.user, forum, thread)
        posts_qs = self.filter_posts_queryset(posts_qs)
        final_posts_qs = posts_qs.select_related('poster').order_by('-id')[:15]

        return self.render(request, {
            'forum': forum,
            'thread': thread,

            'posts_count': posts_qs.count(),
            'posts': final_posts_qs.iterator()
        })


class ReportedPostsListView(ModeratedPostsListView):
    template = 'misago/thread/gotolists/reported.html'

    def allow_action(self, thread):
        if not thread.acl['can_see_reports']:
            message = _("You don't have permission to see reports.")
            raise PermissionDenied(message)

    def filter_posts_queryset(self, queryset):
        return queryset.filter(is_reported=True)
