from misago.models import Forum, Thread
from misago.readstrackers import ThreadsTracker

class PrivateThreadsMiddleware(object):
    def process_request(self, request):
        if (request.user.is_authenticated() and
                request.acl.private_threads.can_participate() and
                request.user.sync_pds):
            forum = Forum.objects.special_model('private_threads')
            tracker = ThreadsTracker(request, forum)
            unread_pds = tracker.unread_count(forum.thread_set.filter(participants__id=request.user.pk))
            request.user.sync_unread_pds(unread_pds)
            request.user.save(force_update=True)