from misago.messages.messages import Messages

class MessagesMiddleware(object):
    def process_request(self, request):
        request.messages = Messages(request.session)