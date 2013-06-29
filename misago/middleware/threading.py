from misago.thread import clear

class ThreadMiddleware(object):
    def process_response(self, request, response):
        clear()
        return response
