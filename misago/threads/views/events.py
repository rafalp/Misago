from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from misago.core.decorators import ajax_only, require_POST
from misago.users.decorators import deny_guests

from misago.threads.models import Event
from misago.threads.views.generic.base import ViewBase


class EventsView(ViewBase):
    def dispatch(self, request, event_id):
        def toggle_event(request, event):
            event.is_hidden = not event.is_hidden
            event.save(update_fields=['is_hidden'])
            return JsonResponse({'is_hidden': event.is_hidden})

        def delete_event(request, event):
            event.delete();

            event.thread.has_events = event.thread.event_set.exists()
            event.thread.save(update_fields=['has_events'])

            return JsonResponse({'is_deleted': True})

        @ajax_only
        @require_POST
        @deny_guests
        @atomic
        def real_view(request, event_id):
            queryset = Event.objects.select_for_update()
            queryset = queryset.select_related('forum', 'thread')
            event = get_object_or_404(queryset, id=event_id)

            forum = event.forum
            thread = event.thread
            thread.forum = forum

            self.check_forum_permissions(request, forum)
            self.check_thread_permissions(request, thread)

            if request.POST.get('action') == 'toggle':
                if not forum.acl.get('can_hide_events'):
                    raise PermissionDenied(_("You can't hide events."))
                return toggle_event(request, event)
            elif request.POST.get('action') == 'delete':
                if forum.acl.get('can_hide_events') != 2:
                    raise PermissionDenied(_("You can't delete events."))
                return delete_event(request, event)
            else:
                raise PermissionDenied(_("Invalid action requested."))
        return real_view(request, event_id)
