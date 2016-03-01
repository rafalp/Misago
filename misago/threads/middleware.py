from misago.threads.counts import sync_user_unread_private_threads_count


class UnreadThreadsCountMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            if request.user.acl['can_use_private_threads']:
                sync_user_unread_private_threads_count(request.user)
