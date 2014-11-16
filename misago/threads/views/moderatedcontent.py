from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.core.uiviews import uiview
from misago.users.decorators import deny_guests

from misago.threads.views.generic.threads import Threads, ThreadsView
from misago.threads.models import Thread
from misago.threads.permissions import exclude_invisible_threads


class ModeratedContent(Threads):
    def get_queryset(self):
        queryset = Thread.objects.filter(has_moderated_posts=True)
        queryset = queryset.select_related('forum')
        queryset = exclude_invisible_threads(queryset, self.user)
        return queryset


class ModeratedContentView(ThreadsView):
    link_name = 'misago:moderated_content'
    template = 'misago/threads/moderated.html'

    Threads = ModeratedContent

    def process_context(self, request, context):
        context['show_threads_locations'] = True

        if request.user.moderated_content != context['threads_count']:
            request.user.moderated_content.set(context['threads_count'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            message = _("You have to sign in to see list of "
                        "moderated content.")
            raise PermissionDenied(message)

        if not request.user.acl['moderated_forums']:
            message = _("You can't review moderated content.")
            raise PermissionDenied(message)

        return super(ModeratedContentView, self).dispatch(
            request, *args, **kwargs)


@uiview("moderated_content")
@deny_guests
def event_sender(request, resolver_match):
    if request.user.acl['moderated_forums']:
        return int(request.user.moderated_content)
    else:
        return 0
