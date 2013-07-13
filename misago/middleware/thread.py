from misago.thread import clear

class ThreadMiddleware(object):
    def process_request(self, request):
        clear()