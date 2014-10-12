from time import time

from django.conf import settings

from misago.threads.counts import NewThreadsCount, UnreadThreadsCount


class UnreadThreadsCountMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            request.user.new_threads = NewThreadsCount(
                request.user, request.session)
            request.user.unread_threads = UnreadThreadsCount(
                request.user, request.session)

