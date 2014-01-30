from misago.core import threadstore


class ThreadStoreMiddleware(object):
    def process_response(self, request, response):
        threadstore.clear()
        return response
