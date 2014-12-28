from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _, ungettext

from misago.acl import add_acl
from misago.core.exceptions import AjaxError
from misago.core.uiviews import uiview
from misago.forums.models import Forum
from misago.users.decorators import deny_guests

from misago.threads import participants
from misago.threads.events import record_event
from misago.threads.forms.posting import ThreadParticipantsForm
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

    def check_thread_permissions(self, request, thread):
        add_acl(request.user, thread.forum)
        add_acl(request.user, thread)

        participants.make_thread_participants_aware(request.user, thread)

        allow_see_private_thread(request.user, thread)
        allow_use_private_threads(request.user)

    def check_post_permissions(self, request, post):
        add_acl(request.user, post.forum)
        add_acl(request.user, post.thread)
        add_acl(request.user, post)

        participants.make_thread_participants_aware(request.user, thread)

        allow_see_private_post(request.user, post)
        allow_see_private_thread(request.user, post.thread)
        allow_use_private_threads(request.user)

    def exclude_invisible_posts(self, queryset, user, forum, thread):
        return queryset


class PrivateThreads(generic.Threads):
    fetch_pinned_threads = False

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
                'name': _("Take thread over")
            })

        if is_owner:
            actions.append({
                'action': 'participants',
                'icon': 'users',
                'name': _("Edit participants"),
                'is_button': True
            })

            for participant in thread.participants_list:
                if not participant.is_owner:
                    actions.append({
                        'action': 'make_owner:%s' % participant.user_id,
                        'is_hidden': True
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

    @atomic
    def action_takeover(self, request, thread):
        participants.set_thread_owner(thread, request.user)
        messages.success(request, _("You are now owner of this thread."))

        message = _("%(user)s took over this thread.")
        record_event(request.user, thread, 'user', message, {
            'user': request.user,
        })
        thread.save(update_fields=['has_events'])

    @atomic
    def action_make_owner(self, request, thread, new_owner_id):
        new_owner_id = int(new_owner_id)

        new_owner = None
        for participant in thread.participants_list:
            if participant.user.id == int(new_owner_id):
                new_owner = participant.user
                break

        if new_owner:
            participants.set_thread_owner(thread, new_owner)

            message = _("You have passed thread ownership to %(user)s.")
            messages.success(request, message % {'user': new_owner.username})

            message = _("%(user)s passed thread ownership to %(participant)s.")
            record_event(request.user, thread, 'user', message, {
                'user': request.user,
                'participant': new_owner
            })
            thread.save(update_fields=['has_events'])


@uiview("private_threads")
@deny_guests
def event_sender(request, resolver_match):
    if request.user.unread_private_threads:
        message = ungettext("%(threads)s unread private thread",
                            "%(threads)s unread private threads",
                            request.user.unread_private_threads)
        message = message % {'threads': request.user.unread_private_threads}
    else:
        message = _("Private threads")

    return {
        'count': request.user.unread_private_threads,
        'message': message,
    }
    return request.user.unread_private_threads


@private_threads_view
class ThreadView(PrivateThreadsMixin, generic.ThreadView):
    template = 'misago/privatethreads/thread.html'
    ThreadActions = PrivateThreadActions


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
        participants_qs = participants_qs.select_related('user', 'user__rank')

        return self.render(request, {
            'forum': thread.forum,
            'thread': thread,
            'participants': participants_qs.order_by('-is_owner', 'user__slug')
        })


@private_threads_view
class EditThreadParticipantsView(ThreadParticipantsView):
    template = 'misago/privatethreads/participants_modal.html'


@private_threads_view
class BaseEditThreadParticipantView(PrivateThreadsMixin, generic.ViewBase):
    @atomic
    def dispatch(self, request, *args, **kwargs):
        thread = self.get_thread(request, lock=True, **kwargs)

        if not request.is_ajax():
            response = render(request, 'misago/errorpages/wrong_way.html')
            response.status_code = 405
            return response

        if not request.method == "POST":
            raise AjaxError(_("Wrong action received."))

        if not thread.participant or not thread.participant.is_owner:
            raise AjaxError(_("Only thread owner can add or "
                              "remove participants from thread."))

        return self.action(request, thread, kwargs)

    def action(self, request, thread, kwargs):
        raise NotImplementedError("views extending EditThreadParticipantView "
                                  "need to define custom action method")


@private_threads_view
class AddThreadParticipantsView(BaseEditThreadParticipantView):
    template = 'misago/privatethreads/participants_modal_list.html'

    def action(self, request, thread, kwargs):
        form = ThreadParticipantsForm(request.POST, user=request.user)
        if not form.is_valid():
            errors = []
            for field_errors in form.errors.as_data().values():
                errors.extend([unicode(e[0]) for e in field_errors])
            return JsonResponse({'message': errors[0], 'is_error': True})

        event_message = _("%(user)s added %(participant)s to this thread.")
        participants_list = [p.user for p in thread.participants_list]
        for user in form.users_cache:
            if user not in participants_list:
                participants.add_participant(request, thread, user)
                record_event(request.user, thread, 'user', event_message, {
                    'user': request.user,
                    'participant': user
                })
                thread.save(update_fields=['has_events'])

        participants_qs = thread.threadparticipant_set
        participants_qs = participants_qs.select_related('user', 'user__rank')
        participants_qs = participants_qs.order_by('-is_owner', 'user__slug')

        participants_list = [p for p in participants_qs]

        participants_list_html = self.render(request, {
            'forum': thread.forum,
            'thread': thread,
            'participants': participants_list,
        }).content

        message = ungettext("%(users)s participant",
                            "%(users)s participants",
                            len(participants_list))
        message = message % {'users': len(participants_list)}

        return JsonResponse({
            'is_error': False,
            'message': message,
            'list_html': participants_list_html
        })


@private_threads_view
class RemoveThreadParticipantView(BaseEditThreadParticipantView):
    def action(self, request, thread, kwargs):
        user_qs = thread.threadparticipant_set.select_related('user')
        try:
            participant = user_qs.get(user_id=kwargs['user_id'])
        except ThreadParticipant.DoesNotExist:
            return JsonResponse({
                'message': _("Requested participant couldn't be found."),
                'is_error': True,
            })

        if participant.user == request.user:
            return JsonResponse({
                'message': _('To leave thread use "Leave thread" option.'),
                'is_error': True,
            })

        participants_count = len(thread.participants_list) - 1
        if participants_count == 0:
            return JsonResponse({
                'message': _("You can't remove last thread participant."),
                'is_error': True,
            })

        participants.remove_participant(thread, participant.user)
        if not participants.thread_has_participants(thread):
            thread.delete()
        else:
            message = _("%(user)s removed %(participant)s from this thread.")
            record_event(request.user, thread, 'user', message, {
                'user': request.user,
                'participant': participant.user
            })
            thread.save(update_fields=['has_events'])

        participants_count = len(thread.participants_list) - 1
        message = ungettext("%(users)s participant",
                            "%(users)s participants",
                            participants_count)
        message = message % {'users': participants_count}

        return JsonResponse({'is_error': False, 'message': message})


@private_threads_view
class LeaveThreadView(BaseEditThreadParticipantView):
    @atomic
    def dispatch(self, request, *args, **kwargs):
        thread = self.get_thread(request, lock=True, **kwargs)

        try:
            if not request.method == "POST":
                raise RuntimeError(_("Wrong action received."))
            if not thread.participant:
                raise RuntimeError(_("You have to be thread participant in "
                                  "order to be able to leave thread."))

            user_qs = thread.threadparticipant_set.select_related('user')
            try:
                participant = user_qs.get(user_id=request.user.id)
            except ThreadParticipant.DoesNotExist:
                raise RuntimeError(_("You need to be thread "
                                     "participant to leave it."))
        except RuntimeError as e:
            messages.error(request, unicode(e))
            return redirect(thread.get_absolute_url())

        participants.remove_participant(thread, request.user)
        if not thread.threadparticipant_set.exists():
            thread.delete()
        elif thread.participant.is_owner:
            new_owner = user_qs.order_by('id')[:1][0].user
            participants.set_thread_owner(thread, new_owner)

            message = _("%(user)s left this thread. "
                        "%(new_owner)s is now thread owner.")
            record_event(request.user, thread, 'user', message, {
                'user': request.user,
                'new_owner': new_owner
            })
            thread.save(update_fields=['has_events'])
        else:
            message = _("%(user)s left this thread.")
            record_event(request.user, thread, 'user', message, {
                'user': request.user,
            })
            thread.save(update_fields=['has_events'])

        message = _('You have left "%(thread)s" thread.')
        message = message % {'thread': thread.title}
        messages.info(request, message)
        return redirect('misago:private_threads')


@private_threads_view
class PostingView(PrivateThreadsMixin, generic.PostingView):
    def allow_reply(self, user, thread):
        super(PostingView, self).allow_reply(user, thread)

        if user.acl['can_moderate_private_threads']:
            can_reply = not thread.participant
        else:
            can_reply = len(thread.participants_list) > 1

        if not can_reply:
            message = _("You have to add new participants to thread "
                        "before you will be able to reply to it.")
            raise PermissionDenied(message)


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
