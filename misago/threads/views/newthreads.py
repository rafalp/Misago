from datetime import timedelta

from django.conf import settings
from django.core.exceptions import PermissionDenied
from misago.core.uiviews import uiview
from misago.users.decorators import deny_guests
from django.utils import timezone
from django.utils.translation import ungettext, ugettext as _

from misago.threads.models import Thread
from misago.threads.permissions import exclude_invisible_threads
from misago.threads.views.generic.threads import Threads, ThreadsView


class NewThreads(Threads):
    def get_queryset(self):
        cutoff_days = settings.MISAGO_FRESH_CONTENT_PERIOD
        cutoff_date = timezone.now() - timedelta(days=cutoff_days)
        if cutoff_date < self.user.joined_on:
            cutoff_date = self.user.joined_on

        queryset = Thread.objects.filter(started_on__gte=cutoff_date)
        queryset = queryset.select_related('forum')

        tracked_threads = self.user.threadread_set.all()
        queryset = queryset.exclude(id__in=tracked_threads.values('thread_id'))
        queryset = exclude_invisible_threads(queryset, self.user)
        return queryset


class NewThreadsView(ThreadsView):
    link_name = 'misago:new_threads'
    template = 'misago/threads/new.html'

    Threads = NewThreads

    def process_context(self, request, context):
        context['show_threads_locations'] = True
        context['fresh_period'] = settings.MISAGO_FRESH_CONTENT_PERIOD

        if request.user.new_threads != context['threads_count']:
            request.user.new_threads.set(context['threads_count'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            message = _("You have to sign in to see your list of new threads.")
            raise PermissionDenied(message)
        else:
            return super(NewThreadsView, self).dispatch(
                request, *args, **kwargs)


@uiview("misago_new_threads")
@deny_guests
def event_sender(request, resolver_match):
    if request.user.new_threads:
        message = ungettext("%(threads)s new thread",
                            "%(threads)s new threads",
                            request.user.new_threads)
        message = message % {'threads': request.user.new_threads}
    else:
        message = _("New threads")

    return {
        'count': int(request.user.new_threads),
        'message': message,
    }
