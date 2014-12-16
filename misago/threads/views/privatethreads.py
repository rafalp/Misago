from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, render
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
    def decorator(f):
        def dispatch(self, request, *args, **kwargs):
            allow_use_private_threads(request.user)
            return f(self, request, *args, **kwargs)
        return dispatch
    klass.dispatch = decorator(klass.dispatch)
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

    def fetch_thread_participants(self, user, thread):
        thread.participants_list = []
        thread.participant = None

        participants_qs = ThreadParticipant.objects.filter(thread=thread)
        participants_qs = participants_qs.select_related('user')
        for participant in participants_qs:
            participant.thread = thread
            thread.participants_list.append(participant)
            if participant.user == user:
                thread.participant = participant
        return thread.participants_list

    def check_thread_permissions(self, request, thread):
        add_acl(request.user, thread.forum)
        add_acl(request.user, thread)

        self.fetch_thread_participants(request.user, thread)

        allow_see_private_thread(request.user, thread)
        allow_use_private_threads(request.user)

    def check_post_permissions(self, request, post):
        add_acl(request.user, post.forum)
        add_acl(request.user, post.thread)
        add_acl(request.user, post)

        self.fetch_thread_participants(request.user, post.thread)

        allow_see_private_post(request.user, post)
        allow_see_private_thread(request.user, post.thread)
        allow_use_private_threads(request.user)

    def exclude_invisible_posts(self, queryset, user, forum, thread):
        return queryset


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
class ThreadParticipantsView(PrivateThreadsMixin, generic.ViewBase):
    template = 'misago/privatethreads/participants.html'

    def dispatch(self, request, *args, **kwargs):
        thread = self.get_thread(request, **kwargs)

        if not request.is_ajax():
            response = render(request, 'misago/errorpages/wrong_way.html')
            response.status_code = 405
            return response

        participants_qs = thread.threadparticipant_set
        participants_qs = participants_qs.select_related('user')

        return self.render(request, {
            'participants': participants_qs.order_by('-is_owner', 'user__slug')
        })


class PrivateThreadActions(generic.ThreadActions):
    def get_available_actions(self, kwargs):
        user = kwargs['user']
        thread = kwargs['thread']

        is_moderator = user.acl['can_moderate_private_threads']
        if thread.participant and thread.participant.is_owner:
            is_owner = True
        else:
            is_owner = False

        actions = []

        if is_moderator and not is_owner:
            actions.append({
                'action': 'takeover',
                'icon': 'level-up',
                'name': _("Takeover thread")
            })

        if is_owner:
            actions.append({
                'action': 'participants',
                'icon': 'users',
                'name': _("Edit participants"),
                'is_button': True
            })

        if is_moderator:
            if thread.is_closed:
                actions.append({
                    'action': 'open',
                    'icon': 'unlock-alt',
                    'name': _("Open thread")
                })
            else:
                actions.append({
                    'action': 'close',
                    'icon': 'lock',
                    'name': _("Close thread")
                })

            actions.append({
                'action': 'delete',
                'icon': 'times',
                'name': _("Delete thread"),
                'confirmation': _("Are you sure you want to delete this "
                                  "thread? This action can't be undone.")
            })

        return actions

    def action_takeover(self, request, thread):
        ThreadParticipant.objects.set_owner(thread, request.user)
        messages.success(request, _("You are now owner of this thread."))


@private_threads_view
class ThreadView(PrivateThreadsMixin, generic.ThreadView):
    template = 'misago/privatethreads/thread.html'
    ThreadActions = PrivateThreadActions


@private_threads_view
class EditThreadParticipantsView(PrivateThreadsMixin, generic.ViewBase):
    template = 'misago/privatethreads/participants_modal.html'

    def dispatch(self, request, *args, **kwargs):
        thread = self.get_thread(request, **kwargs)

        if not request.is_ajax():
            response = render(request, 'misago/errorpages/wrong_way.html')
            response.status_code = 405
            return response

        participants_qs = thread.threadparticipant_set
        participants_qs = participants_qs.select_related('user')

        return self.render(request, {
            'participants': participants_qs.order_by('-is_owner', 'user__slug')
        })

"""
Generics
"""
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
