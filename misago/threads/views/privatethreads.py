from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.forums.models import Forum

from misago.threads.models import Thread, ThreadParticipant
from misago.threads.permissions import (allow_use_private_threads,
                                        allow_see_private_thread,
                                        allow_see_private_post,
                                        exclude_invisible_private_threads)
from misago.threads.views import generic


def private_threads_view(klass):
    """
    decorator for making views check allow_use_private_threads
    """
    def dispatch(self, request, *args, **kwargs):
        allow_use_private_threads(request.user)

        return super(self.__class__, self).dispatch(
            request, *args, **kwargs)
    klass.dispatch = dispatch
    return klass


class PrivateThreadsMixin(object):
    """
    Mixin is used to make views use different permission tests
    """
    def get_forum(self, request, lock=False, **kwargs):
        forum = Forum.objects.private_threads()
        add_acl(request.user, forum)
        return forum

    def check_forum_permissions(self, request, forum):
        add_acl(request.user, forum)
        allow_use_private_threads(request.user)

    def fetch_thread(self, request, lock=False, select_related=None,
                     queryset=None, **kwargs):
        queryset = queryset or Thread.objects
        if lock:
            queryset = queryset.select_for_update()

        select_related = select_related or []
        if not 'forum' in select_related:
            select_related.append('forum')
        queryset = queryset.select_related(*select_related)

        where = {'id': kwargs.get('thread_id')}
        thread = get_object_or_404(queryset, **where)
        if thread.forum.special_role != 'private_threads':
            raise Http404()
        return thread

    def fetch_thread_participants(self, thread):
        thread.participants_list = []
        participants_qs = ThreadParticipant.objects.filter(thread=thread)
        participants_qs = participants_qs.select_related('user')
        for participant in participants_qs:
            participant.thread = thread
            thread.participants_list.append(participant)

    def check_thread_permissions(self, request, thread):
        add_acl(request.user, thread.forum)
        add_acl(request.user, thread)

        self.fetch_thread_participants(thread)

        allow_see_private_thread(request.user, thread)
        allow_use_private_threads(request.user)

    def check_post_permissions(self, request, post):
        add_acl(request.user, post.forum)
        add_acl(request.user, post.thread)
        add_acl(request.user, post)

        self.fetch_thread_participants(post.thread)

        allow_see_private_post(request.user, post)
        allow_see_private_thread(request.user, post.thread)
        allow_use_private_threads(request.user)


class PrivateThreads(generic.Threads):
    def get_queryset(self):
        threads_qs = Forum.objects.private_threads().thread_set
        return exclude_invisible_private_threads(threads_qs, self.user)


class PrivateThreadsFiltering(generic.ThreadsFiltering):
    def get_available_filters(self):
        filters = super(PrivateThreadsFiltering, self).get_available_filters()

        if self.user.acl['can_moderate_private_threads']:
            filters.append({
                'type': 'reported',
                'name': _("With reported posts"),
                'is_label': False,
            })

        return filters


@private_threads_view
class PrivateThreadsView(generic.ThreadsView):
    link_name = 'misago:private_threads'
    template = 'misago/privatethreads/list.html'

    Threads = PrivateThreads
    Filtering = PrivateThreadsFiltering


@private_threads_view
class ThreadView(PrivateThreadsMixin, generic.ThreadView):
    pass


@private_threads_view
class GotoLastView(PrivateThreadsMixin, generic.GotoLastView):
    pass


@private_threads_view
class GotoNewView(PrivateThreadsMixin, generic.GotoNewView):
    pass


@private_threads_view
class GotoPostView(PrivateThreadsMixin, generic.GotoPostView):
    pass


@private_threads_view
class ReportedPostsListView(PrivateThreadsMixin, generic.ReportedPostsListView):
    pass


@private_threads_view
class QuotePostView(PrivateThreadsMixin, generic.QuotePostView):
    pass


@private_threads_view
class UnhidePostView(PrivateThreadsMixin, generic.UnhidePostView):
    pass


@private_threads_view
class HidePostView(PrivateThreadsMixin, generic.HidePostView):
    pass


@private_threads_view
class DeletePostView(PrivateThreadsMixin, generic.DeletePostView):
    pass


@private_threads_view
class EventsView(PrivateThreadsMixin, generic.EventsView):
    pass


@private_threads_view
class PostingView(PrivateThreadsMixin, generic.PostingView):
    pass
