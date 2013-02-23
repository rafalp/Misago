def messages(request):
    try:
        return {
            'messages' : request.messages.messages,
        }
    except AttributeError:
        pass
