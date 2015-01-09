from time import time

from django.conf import settings

from misago.threads.counts import (ModeratedCount, NewThreadsCount,
                                   UnreadThreadsCount,
                                   sync_user_unread_private_threads_count)


class UnreadThreadsCountMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            if request.user.acl['can_review_moderated_content']:
                request.user.moderated_content = ModeratedCount(
                    request.user, request.session)
            request.user.new_threads = NewThreadsCount(
                request.user, request.session)
            request.user.unread_threads = UnreadThreadsCount(
                request.user, request.session)

            if request.user.acl['can_use_private_threads']:
                # special case: count unread threads
                sync_user_unread_private_threads_count(request.user)
