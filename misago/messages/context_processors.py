def messages(request):
    return {
        'messages' : request.messages.messages,
    }
